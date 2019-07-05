#!/usr/bin/env python
import numpy as np
import time
from contexts import ProjectQContext
from projectq import ops
from functools import reduce

import mkl
mkl.set_num_threads(1)

import pytest
from functools import wraps

def run_bench(benchmark, G, locs, nbit):
    with ProjectQContext(nbit, 'simulate') as cc:
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

def ising_hamiltonian(nbit):
    H1 = reduce(lambda x,y: x+y, [1/4. * ops.QubitOperator("Z%d Z%d"%(i, i+1)) for i in range(nbit-1)])
    H2 = reduce(lambda x,y: x+y, [1/4 * ops.QubitOperator("X%d"%(i, )) for i in range(nbit)])
    return H1 + H2

################### Tests #################
nbit_list = range(4,26)
@pytest.mark.parametrize('nbit', nbit_list)
def test_X(benchmark, nbit):
    benchmark.group = "X"
    run_bench(benchmark, ops.X, 2, nbit)

@pytest.mark.parametrize('nbit', nbit_list)
def test_H(benchmark, nbit):
    benchmark.group = "H"
    run_bench(benchmark, ops.H, 2, nbit)

@pytest.mark.parametrize('nbit', nbit_list)
def test_T(benchmark, nbit):
    benchmark.group = "T"
    run_bench(benchmark, ops.T, 2, nbit)

@pytest.mark.parametrize('nbit', nbit_list)
def test_CX(benchmark, nbit):
    benchmark.group = "CNOT"
    run_bench(benchmark, ops.CNOT, (2,3), nbit)

@pytest.mark.parametrize('nbit', nbit_list)
def test_CY(benchmark, nbit):
    benchmark.group = "C-Rx(0.5)"
    run_bench(benchmark, ops.C(ops.Rx(0.5)), (2,3), nbit)

@pytest.mark.parametrize('nbit', nbit_list)
def test_Toffoli(benchmark, nbit):
    benchmark.group = "Toffoli"
    run_bench(benchmark, ops.Toffoli, (2,3,0), nbit)

@pytest.mark.parametrize('nbit', nbit_list)
def test_Measure(benchmark, nbit):
    benchmark.group = "Measure"
    run_bench(benchmark, ops.All(ops.Measure), None, nbit)

@pytest.mark.parametrize('nbit', range(4,16))
def test_TimeEvolution(benchmark, nbit):
    benchmark.group = "TimeEvolution"
    run_bench(benchmark, ops.TimeEvolution(1.0, ising_hamiltonian(nbit)), None, nbit)
