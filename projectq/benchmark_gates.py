#!/usr/bin/env python
import numpy as np
from contexts import ProjectQContext
from projectq import ops
from functools import reduce
from qcbm.testsuit import load_barstripe

import mkl
mkl.set_num_threads(1)

import pytest

def run_bench(benchmark, G, locs, nqubits):
    with ProjectQContext(nqubits, 'simulate') as cc:
        qureg = cc.qureg
        eng = qureg.engine
        qi = take_locs(qureg, locs)
        benchmark(run_gate, eng, G, qi)

def take_locs(qureg, locs):
    if isinstance(locs, int):
        return qureg[locs]
    elif isinstance(locs, tuple):
        return tuple(qureg[loc] for loc in locs)
    elif isinstance(locs, slice):
        return qureg[sls]
    elif locs is None:
        return qureg
    else:
        raise

def run_gate(eng, G, qi):
    G | qi
    eng.flush()

def ising_hamiltonian(nqubits):
    H1 = reduce(lambda x,y: x+y, [1/4. * ops.QubitOperator("Z%d Z%d"%(i, i+1)) for i in range(nqubits-1)])
    H2 = reduce(lambda x,y: x+y, [1/4 * ops.QubitOperator("X%d"%(i, )) for i in range(nqubits)])
    return H1 + H2

################### Tests #################
nqubits_list = range(4,26)
@pytest.mark.parametrize('nqubits', nqubits_list)
def test_X(benchmark, nqubits):
    benchmark.group = "X"
    run_bench(benchmark, ops.X, 2, nqubits)

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_H(benchmark, nqubits):
    benchmark.group = "H"
    run_bench(benchmark, ops.H, 2, nqubits)

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_T(benchmark, nqubits):
    benchmark.group = "T"
    run_bench(benchmark, ops.T, 2, nqubits)

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_CX(benchmark, nqubits):
    benchmark.group = "CNOT"
    run_bench(benchmark, ops.CNOT, (2,3), nqubits)

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_CY(benchmark, nqubits):
    benchmark.group = "C-Rx(0.5)"
    run_bench(benchmark, ops.C(ops.Rx(0.5)), (2,3), nqubits)

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_Toffoli(benchmark, nqubits):
    benchmark.group = "Toffoli"
    run_bench(benchmark, ops.Toffoli, (2,3,0), nqubits)

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_Measure(benchmark, nqubits):
    benchmark.group = "Measure"
    run_bench(benchmark, ops.All(ops.Measure), None, nqubits)

@pytest.mark.parametrize('nqubits', range(4,16))
def test_TimeEvolution(benchmark, nqubits):
    benchmark.group = "TimeEvolution"
    run_bench(benchmark, ops.TimeEvolution(1.0, ising_hamiltonian(nqubits)), None, nqubits)

@pytest.mark.parametrize('nbit', range(4, 16))
def test_X(benchmark, nbit):
    benchmark.group = "QCBM"
    bm = load_barstripe((nbit, 1), 10, structure='ring', context='projectq')
    theta_list = np.random.rand(bm.circuit.num_param)*2*np.pi
    with bm.context( bm.circuit.num_bit, 'simulate') as cc:
        benchmark(bm.circuit, cc.qureg, theta_list)
