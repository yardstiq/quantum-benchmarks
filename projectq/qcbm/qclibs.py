'''
elementary library for quantum computation.

the scipy sparse matrix version.
'''

import scipy as np
import pdb
import scipy.sparse as sps
from scipy.sparse import kron

######  Pauli Matrices  ########

I2 = sps.eye(2).tocsr()
sx = sps.csr_matrix([[0,1],[1,0.]])
sy = sps.csr_matrix([[0,-1j],[1j,0.]])
sz = sps.csr_matrix([[1,0],[0,-1.]])

p0 = (sz + I2) / 2
p1 = (-sz + I2) / 2
h = (sx + sz) / np.sqrt(2.)
sxyz = [I2, sx, sy, sz]

# single bit rotation matrices

def _ri(si, theta):
    return np.cos(theta/2.)*I2 - 1j*np.sin(theta/2.)*si

def rx(theta):
    return _ri(sx, theta)

def ry(theta):
    return _ri(sy, theta)

def rz(theta):
    return _ri(sz, theta)

def rot(t1, t2, t3):
    '''
    a general rotation gate rz(t3)rx(r2)rz(t1).

    Args:
        t1, t2, t3 (float): three angles.

    Returns:
        2x2 csr_matrix: rotation matrix.
    '''
    return rz(t3).dot(rx(t2)).dot(rz(t1))

# multiple bit construction

def CNOT(ibit, jbit, n):
    res = _([p0, I2], [ibit, jbit], n)
    res = res + _([p1, sx], [ibit, jbit], n)
    return res

def _(ops, locs, n):
    '''
    Put operators in a circuit and compile them.

    notice the big end are high loc bits!

    Args:
        ops (list): list of single bit operators.
        locs (list): list of positions.
        n (int): total number of bits.

    Returns:
        csr_matrix: resulting matrix.
    '''
    if np.ndim(locs) == 0:
        locs = [locs]
    if not isinstance(ops, (list, tuple)):
        ops = [ops]
    locs = np.asarray(locs)
    locs = n - locs
    order = np.argsort(locs)
    locs = np.concatenate([[0], locs[order], [n + 1]])
    return _wrap_identity([ops[i] for i in order], np.diff(locs) - 1)


def _wrap_identity(data_list, num_bit_list):
    if len(num_bit_list) != len(data_list) + 1:
        raise Exception()

    res = sps.eye(2**num_bit_list[0])
    for data, nbit in zip(data_list, num_bit_list[1:]):
        res = kron(res, data)
        res = kron(res, sps.eye(2**nbit, dtype='complex128'))
    return res
