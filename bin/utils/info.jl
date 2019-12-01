using PyCall, Pkg, InteractiveUtils
using LinearAlgebra, Markdown

VERSIONS = Dict()

qiskit = pyimport("qiskit")
VERSIONS["qiskit"] = qiskit.__qiskit_version__["qiskit"]
VERSIONS["qiskit-terra"] = qiskit.__qiskit_version__["qiskit-terra"]
VERSIONS["qiskit-aer"] = qiskit.__qiskit_version__["qiskit-aer"]

VERSIONS["projectq"] = pyimport("projectq").__version__
VERSIONS["pennylane"] = pyimport("pennylane").__version__
VERSIONS["Yao"] = Pkg.installed()["Yao"]
VERSIONS["CuYao"] = Pkg.installed()["CuYao"]

text = md"""
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
$(sprint(versioninfo))
```

**Julia BLAS vendor**

$(LinearAlgebra.BLAS.vendor())
"""