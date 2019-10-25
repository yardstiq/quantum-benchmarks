"""
single gate benchmark
"""
import matplotlib
matplotlib.use('TkAgg')
import cirq
import numpy as np
from cirq import Simulator
import pytest
import mkl
mkl.set_num_threads(1)


def run_bench(benchmark, nqubits, gate, locs=(1, )):
    qubits = [cirq.GridQubit(k, 0) for k in range(nqubits)]
    circuit = cirq.Circuit()
    locs = tuple(qubits[k] for k in locs)
    circuit.append(gate(*locs))
    simulator = Simulator(dtype=np.complex128)
    benchmark(simulator.simulate, circuit, qubit_order=qubits)

def layer(n, qubits, first=False, last=False):
    def Rx(theta, k):
        return cirq.XPowGate(exponent=theta)(qubits[k])

    def Rz(theta, k):
        return cirq.ZPowGate(exponent=theta)(qubits[k])

    def Rx_list(theta):
        return [Rx(0.0, k) for k in range(n)]

    def Rz_list(theta):
        return [Rz(0.0, k) for k in range(n)]
    if first:
        return cirq.Moment(Rx_list(0.0)), cirq.Moment(Rz_list(0.0))
    elif last:
        return cirq.Moment(Rz_list(0.0)), cirq.Moment(Rx_list(0.0))
    else:
        return cirq.Moment(Rz_list(0.0)), cirq.Moment(Rx_list(0.0)), cirq.Moment(Rz_list(0.0))

def generate_qcbm_circuit(n, qubits, depth, pairs):
    circuit = cirq.Circuit()
    circuit.append(layer(n, qubits, first=True))
    circuit.append((cirq.CNOT(qubits[i], qubits[j]) for i, j in pairs), strategy=cirq.InsertStrategy.NEW)

    for _ in range(depth - 1):
        circuit.append(layer(n, qubits))
        circuit.append(cirq.CNOT(qubits[i], qubits[j]) for i, j in pairs)

    circuit.append(layer(n, qubits, last=True))
    return circuit

nbit_list = range(4,26)

@pytest.mark.parametrize('nqubits', nbit_list)
def test_X(benchmark, nqubits):
    benchmark.group = "X"
    run_bench(benchmark, nqubits, cirq.X)

@pytest.mark.parametrize('nqubits', nbit_list)
def test_H(benchmark, nqubits):
    benchmark.group = "H"
    run_bench(benchmark, nqubits, cirq.H)

@pytest.mark.parametrize('nqubits', nbit_list)
def test_T(benchmark, nqubits):
    benchmark.group = "T"
    run_bench(benchmark, nqubits, cirq.T)

@pytest.mark.parametrize('nqubits', nbit_list)
def test_CX(benchmark, nqubits):
    benchmark.group = "CNOT"
    run_bench(benchmark, nqubits, cirq.CNOT, (1, 2))

@pytest.mark.parametrize('nqubits', nbit_list)
def test_CY(benchmark, nqubits):
    benchmark.group = "C-Rx(0.5)"
    run_bench(benchmark, nqubits, cirq.CNotPowGate(exponent=0.5), (2, 3))

@pytest.mark.parametrize('nqubits', nbit_list)
def test_Toffoli(benchmark, nqubits):
    benchmark.group = "Toffoli"
    run_bench(benchmark, nqubits, cirq.TOFFOLI, (2, 3, 0))

@pytest.mark.parametrize('nqubits', range(4, 26))
def test_QCBM(benchmark, nqubits):
    benchmark.group = "QCBM"
    qubits = [cirq.GridQubit(k, 0) for k in range(nqubits)]
    circuit = generate_qcbm_circuit(nqubits, qubits, 10,
            [(i, (i+1) % nqubits) for i in range(nqubits)])
    simulator = Simulator()
    benchmark(simulator.simulate, circuit, qubit_order=qubits)
