import pennylane as qml
import numpy as np
import mkl

mkl.set_num_threads(1)

import pytest


class QFT:
    def __init__(self, n, dev="default.qubit"):
        self.n = n
        self.dev = qml.device(dev, wires=n)

    def __call__(self):
        @qml.qnode(self.dev)
        def qft_circuit():
            for wire in reversed(range(self.n)):
                qml.Hadamard(wire)
                for i in range(wire):
                    qml.CRZ(np.pi/(2**wire-i), wires=[i,wire])

            for i in range(self.n//2):
                qml.SWAP(wires=[i, self.n - i - 1])

            return qml.probs(wires=range(self.n))
        return qft_circuit()


class QCBM:
    def __init__(self, n, nlayers, dev="default.qubit"):
        self.n = n
        self.nlayers = nlayers
        self.neighbors = [(i, (i + 1) % n) for i in range(n)]
        self.dev = qml.device(dev, wires=n)

    def __call__(self, vars):
        @qml.qnode(self.dev)
        def qcbm_circuit(vars):
            self.first_layer(vars[1])
            for each in vars[2:-2]:
                self.entangler()
                self.mid_layer(each)

            self.entangler()
            self.last_layer(vars[-1])

            return qml.expval(qml.PauliZ(0))

        return qcbm_circuit(vars)

    def generate_random_vars(self):
        vars = [np.random.rand(self.n, 2)]
        vars += [np.random.rand(self.n, 3) for _ in range(self.n - 2)]
        vars += [np.random.rand(self.n, 2)]
        return vars

    @staticmethod
    def first_rotation(alpha, beta, wires=1):
        qml.RX(alpha, wires=wires)
        qml.RZ(beta, wires=wires)

    @staticmethod
    def mid_rotation(alpha, beta, gamma, wires=1):
        qml.RZ(alpha, wires=wires)
        qml.RX(beta, wires=wires)
        qml.RZ(gamma, wires=wires)

    @staticmethod
    def last_rotation(alpha, beta, wires=1):
        qml.RX(alpha, wires=wires)
        qml.RZ(beta, wires=wires)

    def first_layer(self, vars):
        for each in vars:
            self.first_rotation(each[0], each[1])

    def mid_layer(self, vars):
        for each in vars:
            self.mid_rotation(each[0], each[1], each[2])

    def last_layer(self, vars):
        for each in vars:
            self.last_rotation(each[0], each[1])

    def entangler(self):
        for i, j in self.neighbors:
            qml.CNOT(wires=[i, j])


def _raise_exception(self):
    raise Exception()


class GateTest:
    def __init__(self, n, gate, wires, dev="default.qubit", args=()):
        self.n = n
        self.dev = qml.device(dev, wires=n)

        # This ensures that no expectation values are calculated
        # which would skew the results for gate tests
        self.dev.pre_measure = _raise_exception
        self.gate = gate
        self.args = args
        self.wires = wires

    def __call__(self):
        @qml.qnode(self.dev)
        def gate_circuit():
            self.gate(*self.args, wires=self.wires)
            return qml.expval(qml.PauliZ(0))

        def eval():
            try:
                gate_circuit()
            except:
                pass

        return eval()


nqubits_list = range(4,26)


@pytest.mark.parametrize("nqubits", nqubits_list)
def test_qft(benchmark, nqubits):
    benchmark.group = "QFT"
    qft = QFT(nqubits)
    benchmark(qft)

@pytest.mark.parametrize("nqubits", nqubits_list)
def test_QCBM(benchmark, nqubits):
    benchmark.group = "QCBM"
    qcbm = QCBM(nqubits, 9)
    vars = qcbm.generate_random_vars()
    benchmark(qcbm, vars)


@pytest.mark.parametrize("nqubits", nqubits_list)
def test_X(benchmark, nqubits):
    benchmark.group = "X"
    gate_test = GateTest(nqubits, qml.PauliX, [2])
    benchmark(gate_test)

@pytest.mark.parametrize("nqubits", nqubits_list)
def test_H(benchmark, nqubits):
    benchmark.group = "H"
    gate_test = GateTest(nqubits, qml.Hadamard, [2])
    benchmark(gate_test)

@pytest.mark.parametrize("nqubits", nqubits_list)
def test_T(benchmark, nqubits):
    benchmark.group = "T"
    gate_test = GateTest(nqubits, qml.T, [2])
    benchmark(gate_test)

@pytest.mark.parametrize("nqubits", nqubits_list)
def test_Rz(benchmark, nqubits):
    benchmark.group = "Rz"
    gate_test = GateTest(nqubits, qml.RZ, [2], args=(0.5, ))
    benchmark(gate_test)

@pytest.mark.parametrize("nqubits", nqubits_list)
def test_Rx(benchmark, nqubits):
    benchmark.group = "Rx"
    gate_test = GateTest(nqubits, qml.RX, [2], args=(0.5, ))
    benchmark(gate_test)

@pytest.mark.parametrize("nqubits", nqubits_list)
def test_CX(benchmark, nqubits):
    benchmark.group = "CNOT"
    gate_test = GateTest(nqubits, qml.CNOT, [0, 1])
    benchmark(gate_test)


@pytest.mark.parametrize("nqubits", nqubits_list)
def test_Toffoli(benchmark, nqubits):
    benchmark.group = "Toffoli"
    gate_test = GateTest(nqubits, qml.Toffoli, [0, 1, 2])
    benchmark(gate_test)
