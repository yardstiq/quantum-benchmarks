import pytest
import mkl
import uuid
from qiskit import Aer, QuantumCircuit
from qiskit.compiler import transpile, assemble
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