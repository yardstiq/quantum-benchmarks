## Install via

```sh
pip install cirq
```

## Run benchmarks

```sh
OMP_NUM_THREADS=1 pytest benchmark_gates.py --benchmark-save=cirq.json --benchmark-sort=name
```
