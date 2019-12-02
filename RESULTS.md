# Benchmark Results

- [Benchmark Results](#benchmark-results)
  - [Single Thread Benchmark](#single-thread-benchmark)
    - [Machine Info](#machine-info)
    - [Package Info](#package-info)
    - [Single Gate Benchmark](#single-gate-benchmark)
    - [Parameterized Circuit Benchmark](#parameterized-circuit-benchmark)
    - [Batched parameterized circuit of Yao and CuYao](#batched-parameterized-circuit-of-yao-and-cuyao)

## Single Thread Benchmark

This benchmark only include single thread benchmark, all the multithread features are disabled.

### Machine Info

Julia & CPU Info

```
julia> versioninfo()
Julia Version 1.3.0
Commit 46ce4d7933 (2019-11-26 06:09 UTC)
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

### Package Info

|       Package        | Version |
| -------------------- | ------- |
| Yao                  | v0.6.0-DEV  |
| CuYao                | v0.1.3  |
| qiskit               | 0.13.0  |
| qiskit-aer           | 0.3.2   |
| qiskit-terra         | 0.10.2  |
| qulacs               | 0.1.8   |
| projectq             | 0.4.2   |
| Cirq                 | 0.6.0   |
| PennyLane            | 0.7.0   |
| QuEST (pyquest-cffi) | 0.1.1   |


### Single Gate Benchmark

![gates](https://github.com/Roger-luo/quantum-benchmarks/blob/master/images/gates.png)
![gates-relative](https://github.com/Roger-luo/quantum-benchmarks/blob/master/images/gates_relative.png)

### Parameterized Circuit Benchmark

NOTE: 

- qiskit state vector simulator does not support rotation x/z gate, thus there is no benchmark on the following circuits.
- PennyLane benchmark contains some overhead from error handling since we do not include measurement in this benchmark (https://github.com/Roger-luo/quantum-benchmarks/pull/7)
- the performance of CUDA may vary on different machine (https://github.com/Roger-luo/quantum-benchmarks/issues/6), although the difference is not very huge

![pcircuit](https://github.com/Roger-luo/quantum-benchmarks/blob/master/images/pcircuit.png)
![pcircuit-relative](https://github.com/Roger-luo/quantum-benchmarks/blob/master/images/pcircuit_relative.png)
