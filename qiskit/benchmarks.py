import pytest
import mkl
from qiskit import *
from qiskit.compiler import transpile, assemble
mkl.set_num_threads(1)

backend = Aer.get_backend('statevector_simulator')

def run_bench(benchmark, nqubits, gate, locs=(1, )):
    qubits = QuantumRegister(nqubits)
    circuit = QuantumCircuit(qubits)
    locs = [qubits[k] for k in locs]
    getattr(circuit, gate)(*locs)
    experiments = circuit
    basis_gates = None
    coupling_map = None  # circuit transpile options
    backend_properties = None
    initial_layout = None
    seed_transpiler = None
    optimization_level = None
    pass_manager = None
    qobj_id = None
    qobj_header = None
    shots = 1024  # common run options
    memory = False
    max_credits = 10
    seed_simulator = None
    default_qubit_los = None
    default_meas_los = None  # schedule run options
    schedule_los = None
    meas_level = 2
    meas_return = 'avg'
    memory_slots = None
    memory_slot_size = 100
    rep_time = None
    parameter_binds = None
    seed = None
    seed_mapper = None  # deprecated
    config = None
    circuits = None

    run_config = {}
    experiments = transpile(experiments,
                            basis_gates=basis_gates,
                            coupling_map=coupling_map,
                            backend_properties=backend_properties,
                            initial_layout=initial_layout,
                            seed_transpiler=seed_transpiler,
                            optimization_level=optimization_level,
                            backend=backend,
                            pass_manager=pass_manager,
                            seed_mapper=seed_mapper,  # deprecated
                            )
    qobj = assemble(experiments,
                    qobj_id=qobj_id,
                    qobj_header=qobj_header,
                    shots=shots,
                    memory=memory,
                    max_credits=max_credits,
                    seed_simulator=seed_simulator,
                    default_qubit_los=default_qubit_los,
                    default_meas_los=default_meas_los,
                    schedule_los=schedule_los,
                    meas_level=meas_level,
                    meas_return=meas_return,
                    memory_slots=memory_slots,
                    memory_slot_size=memory_slot_size,
                    rep_time=rep_time,
                    parameter_binds=parameter_binds,
                    backend=backend,
                    config=config,  # deprecated
                    seed=seed,  # deprecated
                    run_config=run_config
                    )

    benchmark(backend.run, qobj, **run_config)

def first_rotation(circuit, qubits):
    for each in qubits:
        circuit.rx(1.0, each)
        circuit.rz(1.0, each)
    return circuit

def mid_rotation(circuit, qubits):
    for each in qubits:
        circuit.rz(1.0, each)
        circuit.rx(1.0, each)
        circuit.rz(1.0, each)
    return circuit

def last_rotation(circuit, qubits):
    for each in qubits:
        circuit.rz(1.0, each)
        circuit.rx(1.0, each)
    return circuit

def entangler(circuit, qubits, pairs):
    for a, b in pairs:
        circuit.cx(qubits[a], qubits[b])
    return circuit

def generate_qcbm_circuit(n, depth, pairs):
    qubits = QuantumRegister(n)
    circuit = QuantumCircuit(qubits)
    circuit = first_rotation(circuit, qubits)
    circuit = entangler(circuit, qubits, pairs)
    for k in range(depth-1):
        circuit = mid_rotation(circuit, qubits)
        circuit = entangler(circuit, qubits, pairs)
    circuit = last_rotation(circuit, qubits)
    return circuit


nbit_list = range(4,18)

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

@pytest.mark.parametrize('nqubits', range(4, 16))
def test_qcbm(benchmark, nqubits):
    benchmark.group = "QCBM"
    circuit = generate_qcbm_circuit(nqubits, 9,
        [(i, (i+1)%nqubits) for i in range(nqubits)])
    benchmark(execute, circuit, backend)
