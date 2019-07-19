# Quantum Software Benchmarks

## Results

Parameterized Circuit Benchmark

![pcircuit](https://github.com/Roger-luo/quantum-benchmarks/blob/master/pcircuit.png)

## Installation

1. Install Python packages

```sh
pip install -r requiurements.txt
```

2. Install Julia packages

enter Julia REPL, press `]`

```jl
(pkg) > add Yao CuYao DataFrames CSV
```

## Run Benchmarks

```sh
sh benchmarks.sh
```

## Generate Plots

```sh
python plot.py
```

## Platform Info

Julia & CPU Info

```
julia> versioninfo()
Julia Version 1.1.1
Commit 55e36cc (2019-05-16 04:10 UTC)
Platform Info:
  OS: Linux (x86_64-linux-gnu)
  CPU: Intel(R) Core(TM) i7-6800K CPU @ 3.40GHz
  WORD_SIZE: 64
  LIBM: libopenlibm
  LLVM: libLLVM-6.0.1 (ORCJIT, broadwell)
Environment:
  JULIA_NUM_THREADS = 12
```

BLAS: intel MKL

Python version: 3.7.3

GPU: TITAN Xp

### Yao Version

```
[b48ca7a8] CuYao v0.1.0
[5872b779] Yao v0.5.0
```

### Cirq Version

v0.5.0

### qiskit version

qiskit: 62dd60a1cd45a1d49b8238a5d26ef82b3b7e59b0
qiskit-terra: bfd1f859fc79c36190322ade8359f88ce4adb48e
qiskit-aer: 558b0bbc27d2562248f5b5ae81a578acba7a3d3c
qiskit-aqua: 422e74b3a0d73b24994359f460085a24bf03ca89

### ProjectQ

v0.4.2

## Acknowledge

We thank [Juan Gomez](https://github.com/atilag) for reviewing the benchmark of qiskit.
