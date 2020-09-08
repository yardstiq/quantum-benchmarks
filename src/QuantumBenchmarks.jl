module QuantumBenchmarks

using Pkg
using Pkg.TOML
using JSON
using Distributed
using Comonicon
using Comonicon.PATH

export scan_projects, conda, setup_project, read_version, execute_project, ncores

const EXCLUDE_PATHS = ["images", "src", "build", "deps", "bin", "test"]

const EXT_TO_INTERPRETER = Dict(
    ".sh" => "bash",
    ".jl" => "julia",
    ".py" => "python",
)

function miniconda_url()
    res = "https://repo.continuum.io/miniconda/Miniconda3-latest-"
    if Sys.isapple()
        res *= "MacOSX"
    elseif Sys.islinux()
        res *= "Linux"
    else
        error("Unsuported OS.")
    end

    # mapping of Julia architecture names to Conda architecture names, where they differ
    arch2conda = Dict(:i686 => :x86)

    if Sys.ARCH in (:i686, :x86_64, :ppc64le)
        res *= string('-', get(arch2conda, Sys.ARCH, Sys.ARCH))
    else
        error("Unsupported architecture: $(Sys.ARCH)")
    end

    res *= ".sh"
    return res
end

conda_path(xs...) = PATH.project(QuantumBenchmarks, "bin", "conda", xs...)
conda_exe() = conda_path("bin", "conda")
conda_cmd(commands::String...) = Cmd([conda_exe(), commands...])
conda_cmd(cmd::Cmd) = conda_cmd(cmd.exec...)
conda(commands...) = Base.run(conda_cmd(commands...))

function setup_conda()
    installer = PATH.project(QuantumBenchmarks, "bin", "miniconda.sh")
    @info "downloading Miniconda3 to $installer"
    download(miniconda_url(), installer)

    @info "installing Miniconda3"
    chmod(installer, 33261) # 33261 corresponds to 755 mode of the 'chmod' program
    Base.run(`$installer -b -f -p $(conda_path())`)
    conda(`update -n base -c defaults conda -y`)
    return
end

function project_env(path::String)
    PROJECT_ENV = copy(ENV)

    PROJECT_ENV["OMP_NUM_THREADS"]="1"
    PROJECT_ENV["MKL_NUM_THREADS"]="1"
    PROJECT_ENV["MKL_DOMAIN_NUM_THREADS"]="1"
    PROJECT_ENV["JULIA_NUM_THREADS"]="1"

    PROJECT_ENV["CONDA"] = conda_exe()
    PROJECT_ENV["ACTIVATE"] = conda_path("bin", "activate")
    PROJECT_ENV["CONDA_PATH"] = conda_path()
    PROJECT_ENV["JULIA"] = joinpath(Sys.BINDIR, Base.julia_exename())
    # Benchmark Project Path
    PROJECT_ENV["BENCHMARK_ROOT_PATH"] = PATH.project(QuantumBenchmarks)
    PROJECT_ENV["BENCHMARK_BIN_PATH"] = PATH.project(QuantumBenchmarks, "bin")

    PROJECT_ENV["BENCHMARK_PATH"] = path
    PROJECT_ENV["BENCHMARK_DATA_PATH"] = joinpath(path, "data")
    PROJECT_ENV["BENCHMARK_LOG_PATH"] = joinpath(path, "log")
    PROJECT_ENV["PYTEST_BENCHMARK"] = raw"""
    ./env/bin/pytest benchmarks.py --benchmark-storage="file://data" \
        --benchmark-save="data" --benchmark-sort=name --benchmark-min-rounds=5
    """
    return PROJECT_ENV
end

set_project_env(cmd::Cmd, project) = setenv(cmd, project_env(project))

function check_script(project::String, name::String)
    script = joinpath(project, name)
    isfile(script) || error("a script named \"$name\" is required in $project")
    chmod(script, 33261) # 33261 corresponds to 755 mode of the 'chmod' program
    return script
end

