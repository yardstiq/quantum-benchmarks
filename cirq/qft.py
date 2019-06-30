import cirq

def _cz_and_swap(q0, q1, rot):
    yield cirq.CZ(q0, q1)**rot
    yield cirq.SWAP(q0,q1)

# Create a quantum fourier transform circuit for 2*2 planar qubit architecture.
# Circuit is adopted from https://arxiv.org/pdf/quant-ph/0402196.pdf
def generate_2x2_grid_qft_circuit():
    # Define a 2*2 square grid of qubits.
    a,b,c,d = [cirq.GridQubit(0, 0), cirq.GridQubit(0, 1),
               cirq.GridQubit(1, 1), cirq.GridQubit(1, 0)]

    circuit = cirq.Circuit.from_ops(
        cirq.H(a),
        _cz_and_swap(a, b, 0.5),
        _cz_and_swap(b, c, 0.25),
        _cz_and_swap(c, d, 0.125),
        cirq.H(a),
        _cz_and_swap(a, b, 0.5),
        _cz_and_swap(b, c, 0.25),
        cirq.H(a),
        _cz_and_swap(a, b, 0.5),
        cirq.H(a),
        strategy=cirq.InsertStrategy.EARLIEST
    )
    return circuit
