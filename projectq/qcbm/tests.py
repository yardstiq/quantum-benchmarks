import numpy as np
from numpy.testing import dec, assert_, assert_raises,\
    assert_almost_equal, assert_allclose
import matplotlib.pyplot as plt
import pdb, os
import scipy.sparse as sps

from .blocks import get_demo_circuit
from .structure import nearest_neighbor
from .dataset import gaussian_pdf, barstripe_pdf
from .contexts import ProjectQContext, ScipyContext
from .mmd import RBFMMD2
from .train import train
from .testsuit import load_gaussian, load_barstripe
from .qclibs import rot, CNOT, ry, I2

def test_dataset():
    geometry = (3,3)
    pl2 = barstripe_pdf(geometry)
    assert_((pl2>1e-5).sum()==14)

def test_bm():
    depth = 2
    np.random.seed(2)

    #bm = load_gaussian(6, depth)
    bm = load_barstripe((3,3), depth)
    theta_list = np.random.random(bm.circuit.num_param)*2*np.pi

    assert_(bm.depth == depth)
    print('loss = %s'%bm.mmd_loss(theta_list))
    g1 = bm.gradient(theta_list)
    g2 = bm.gradient_numerical(theta_list)
    assert_allclose(g1, g2, atol=1e-5)

def test_wf():
    depth = 0
    geometry = (6,)

    num_bit = np.prod(geometry)
    pairs = nearest_neighbor(geometry)
    circuit = get_demo_circuit(num_bit, depth, pairs)

    # cross check
    theta_list = np.random.random(circuit.num_param)
    with ScipyContext(np.prod(geometry)) as cc2:
        circuit(cc2.qureg, theta_list)
    with ProjectQContext(np.prod(geometry), 'simulate') as cc:
        circuit(cc.qureg, theta_list)
    assert_allclose(cc.wf, cc2.wf)

def test_qclib():
    cnot = CNOT(1,0,2)
    assert_(cnot.nnz==4)
    assert_allclose(cnot.toarray(), sps.coo_matrix(([1,1,1,1],([0,1,2,3],[0,1,3,2]))).toarray())
    assert_allclose(rot(-np.pi/2.,np.pi/4.,np.pi/2.).toarray(),ry(np.pi/4.).toarray())

if __name__ == '__main__':
    test_dataset()
    test_wf()
    test_bm()
    test_qclib()
