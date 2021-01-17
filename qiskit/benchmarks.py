import pytest
import mkl
import uuid
from qiskit import Aer, QuantumCircuit
from qiskit.compiler import transpile, assemble
import numpy as np
mkl.set_num_threads(1)

backend = Aer.get_backend("qasm_simulator")
default_options = {
    "method": "statevector",   # Force dense statevector method for benchmarks
    "truncate_enable": False,  # Disable unused qubit truncation for benchmarks
    "max_parallel_threads": 1  # Disable OpenMP parallelization for benchmarks
}

def _execute(circuit, backend_options=None):
    experiment = transpile(circuit, backend)
    qobj = assemble(experiment, shots=1)
    qobj_aer = backend._format_qobj(qobj, backend_options, None)
    return backend._controller(qobj_aer)

def native_execute(benchmark, circuit, backend_options=None):
    experiment = transpile(circuit, backend)
    qobj = assemble(experiment, shots=1)
    qobj_aer = backend._format_qobj(qobj, backend_options, None)
    benchmark(backend._controller, qobj_aer)

def run_bench(benchmark, nqubits, gate, args=(3, )):
    qc = QuantumCircuit(nqubits)
    getattr(qc, gate)(*args)
    native_execute(benchmark, qc, default_options)

def first_rotation(circuit, nqubits):
    circuit.rx(1.0, range(nqubits))
    circuit.rz(1.0, range(nqubits))
    return circuit

def mid_rotation(circuit, nqubits):
    circuit.rz(1.0, range(nqubits))
    circuit.rx(1.0, range(nqubits))
    circuit.rz(1.0, range(nqubits))
    return circuit

def last_rotation(circuit, nqubits):
    circuit.rz(1.0, range(nqubits))
    circuit.rx(1.0, range(nqubits))
    return circuit

def entangler(circuit, pairs):
    for a, b in pairs:
        circuit.cx(a, b)
    return circuit

def generate_qcbm_circuit(nqubits, depth, pairs):
    circuit = QuantumCircuit(nqubits)
    first_rotation(circuit, nqubits)
    entangler(circuit, pairs)
    for k in range(depth-1):
        mid_rotation(circuit, nqubits)
        entangler(circuit, pairs)
    last_rotation(circuit, nqubits)
    return circuit

def qft_rotations(circuit, n):
    """Performs qft on the first n qubits in circuit (without swaps)"""
    if n == 0:
        return circuit
    n -= 1
    circuit.h(n)
    for qubit in range(n):
        circuit.cu1(np.pi/2**(n-qubit), qubit, n)
    # At the end of our function, we call the same function again on
    # the next qubits (we reduced n by one earlier in the function)
    return qft_rotations(circuit, n)

def swap_registers(circuit, n):
    for qubit in range(n//2):
        circuit.swap(qubit, n-qubit-1)
    return circuit

def generate_qft_circuit(nqubits):
    qc = QuantumCircuit(nqubits)
    qc = qft_rotations(qc, nqubits)
    qc = swap_registers(qc, nqubits)
    return qc


nqubit_list = range(4, 26)

@pytest.mark.parametrize('nqubits', nqubit_list)
def test_X(benchmark, nqubits):
    benchmark.group = "X"
    run_bench(benchmark, nqubits, 'x')

@pytest.mark.parametrize('nqubits', nqubit_list)
def test_H(benchmark, nqubits):
    benchmark.group = "H"
    run_bench(benchmark, nqubits, 'h')

@pytest.mark.parametrize('nqubits', nqubit_list)
def test_T(benchmark, nqubits):
    benchmark.group = "T"
    run_bench(benchmark, nqubits, 't')

@pytest.mark.parametrize('nqubits', nqubit_list)
def test_Rx(benchmark, nqubits):
    benchmark.group = "Rx"
    run_bench(benchmark, nqubits, 'rx', (0.5, 3))

@pytest.mark.parametrize('nqubits', nqubit_list)
def test_Rz(benchmark, nqubits):
    benchmark.group = "Rz"
    run_bench(benchmark, nqubits, 'rz', (0.5, 3))

@pytest.mark.parametrize('nqubits', nqubit_list)
def test_CX(benchmark, nqubits):
    benchmark.group = "CNOT"
    run_bench(benchmark, nqubits, 'cx', (1, 2))

@pytest.mark.parametrize('nqubits', nqubit_list)
def test_Toffoli(benchmark, nqubits):
    benchmark.group = "Toffoli"
    run_bench(benchmark, nqubits, 'ccx', (2, 3, 0))

@pytest.mark.parametrize('nqubits', nqubit_list)
def test_qcbm(benchmark, nqubits):
    benchmark.group = "QCBM"
    pairs = [(i, (i + 1) % nqubits) for i in range(nqubits)]
    circuit = generate_qcbm_circuit(nqubits, 9, pairs)
    native_execute(benchmark, circuit, default_options)

@pytest.mark.parametrize('nqubits', nqubit_list)
def test_qft(benchmark, nqubits):
    benchmark.group = "QFT"
    circuit = generate_qft_circuit(nqubits)
    native_execute(benchmark, circuit, default_options)

# NOTE: The following benchmark requires installing Qiskit Aer with GPU
# which is currently only available for Linux
# install with: `pip install qiskit qiskit-aer-gpu`
@pytest.mark.parametrize('nqubits', nqubit_list)
def test_qcbm_cuda(benchmark, nqubits):
    benchmark.group = "QCBM (cuda)"
    pairs = [(i, (i + 1) % nqubits) for i in range(nqubits)]
    circuit = generate_qcbm_circuit(nqubits, 9, pairs)
    # Set simulation method to the GPU statevector
    gpu_options = default_options.copy()
    gpu_options["method"] = "statevector_gpu"
    native_execute(benchmark, circuit, gpu_options)
