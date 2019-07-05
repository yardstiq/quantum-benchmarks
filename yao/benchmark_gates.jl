using Yao, Yao.YaoBlocks.ConstGate, BenchmarkTools
using LinearAlgebra
BLAS.set_num_threads(1)

benchmarks = Dict()

@info "benchmarking X"
benchmarks["X"] = map(4:26) do k
    t = @benchmark apply!(st, $(put(k, 2=>X))) setup=(st=rand_state($k))
    k, minimum(t).time
end

@info "benchmarking H"
benchmarks["H"] = map(4:26) do k
    t = @benchmark apply!(st, $(put(k, 2=>H))) setup=(st=rand_state($k))
    k, minimum(t).time
end

@info "benchmarking T"
benchmarks["T"] = map(4:26) do k
    t = @benchmark apply!(st, $(put(k, 2=>ConstGate.T))) setup=(st=rand_state($k))
    k, minimum(t).time
end

@info "benchmarking CNOT"
benchmarks["CNOT"] = map(4:26) do k
    t = @benchmark apply!(st, $(control(k, 2, 3=>X))) setup=(st=rand_state($k))
    k, minimum(t).time
end

@info "benchmarking CRx"
benchmarks["CRx(0.5)"] = map(4:26) do k
    t = @benchmark apply!(st, $(control(k, 2, 3=>Rx(0.5)))) setup=(st=rand_state($k))
    k, minimum(t).time
end

@info "benchmarking Toffoli"
benchmarks["Toffoli"] = map(4:26) do k
    t = @benchmark apply!(st, $(control(k, (2, 3), 1=>X))) setup=(st=rand_state($k))
    k, minimum(t).time
end

using DataFrames, CSV
df = DataFrame(
    nqubits=4:26,
    X=benchmarks["X"],
    H=benchmarks["H"],
    T=benchmarks["T"],
    CNOT=benchmarks["CNOT"],
    CRx=benchmarks["CRx(0.5)"],
    Toffoli=benchmarks["Toffoli"])

CSV.write(ARGS[1], df)
