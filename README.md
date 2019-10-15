# Quantum Software Benchmarks

We benchmark several popular quantum computation softwares/frameworks/simulators to test their performance
in practical daily research.

This benchmark is written with the following principals:

- tries to use the user interface (UI) instead of high performance hack from internals.
- focus on laptop runnable scale instead of High Performance Cluster scale (4-25 qubits)

## Results

### Single Gate Benchmark

![gates](https://github.com/Roger-luo/quantum-benchmarks/blob/master/images/gates.png)
![gates-relative](https://github.com/Roger-luo/quantum-benchmarks/blob/master/images/gates_relative.png)

### Parameterized Circuit Benchmark

NOTE: qiskit state vector simulator does not support rotation x/z gate, thus there is no benchmark on the following circuits.

![pcircuit](https://github.com/Roger-luo/quantum-benchmarks/blob/master/images/pcircuit.png)
![pcircuit-relative](https://github.com/Roger-luo/quantum-benchmarks/blob/master/images/pcircuit_relative.png)

### Batched parameterized circuit of Yao and CuYao

![batch-pcircuit](https://github.com/Roger-luo/quantum-benchmarks/blob/master/images/pcircuit_batch.png)
![batch-pcircuit-relative](https://github.com/Roger-luo/quantum-benchmarks/blob/master/images/pcircuit_batch_relative.png)

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

This will usually take a few hours to finish, thus if you want to run it in the backend, you can use `parallel`.
You can generate the plot by running:

```sh
bin/plot
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
| qiskit-terra         | 0.8.2   |
| projectq             | 0.4.2   |
| PennyLane            | 0.5.0   |
| QuEST (pyquest-cffi) | 0.1.1   |

## Acknowledge

We thank [Juan Gomez](https://github.com/atilag) for reviewing the benchmark of qiskit.
