import numpy as np
import cirq


class QftInverse(cirq.Gate):

    def __init__(self, num_qubits):
        super(QftInverse, self)
        self._num_qubits = num_qubits

    def num_qubits(self):
        return self._num_qubits

    def _decompose_(self, qubits):
        qubits = list(qubits)
        while len(qubits) > 0:
            q_head = qubits.pop(0)
            yield cirq.H(q_head)
            for i, qubit in enumerate(qubits):
                yield (cirq.CZ**(-1/2.0**(i+1)))(qubit, q_head)


def run_estimate(unknown_gate, qnum, repetitions):
    qubits = [None] * qnum
    for i in range(len(qubits)):
        qubits[i] = cirq.GridQubit(0, i)
    ancilla = cirq.GridQubit(0, len(qubits))

    circuit = cirq.Circuit.from_ops(
        cirq.H.on_each(*qubits),
        [cirq.ControlledGate(unknown_gate**(2**i)).on(qubits[qnum-i-1], ancilla)
         for i in range(qnum)],
        QftInverse(qnum)(*qubits),
        cirq.measure(*qubits, key='phase'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=repetitions)
    return result


def experiment(qnum, repetitions=100):

    def example_gate(phi):
        gate = cirq.SingleQubitMatrixGate(
            matrix=np.array([[np.exp(2*np.pi*1.0j*phi), 0], [0, 1]]))
        return gate

    print('Estimation with {}qubits.'.format(qnum))
    print('Actual, Estimation (Raw binary)')
    errors = []
    fold_func = lambda ms: ''.join(np.flip(ms, 0).astype(int).astype(str))
    for phi in np.arange(0, 1, 0.1):
        result = run_estimate(example_gate(phi), qnum, repetitions)
        hist = result.histogram(key='phase', fold_func=fold_func)
        estimate_bin = hist.most_common(1)[0][0]
        estimate = (sum([float(s)*0.5**(order+1)
                         for order, s in enumerate(estimate_bin)]))
        print('{:0.4f}, {:0.4f} ({})'.format(phi, estimate, estimate_bin))
        errors.append((phi-estimate)**2)
    print('RMS Error: {:0.4f}\n'.format(np.sqrt(sum(errors)/len(errors))))


def main(qnums = (2, 4, 8), repetitions=100):
    for qnum in qnums:
        experiment(qnum, repetitions=repetitions)


if __name__ == '__main__':
    main()
