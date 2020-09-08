using Yao, Yao.YaoBlocks.ConstGate, BenchmarkTools
using JSON
using LinearAlgebra, Pkg
using CuYao, CuArrays

BLAS.set_num_threads(1)

const nqubits=4:25
const benchmarks = Dict()

layer(nbit::Int, x::Symbol) = layer(nbit, Val(x))
layer(nbit::Int, ::Val{:first}) = chain(nbit, put(i=>chain(Rx(0), Rz(0))) for i = 1:nbit);
layer(nbit::Int, ::Val{:last}) = chain(nbit, put(i=>chain(Rz(0), Rx(0))) for i = 1:nbit)
layer(nbit::Int, ::Val{:mid}) = chain(nbit, put(i=>chain(Rz(0), Rx(0), Rz(0))) for i = 1:nbit);
entangler(pairs) = chain(control(ctrl, target=>X) for (ctrl, target) in pairs);
function build_circuit(n, nlayers, pairs)
    circuit = chain(n)
    push!(circuit, layer(n, :first))
    for i in 2:nlayers
        push!(circuit, entangler(pairs))
        push!(circuit, layer(n, :mid))
    end
    push!(circuit, entangler(pairs))
    push!(circuit, layer(n, :last))
    return circuit
end

macro task(name::String, nqubits_ex, body)
    nqubits = nqubits_ex.args[2]
    msg = "benchmarking $name"
    quote
        @info $msg
        benchmarks[$(name)] = Dict()
        benchmarks[$(name)]["nqubits"] = $(esc(nqubits))
        benchmarks[$(name)]["times"] = $(esc(body))
    end
end

@task "X" nqubits=nqubits begin
    map(nqubits) do k
        t = @benchmark apply!(st, $(put(k, 2=>X))) setup=(st=rand_state($k))
        minimum(t).time
    end
end

@task "H" nqubits=nqubits begin
    map(nqubits) do k
        t = @benchmark apply!(st, $(put(k, 2=>H))) setup=(st=rand_state($k))
        minimum(t).time
    end
end

@task "T" nqubits=nqubits begin
    map(nqubits) do k
        t = @benchmark apply!(st, $(put(k, 2=>T))) setup=(st=rand_state($k))
        minimum(t).time
    end
end

@task "CNOT" nqubits=nqubits begin
    map(nqubits) do k
        t = @benchmark apply!(st, $(control(k, 2, 3=>X))) setup=(st=rand_state($k))
        minimum(t).time
    end
end

@task "Rx(0.5)" nqubits=nqubits begin
    map(nqubits) do k
        t = @benchmark apply!(st, $(put(k, 2=>Rx(0.5)))) setup=(st=rand_state($k))
        minimum(t).time
    end
end

@task "Rz(0.5)" nqubits=nqubits begin
    map(nqubits) do k
        t = @benchmark apply!(st, $(put(k, 2=>Rz(0.5)))) setup=(st=rand_state($k))
        minimum(t).time
    end
end

@task "CRx(0.5)" nqubits=nqubits begin
    map(nqubits) do k
        t = @benchmark apply!(st, $(control(k, 2, 3=>Rx(0.5)))) setup=(st=rand_state($k))
        minimum(t).time
    end
end

@task "Toffoli" nqubits=nqubits begin
    map(nqubits) do k
        t = @benchmark apply!(st, $(control(k, (2, 3), 1=>X))) setup=(st=rand_state($k))
        minimum(t).time
    end
end

const qcbm_nqubits = 4:25

@task "QCBM" nqubits=qcbm_nqubits begin
    map(qcbm_nqubits) do k
        t = @benchmark apply!(st, $(build_circuit(k, 9, [(i, mod1(i+1, k)) for i in 1:k]))) setup=(st=zero_state($k))
        minimum(t).time
    end
end

@task "QCBM (batch)" nqubits=4:15 begin
    map(4:15) do k
        t = @benchmark apply!(st, $(build_circuit(k, 9, [(i, mod1(i+1, k)) for i in 1:k]))) setup=(st=zero_state($k, nbatch=1000))
        minimum(t).time
    end
end

@static if CuArrays.functional()

    @task "QCBM (cuda)" nqubits=qcbm_nqubits begin
        map(qcbm_nqubits) do k
            t = @benchmark CuArrays.@sync(apply!(st, $(build_circuit(k, 9, [(i, mod1(i+1, k)) for i in 1:k])))) setup=(st=cu(zero_state($k)))
            minimum(t).time
        end
    end

    @task "QCBM (batch) (cuda)" nqubits=4:15 begin
        map(4:15) do k
            t = @benchmark CuArrays.@sync(apply!(st, $(build_circuit(k, 9, [(i, mod1(i+1, k)) for i in 1:k])))) setup=(st=cu(zero_state($k, nbatch=1000)))
            minimum(t).time
        end
    end

end


if !ispath("data")
    mkpath("data")
end

write("data/data.json", JSON.json(benchmarks))
