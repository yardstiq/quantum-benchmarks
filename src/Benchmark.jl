module Benchmark

export Project
using Pkg.TOML

const tab = "  "
const benchmark_toml = "Benchmark.toml"

Base.@kwdef struct Project
    name::String
    author::Vector{String} = []
    path::String = ""
    executable::String = "julia"
    script::String = "benchmarks.jl"
    setup_file::String = "setup.jl"
    data_file::String = "data.json"
    version::VersionNumber = v"0.0.0"
end

function Project(dirname::String)
    filename = joinpath(dirname, benchmark_toml)
    if ispath(filename)
        config = TOML.parsefile(filename)
    else
        error("cannot find configuration file Benchmark.toml")
    end

    if haskey(config, "version")
        config["version"] = VersionNumber(config["version"])
    else
        config["version"] = v"0.0.0"
    end

    d = Dict{Symbol, Any}()
    for (k, v) in config
        d[Symbol(k)] = v
    end

    return Project(;path=dirname, d...)
end

function Base.show(io::IO, pj::Project)
    indent = get(io, :indent, 0)
    println(io, tab^indent, "Benchmark Project:")
    for name in fieldnames(Project)
        println(io, tab^indent, tab, name, ": ", getfield(pj, name))
    end
end

function Base.run(project::Project; wait=true)
    script = joinpath(project.path, project.script)
    cmd = `$(project.executable) $script`
    return run(cmd; wait=wait)
end

function Base.run(projects::Vector{Project}; parallel=false)
    if !parallel
        for each in projects
            run(each)
        end
        return
    end

    # there are always <number of cores - 1> projects running
    ptr = 1; N = Sys.CPU_THREADS ÷ 2 - 1
    while ptr != length(projects)
        ps = Base.Process[]
        for k in 1:N
            ptr += 1
            if ptr <= length(projects)
                pj = projects[ptr]
                p = run(pj; wait=false)
                push!(ps, p)
            end
        end
        wait.(ps)
    end
    return
end

function scan_projects(path::String, excludes=["bin", "images", "img", "data", "src"])
    projects = Project[]
    for (root, dirs, files) in walkdir(path)
        for file in files
            if file == benchmark_toml
                push!(projects, Project(root))
            end
        end
    end
    return projects
end

function setup(project::Project)
    exec = project.executable
    setup = joinpath(project.path, project.setup_file)

    printstyled("setting up  ", color=:light_blue)
    printstyled(project.name, color=:bold)
    printstyled("  ...\n", color=:light_blue)
    run(`$exec $setup`)
    return
end

function setup(projects::Vector{Project})
    for each in projects
        setup(each)
    end
    return
end

const help_msg = """
    benchmark <cmd> <options>

-h, --help, help                show this message

run [project] [--parallel]      run project, will run all possible
                                project if no project name specified
                                if parallel is specified, the benchmark
                                will be run in parallel

setup [project]                 setup project, or setup all possible
                                project under current working directory
"""

function main()
    if isempty(ARGS) || ARGS[1] in ["-h", "--help", "help"]
        print(help_msg)
    elseif ARGS[1] == "run"
        if length(ARGS) == 1
            projects = scan_projects(pwd())
            run(projects; parallel = length(ARGS) == 2 && ARGS[2] in ["-p", "--parallel"])
        else
            pj = Project(ARGS[2])
            run(pj)
        end
    elseif ARGS[1] == "setup"
        if length(ARGS) == 1
            projects = scan_projects(pwd())
            setup(projects)
        else
            setup(Project(ARGS[2]))
        end
    else
        print(help_msg)
    end
end

end # module
