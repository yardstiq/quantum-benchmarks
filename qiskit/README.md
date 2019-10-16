# Qiskit Benchmark

This benchmark script uses `pytest.benchmark` to benchmark qiskit's `statevector` simulator.

However, the builtin `execute` API will submit the job as a separate process, thus, we implemented
our own `execute` function `native_execute` to execute the job natively on the master process without
counting compilation time.
