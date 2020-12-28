import numpy as np
from pyquest_cffi import quest
import pytest

env = quest.createQuESTEnv()
nqubits_list = range(4,26)

def entangler(circuit, qubits, pairs):
    for a, b in pairs:
        circuit.cx(qubits[a], qubits[b])
    return circuit

def first_rotation(qubits, nqubits):
    for k in range(nqubits):
        quest.rotateX(qubits, k, np.random.rand())
        quest.rotateZ(qubits, k, np.random.rand())

def mid_rotation(qubits, nqubits):
    for k in range(nqubits):
        quest.rotateZ(qubits, k, np.random.rand())
        quest.rotateX(qubits, k, np.random.rand())
        quest.rotateZ(qubits, k, np.random.rand())

def last_rotation(qubits, nqubits):
    for k in range(nqubits):
        quest.rotateZ(qubits, k, np.random.rand())
        quest.rotateX(qubits, k, np.random.rand())

def entangler(qubits, nqubits, pairs):
    for a, b in pairs:
        quest.controlledNot(qubits, a, b)

def run_qcbm(qubits, nqubits, depth, pairs):
    first_rotation(qubits, nqubits)
    entangler(qubits, nqubits, pairs)
    for k in range(depth):
        mid_rotation(qubits, nqubits)
        entangler(qubits, nqubits, pairs)

    last_rotation(qubits, nqubits)
    return qubits

def run_bench(benchmark, gate, nqubits, args):
    qubits = quest.createQureg(nqubits, env)
    benchmark(gate, qubits, *args)

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_X(benchmark, nqubits):
    benchmark.group = "X"
    run_bench(benchmark, quest.pauliX, nqubits, (3, ))
    
@pytest.mark.parametrize('nqubits', nqubits_list)
def test_H(benchmark, nqubits):
    benchmark.group = "H"
    run_bench(benchmark, quest.hadamard, nqubits, (3, ))

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_T(benchmark, nqubits):
    benchmark.group = "T"
    run_bench(benchmark, quest.tGate, nqubits, (3, ))

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_Rx(benchmark, nqubits):
    benchmark.group = "Rx"
    run_bench(benchmark, quest.rotateX, nqubits, (3, 0.5))

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_Rz(benchmark, nqubits):
    benchmark.group = "Rz"
    run_bench(benchmark, quest.rotateZ, nqubits, (3, 0.5))

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_CNOT(benchmark, nqubits):
    benchmark.group = "CNOT"
    run_bench(benchmark, quest.controlledNot, nqubits, (2, 3))

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_Toffoli(benchmark, nqubits):
    benchmark.group = "Toffoli"
    X = ((0.0, 0.0), (1.0, 0.0), (1.0, 0.0), (0.0, 0.0))
    qubits = quest.createQureg(nqubits, env)
    benchmark(quest.multiControlledUnitary, qubits, [0, 1], 2, 2, X)

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_QCBM(benchmark, nqubits):
    benchmark.group = "QCBM"
    qubits = quest.createQureg(nqubits, env)
    pairs = [(i, (i + 1) % nqubits) for i in range(nqubits)]
    benchmark(run_qcbm, qubits, nqubits, 9, pairs)
