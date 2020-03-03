# Quantum Software Benchmarks

We benchmark several popular quantum computation softwares/frameworks/simulators to test their performance
in practical daily research.

This benchmark is written with the following principles:

- try to use the user interface (UI) instead of high performance hack from internals.
- focus on laptop runnable scale (4-25 qubits) instead of High Performance Cluster scale

## Results

<img src="https://github.com/Roger-luo/quantum-benchmarks/blob/master/images/gates.png" alt="single gate benchmark (absolute timing)" height=600></img>

The complete results are included in [RESULTS.md](https://github.com/Roger-luo/quantum-benchmarks/blob/master/RESULTS.md)

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

## Contributing

Please feel free to update and add new benchmarks. Check [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## Acknowledge

We thank the following people for reviewing our benchmarks:

- [Juan Gomez](https://github.com/atilag), [Christopher J. Wood](https://github.com/chriseclectic) for reviewing qiskit
- [Craig Gidney](https://github.com/Strilanc) for reviewing Cirq
- [corryvrequan](https://github.com/corryvrequan) for reviewing qulacs
- [Damian Steiger](https://github.com/damiansteiger) for reviewing ProjectQ
- [johannesjmeyer](https://github.com/johannesjmeyer) for reviewing PennyLane

## License

[MIT license](LICENSE)
