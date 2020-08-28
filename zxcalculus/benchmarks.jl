using YaoLang: YaoIR, is_pure_quantum
using ZXCalculus
using BenchmarkTools

function zx_load_qasm(filename::String)
    srcs = readlines("circuits/$(filename)")
    src = prod([srcs[1]; srcs[3:end]])
    m = @__MODULE__
    ir = YaoIR(m, src, :qasm_circ)
    ir.pure_quantum = is_pure_quantum(ir)
    zxd = ZXDiagram(ir)
    return zxd
end
function run_benchmark()
    filenames = readdir("circuits")
    bms = Dict()
    for circ_name in filenames
        zxd = zx_load_qasm(circ_name)
        b = @benchmark phase_teleportation($zxd)
        println(circ_name, "\t time = ", (mean(b).time / 1e9), tcount(phase_teleportation(zxd)))
        bms[circ_name] = b
    end
    return bms
end

println("Benchmarking ZXCalculus.jl...")
bms = run_benchmark()
