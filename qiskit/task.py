import pytest
import mkl
import uuid
from numba import cuda
from qiskit import Aer, QuantumCircuit
from qiskit.compiler import transpile, assemble
mkl.set_num_threads(1)

backend = Aer.get_backend("qasm_simulator")
default_options = {
    "method": "statevector",   # Force dense statevector method for benchmarks
    "truncate_enable": False,  # Disable unused qubit truncation for benchmarks
    "max_parallel_threads": 1  # Disable OpenMP parallelization for benchmarks
}

def _execute(controller, qobj_aer):
    controller(qobj_aer)
    cuda.synchronize()
    return

def native_execute(circuit, backend_options=None):
    experiment = transpile(circuit, backend)
    qobj = assemble(experiment, shots=1)
    qobj_aer = backend._format_qobj(qobj, backend_options, None)
    _execute(backend._controller, qobj_aer)

def run_bench(benchmark, nqubits, gate, locs=(1, )):
    qc = QuantumCircuit(nqubits)
    getattr(qc, gate)(*locs)
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


nqubits = 30
pairs = [(i, (i + 1) % nqubits) for i in range(nqubits)]
circuit = generate_qcbm_circuit(nqubits, 9, pairs)
    # Set simulation method to the GPU statevector
gpu_options = default_options.copy()
gpu_options["method"] = "statevector_gpu"
native_execute(circuit, gpu_options)
