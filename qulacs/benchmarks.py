import numpy as np
from qulacs import QuantumCircuit, QuantumState
from qulacs.gate import X, T, H, CNOT, ParametricRZ, ParametricRX, DenseMatrix

import pytest

nqubits_list = range(4,26)

def first_rotation(circuit, nqubits):
    for k in range(nqubits):
        circuit.add_RX_gate(k, np.random.rand())
        circuit.add_RZ_gate(k, np.random.rand())

def mid_rotation(circuit, nqubits):
    for k in range(nqubits):
        circuit.add_RZ_gate(k, np.random.rand())
        circuit.add_RX_gate(k, np.random.rand())
        circuit.add_RZ_gate(k, np.random.rand())

def last_rotation(circuit, nqubits):
    for k in range(nqubits):
        circuit.add_RZ_gate(k, np.random.rand())
        circuit.add_RX_gate(k, np.random.rand())


def entangler(circuit, nqubits, pairs):
    for a, b in pairs:
        circuit.add_CNOT_gate(a, b)

def build_circuit(nqubits, depth, pairs):
    circuit = QuantumCircuit(nqubits)
    first_rotation(circuit, nqubits)
    entangler(circuit, nqubits, pairs)
    for k in range(depth):
        mid_rotation(circuit, nqubits)
        entangler(circuit, nqubits, pairs)

    last_rotation(circuit, nqubits)
    return circuit


def bench_gate(benchmark, nqubits, gate, locs):
    st = QuantumState(nqubits)
    g = gate(*locs)
    benchmark(g.update_quantum_state, st)

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_X(benchmark, nqubits):
    benchmark.group = "X"
    bench_gate(benchmark, nqubits, X, (3, ))

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_T(benchmark, nqubits):
    benchmark.group = "T"
    bench_gate(benchmark, nqubits, T, (3, ))

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_H(benchmark, nqubits):
    benchmark.group = "H"
    bench_gate(benchmark, nqubits, H, (3, ))

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_CNOT(benchmark, nqubits):
    benchmark.group = "CNOT"
    bench_gate(benchmark, nqubits, CNOT, (2, 3))

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_Toffoli(benchmark, nqubits):
    benchmark.group = "Toffoli"
    toffoli = DenseMatrix(0, [[0,1],[1,0]])
    toffoli.add_control_qubit(1,1)
    toffoli.add_control_qubit(2,1)
    st = QuantumState(nqubits)
    benchmark(toffoli.update_quantum_state, st)

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_QCBM(benchmark, nqubits):
    benchmark.group = "QCBM"
    pairs = [(i, (i + 1) % nqubits) for i in range(nqubits)]
    circuit = build_circuit(nqubits, 9, pairs)
    st = QuantumState(nqubits)
    benchmark(circuit.update_quantum_state, st)
