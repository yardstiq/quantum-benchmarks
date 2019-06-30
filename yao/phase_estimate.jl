using Yao, FFTW, LinearAlgebra, BitBasis

A(i, j) = control(i, j=>shift(2π/(1<<(i-j+1))))
B(n, i) = chain(n, i==j ? put(i=>H) : A(j, i) for j in i:n)
qft(n) = chain(B(n, i) for i in 1:n)

struct QFT{N} <: PrimitiveBlock{N} end
QFT(n::Int) = QFT{n}()
YaoBlocks.mat(::Type{T}, x::QFT) where T = mat(T, qft(nqubits(x)))
YaoBlocks.print_block(io::IO, x::QFT{N}) where N = print(io, "QFT($N)")

function YaoBlocks.apply!(r::ArrayReg, x::QFT)
    α = sqrt(length(statevec(r)))
    invorder!(r)
    lmul!(α, ifft!(statevec(r)))
    return r
end

Hadamards(n) = repeat(H, 1:n)
ControlU(n, m, U) = chain(n+m, control(k, n+1:n+m=>matblock(U^(2^(k-1)))) for k in 1:n)

PE(n, m, U) =
    chain(n+m, # total number of the qubits
        concentrate(Hadamards(n), 1:n), # apply H in local scope
        ControlU(n, m, U),
        concentrate(QFT(n)', 1:n))

N, M = 3, 5
P = eigen(rand_unitary(1<<M)).vectors
θ = Int(0b110) / 1<<N
phases = rand(1<<M)
phases[bit"010"] = θ
U = P * Diagonal(exp.(2π * im * phases)) * P'

r = join(ArrayReg(psi), zero_state(N))
r |> PE(N, M, U)
results = measure(r, 1:N; nshots=1)
estimated_phase = bfloat(results[]; nbits=N)