function scan_projects(root::String=PATH.project(QuantumBenchmarks); exclude=EXCLUDE_PATHS)
    projects = String[]
    for each in readdir(root)
        path = joinpath(root, each)
        if !(each in exclude) && isdir(path) && !startswith(each, ".") && !startswith(each, "_")
            if ["benchmarks", "setup"] ⊆ readdir(path)
                push!(projects, each)
            end
        end
    end
    return projects
end

function setup_project(project::String)
    script = check_script(project, "setup")

    cd(project) do
        Base.run(set_project_env(`./setup`, project))
    end
end

function execute_project(project::String)
    @info "benchmarking $project"
    script = check_script(project, "benchmarks")

    cd(project) do
        Base.run(pipeline(set_project_env(`./benchmarks`, project); stdout="log.out", stderr="log.err"))
    end
end

function read_version(project::String)
    script = check_script(project, "version")
    raw = cd(project) do
        readchomp(set_project_env(`./version`, project))
    end
    
    version = Dict()
    for line in split(raw, "\n")
        name, ver = strip.(split(line, "="))
        version[name] = VersionNumber(ver)
    end
    
    return version
end

function print_version(root, name)
    vers = read_version(joinpath(root, name))
    printstyled("Benchmark Project "; color=:light_blue)
    printstyled(name, ":"; bold=true)
    println()

    for (k, v) in vers
        println(" ", k, ": ", v)
    end
end

"""
list benchmark projects

# Arguments

- `root`: root path of all projects. default is root path of this package.
"""
@cast function list(root::String=PATH.project(QuantumBenchmarks))
    projects = scan_projects(root)
    if isempty(projects)
        print("cannot find any benchmark projects")
    else
        println(length(projects), " found:")
        for each in projects
            printstyled("  ", each; color=:light_blue)
            println()
        end
    end
end

function ncores()
    if Sys.islinux()
        raw = readchomp(pipeline(`grep ^cpu\\scores /proc/cpuinfo`, `uniq`, `awk '{print $4}'`))
    elseif Sys.isapple()
        raw = readchomp(`/usr/sbin/sysctl -n hw.physicalcpu`)
    else
        error("unsupported OS")
    end
    return parse(Int, raw)
end

"""
run a benchmark project or all benchmark projects under `root` directory.

# Arguments

- `project`: name of the project, optional.

# Options

- `--root <path>`: path of the root directory, default is this package directory.
"""
@cast function run(project::String=""; root::String=PATH.project(QuantumBenchmarks))
    if isempty(project)
        projects = scan_projects(root)
        isempty(projects) && return
        length(projects) == 1 && return execute_project(joinpath(root, projects[1]))

        workers = addprocs(ncores();exeflags=["--project=$(PATH.project(QuantumBenchmarks))"])
        Distributed.remotecall_eval(Main, workers, :(using QuantumBenchmarks: execute_project))
        for tasks in Iterators.partition(projects, ncores())
            @sync for each in tasks
                @spawnat :any execute_project(each)
            end
        end
    else
        execute_project(joinpath(root, project))
    end
    return
end

"""
setup a benchmark project or all benchmark projects under `root` directory.

# Arguments

- `project`: name of the project, optional.

# Options

- `--root <path>`: path of the root directory, default is this package directory.
"""
@cast function setup(project::String=""; root::String=PATH.project(QuantumBenchmarks))
    if !ispath(conda_path())
        setup_conda()
    end
    
    if isempty(project)
        for each in scan_projects(root)
            setup_project(joinpath(root, each))
        end
    else
        setup_project(joinpath(root, project))
    end
end

"""
print version info of given benchmark project.

# Arguments

- `project`: name of the project, optional.

# Options

- `--root <path>`: path of the root directory, default is this package directory.
"""
@cast function version(project::String=""; root::String=PATH.project(QuantumBenchmarks))
    if isempty(project)
        for each in scan_projects(root)
            print_version(root, each)
        end
    else
        print_version(root, project)
    end
end

# function verify_datafile_json(path::String)
#     d = JSON.parsefile(path)
# end

@main name="benchmark" doc="""
Quantum Computing Software Benchmark. 
Copyright (C) 2020 Xiu-Zhe (Roger) Luo <rogerluo.rl18@gmail.com> and contributors
Distributed under terms of the MIT license.
"""

end
