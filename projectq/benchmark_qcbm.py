#!/usr/bin/env python
'''
Learning 2 x 3 bar and stripe using Born Machine.
'''
import numpy as np
import pytest

from qcbm.testsuit import load_barstripe

import mkl
mkl.set_num_threads(1)

np.random.seed(2)

# the testcase used in this program.
@pytest.mark.parametrize('nbit', range(4, 16))
def test_X(benchmark, nbit):
    benchmark.group = "qcbm"
    bm = load_barstripe((nbit, 1), 10, structure='ring', context='projectq')
    theta_list = np.random.rand(bm.circuit.num_param)*2*np.pi
    with bm.context( bm.circuit.num_bit, 'simulate') as cc:
        benchmark(bm.circuit, cc.qureg, theta_list)
