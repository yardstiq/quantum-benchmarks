# set threads to one
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export MKL_DOMAIN_NUM_THREADS=1
export JULIA_NUM_THREADS=1

# start benchmark
## 1.Cirq
pytest cirq/benchmark_gates.py --benchmark-save=cirq --benchmark-sort=name
## 2.QISKit
pytest qiskit/benchmarks.py --benchmark-save=qiskit --benchmark-sort=name
## 3.ProjectQ
pytest projectq/benchmark_gates.py --benchmark-save=projectq --benchmark-sort=name
## 4.Yao
julia yao/benchmark_gates.jl yao.csv
