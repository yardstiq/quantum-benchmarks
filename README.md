# Quantum Software Benchmarks

## Results

Single Gate Benchmark

![gates](https://github.com/Roger-luo/quantum-benchmarks/blob/master/gates.png)

Parameterized Circuit Benchmark

![pcircuit](https://github.com/Roger-luo/quantum-benchmarks/blob/master/pcircuit.png)

Batched parameterized circuit of Yao and CuYao

![batch-pcircuit](https://github.com/Roger-luo/quantum-benchmarks/blob/master/pcircuit_batch.png)

## Installation

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

This will usually take a few hours to finish, thus if you want to run it in the backend, you can use `nohup`

```sh
nohup bin/benchmark run &
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
