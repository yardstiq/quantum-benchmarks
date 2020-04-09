# JKQ-DDSIM Benchmark

This benchmark uses Google Benchmark to measure the runtime of the jkq-ddsim simulator.

For more information visit [the university site](http://iic.jku.at/eda/research/quantum_simulation) or the [GitHub repo](https://github.com/iic-jku/ddsim).
The benchmark itself ist implemented in [apps/benchmark.cpp](https://github.com/iic-jku/ddsim/blob/v1.0.1a/apps/benchmark.cpp) for anyone interested the API design.

## Short Explanation

The simulator uses decision diagrams (DDs) to represent quantum state and operations.
This data structure is able to exploit redundancies in the state (vector) and operations (matrizes) and often provides a drastic reduction in required memeory.
The one-operations benchmarks clearly show this: The runtime remains linear with the number of qubits.
In contrast, the states in the quasi-random QCBM benchmark do not have the potential for compaction and, hence, the simulator tanks.

For more information, please visit the websites linked above.


## Usage

This folder contains two files:

- `install.sh` clones the jkq-ddsim repository, initializes the submodules and builds the benchmark binary in `ddsim/build/apps/ddsim_benchmark`. This should be called during installation of the benchmark set (`../bin/benchmark install`). Subsequent invocations on this script pull from the repository, update the submodules and re-build the executable.
- `benchmarks.sh` runs the benchmarks. It provides console output and saves a JSON file to `../data/jkq-ddsim.json`.

The user does not need to call the scripts by themself, it is handled via the `../bin/benchmark` script.

The QCBM executions takes very long, so this might be skipped by adjusting the filter as described in the script as comment.
