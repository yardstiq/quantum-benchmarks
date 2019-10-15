# Quantum Software Benchmarks

## Results

Single Gate Benchmark

![gates](https://github.com/Roger-luo/quantum-benchmarks/blob/master/gates.png)

Parameterized Circuit Benchmark

**NOTE: qiskit benchmark here looks physically wrong (should scales exponentially), I still need more investigation on it.**

![pcircuit](https://github.com/Roger-luo/quantum-benchmarks/blob/master/pcircuit.png)

Batched parameterized circuit of Yao and CuYao

![batch-pcircuit](https://github.com/Roger-luo/quantum-benchmarks/blob/master/pcircuit_batch.png)

## Installation

You should be able to run this benchmark with the `bin/benchmark` script.

```
    Quantum Circuit Simulation Benchmark

install                 install dependencies
run [package]           run benchmark of [package] or run all benchmarks by default
parallel [package]      spawn [package] benchmark in a process or run all benchmark in parallel by default
help                    print this message
```

### Requirements

- [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html?highlight=conda)
- [Python 3](https://www.python.org/downloads/)
- [Julia 1.0+](https://julialang.org/)
- [CUDA Toolkit (optional)](https://developer.nvidia.com/cuda-toolkit) for benchmarking Yao's CUDA backend

Make sure you have the above required dependency installed, then run the following script, which will install
all the dependencies for you.

```sh
bin/benchmark install
```

If you prefer a virtual environment to run the benchmark, please create one using either `conda` or `virtualenv`
before you install the dependencies with `bin/benchmark`.

## Run Benchmark

```sh
bin/benchmark run
```

This will usually take a few hours to finish, thus if you want to run it in the backend, you can use `parallel`

## Generate Plots

```sh
python plot.py
```

## Platform Info

Julia & CPU Info

```
julia> versioninfo()
Julia Version 1.2.0
Commit c6da87ff4b (2019-08-20 00:03 UTC)
Platform Info:
  OS: Linux (x86_64-pc-linux-gnu)
  CPU: Intel(R) Xeon(R) Gold 6230 CPU @ 2.10GHz
  WORD_SIZE: 64
  LIBM: libopenlibm
  LLVM: libLLVM-6.0.1 (ORCJIT, skylake)
```

BLAS: intel MKL

Python version: 3.7.3

GPU: Tesla V100

## Package Info

|       Package        | Version |
| -------------------- | ------- |
| Yao                  | v0.6.0  |
| CuYao                | v0.1.3  |
| qiskit               | 0.11.0  |
| qiskit-aer           | 0.2.3   |
| qiskit-aqua          | 0.5.2   |
| qiskit-ignis         | 0.1.1   |
| qiskit-terra         | 0.8.2   |
| projectq             | 0.4.2   |
| PennyLane            | 0.5.0   |

## Acknowledge

We thank [Juan Gomez](https://github.com/atilag) for reviewing the benchmark of qiskit.
