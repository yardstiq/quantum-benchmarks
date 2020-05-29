# Contribution Guide

*By contributing to this benchmark, you are agreeing to release it under [MIT License](LICENSE).*

To contribute new benchmarks, please open a pull request and the maintainer to run it on test machine.

## Shell Scripts
The shell script `bin/benchmark` provides an easy interface to setup benchmarks on arbitrary machine.
If you would like to add a new benchmark please:

- add your new benchmark installation instructions to the shell scripts so one can install it with just running `bin/benchmark install`.
- make sure to add your benchmark command to `benchmark_all_parallel` and `benchmark_all`, if you are not benchmarking your code via [pytest-benchmark](https://pytest-benchmark.readthedocs.io/en/latest/usage.html) please also add a new entry to `benchmark` function.

## Structure of the benchmarks

**Each software/framework benchmark is stored in their corresponding folder with file name `benchmarks.<extension name>`, e.g
`cirq/benchmarks.py`.

To make sure that we are doing the right measurement on execution time, the benchmarks are done with the following frameworks:

- [pytest-benchmark](https://pytest-benchmark.readthedocs.io/en/latest/usage.html) for Python
- [BenchmarkTools.jl](https://github.com/JuliaCI/BenchmarkTools.jl) for Julia

We always use the minimum time in the statistics for all benchmarks, due to [Which estimator should I use?](https://github.com/JuliaCI/BenchmarkTools.jl/blob/master/doc/manual.md#which-estimator-should-i-use)


### Format

The benchmark data is generated in the following way:

- `.benchmarks/<system info folder>/` pytest-based benchmark results are saved into `json` file in this folder
- `.` julia-based benchmark results are saved as CSV files in the root folder

### Labels

Currently we use the following labels in benchmark group:

- `X`, `H`, `T`, `CNOT`, `Toffoli` for single qubit gates
- `QCBM` for parameterized quantum circuits
- `QCBM_batch` for batched parameterized quantum circuits
- `QCBM_cuda` for parameterized quantum circuit simulation on CUDA
- `QCBM_cuda_batch` for batched parameterize quantum circuits on CUDA

### Circuit

The circuit we benchmark is shown as below:

![QCBM](http://tutorials.yaoquantum.org/dev/generated/quick-start/6.quantum-circuit-born-machine/assets/differentiable.png)

Each benchmark script benchmarks such a circuit with 9 entanglers from 4 qubits to 25 qubits.
