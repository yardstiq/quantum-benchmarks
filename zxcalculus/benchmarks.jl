using YaoLang: YaoIR, is_pure_quantum
using ZXCalculus
using BenchmarkTools, JSON

function zx_load_qasm(filename::String)
    srcs = readlines("circuits/$(filename)")
    src = prod([srcs[1]; srcs[3:end]])
    # m = @__MODULE__
    # ir = YaoIR(m, src, :qasm_circ)
    # ir.pure_quantum = is_pure_quantum(ir)
    # zxd = ZXDiagram(ir)
    zxd = ZXDiagram(src, Val(:qasm))
    return zxd
end
function run_benchmark()
    filenames = readdir("circuits")
    benchmarks = Dict()
    for circ_name in filenames
        println("benchmarking $circ_name")
        zxd = zx_load_qasm(circ_name)
        b = @benchmark phase_teleportation($zxd)
        tc = tcount(phase_teleportation(zxd))
        # println(circ_name, "\ttime = ", (mean(b).time / 1e9), "(s)\tT-count = ", tc)
        benchmarks[circ_name] = Dict()
        benchmarks[circ_name]["times"] = Dict()
        benchmarks[circ_name]["times"]["mean"] = mean(b).time
        benchmarks[circ_name]["times"]["min"] = minimum(b).time
        benchmarks[circ_name]["times"]["max"] = maximum(b).time
        benchmarks[circ_name]["T-count"] = tc
    end
    return benchmarks
end

benchmarks = run_benchmark()

if !ispath("data")
    mkpath("data")
end

write("data/data.json", JSON.json(benchmarks))
