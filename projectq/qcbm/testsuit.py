'''
Several Models used for testing.
'''

import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree

from .blocks import get_demo_circuit
from .dataset import gaussian_pdf, barstripe_pdf
from .qcbm import QCBM
from .mmd import RBFMMD2
from .structure import chowliu_tree, nearest_neighbor, random_tree
from .contexts import ProjectQContext


def load_gaussian(num_bit, depth, context='scipy'):
    '''gaussian distribution.'''
    geometry = (num_bit,)
    hndim = 2**num_bit

    # standard circuit
    pairs = nearest_neighbor(geometry)
    circuit = get_demo_circuit(num_bit, depth, pairs)

    # bar and stripe
    p_bs = gaussian_pdf(geometry, mu=hndim/2., sigma=hndim/4.)

    # mmd loss
    mmd = RBFMMD2([0.25,4], num_bit, False)

    # Born Machine
    bm = QCBM(circuit, mmd, p_bs)
    if context == 'projectq':
        bm.context = ProjectQContext
    return bm

def load_barstripe(geometry, depth, context='scipy', structure='nn'):
    '''3 x 3 bar and stripes.'''
    num_bit = np.prod(geometry)

    # bar and stripe
    p_bs = barstripe_pdf(geometry)

    # standard circuit
    if structure == 'random-tree':
        pairs = random_tree()
    elif structure == 'chowliu-tree':
        pairs = chowliu_tree(p_bs)
    elif structure == 'ring':
        pairs = [(i, (i+1)%num_bit) for i in range(num_bit)]
    elif structure == 'nn':
        # nearest neighbor
        pairs = nearest_neighbor(geometry)
    else:
        raise ValueError('unknown entangle structure %s!'%structure)
    circuit = get_demo_circuit(num_bit, depth, pairs)

    # mmd loss
    mmd = RBFMMD2([0.5], num_bit, True)

    # Born Machine
    bm = QCBM(circuit, mmd, p_bs)
    if context == 'projectq':
        bm.context = ProjectQContext
    return bm
