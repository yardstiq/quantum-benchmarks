import pennylane as qml
from pennylane import numpy as np
import mkl
mkl.set_num_threads(1)

import pytest


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
            return [qml.expval(qml.PauliZ(k)) for k in range(self.n)]

        return qcbm_circuit(vars)

    def generate_random_vars(self):
        vars = [np.random.rand(self.n, 2)]
        vars += [np.random.rand(self.n, 3) for _ in range(self.n-2)]
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


@pytest.mark.parametrize('nqubits', range(4,26))
def qcbm(benchmark, nqubits):
    benchmark.group = "QCBM"
    qcbm = QCBM(nqubits, 9)
    vars = qcbm.generate_random_vars()
    benchmark(qcbm, vars)
