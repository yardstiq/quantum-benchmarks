import pytest
import mkl
from qiskit import *
mkl.set_num_threads(1)

backend = Aer.get_backend('statevector_simulator')

def run_bench(benchmark, nqubits, gate, locs=(1, )):
    qubits = QuantumRegister(nqubits)
    circuit = QuantumCircuit(qubits)
    locs = [qubits[k] for k in locs]
    getattr(circuit, gate)(*locs)
    benchmark(execute, circuit, backend)


nbit_list = range(4,15)

@pytest.mark.parametrize('nqubits', nbit_list)
def test_X(benchmark, nqubits):
    benchmark.group = "X"
    run_bench(benchmark, nqubits, 'x')

@pytest.mark.parametrize('nqubits', nbit_list)
def test_H(benchmark, nqubits):
    benchmark.group = "H"
    run_bench(benchmark, nqubits, 'h')

@pytest.mark.parametrize('nqubits', nbit_list)
def test_T(benchmark, nqubits):
    benchmark.group = "T"
    run_bench(benchmark, nqubits, 't')

@pytest.mark.parametrize('nqubits', nbit_list)
def test_CX(benchmark, nqubits):
    benchmark.group = "CNOT"
    run_bench(benchmark, nqubits, 'cx', (1, 2))

# qiskit doesn't support?
# @pytest.mark.parametrize('nqubits', nbit_list)
# def test_CY(benchmark, nqubits):
#     benchmark.group = "C-Rx(0.5)"
#     run_bench(benchmark, nqubits, '', (2, 3))

@pytest.mark.parametrize('nqubits', nbit_list)
def test_Toffoli(benchmark, nqubits):
    benchmark.group = "Toffoli"
    run_bench(benchmark, nqubits, 'ccx', (2, 3, 0))
