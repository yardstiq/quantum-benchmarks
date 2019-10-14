#!/usr/bin/env python
import numpy as np
from projectq import MainEngine
from projectq import ops
from projectq.ops import *

import mkl
mkl.set_num_threads(1)

import pytest

def run_bench(benchmark, G, locs, nqubits):
    eng = MainEngine()
    reg = eng.allocate_qureg(nqubits)
    G | take_locs(reg, locs)
    benchmark(eng.flush)

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

def first_rotation(reg, nqubits):
    for k in range(nqubits):
        Rx(np.random.rand()) | reg[k]
        Rz(np.random.rand()) | reg[k]

def mid_rotation(reg, nqubits):
    for k in range(nqubits):
        Rz(np.random.rand()) | reg[k]
        Rx(np.random.rand()) | reg[k]
        Rz(np.random.rand()) | reg[k]

def last_rotation(reg, nqubits):
    for k in range(nqubits):
        Rz(np.random.rand()) | reg[k]
        Rx(np.random.rand()) | reg[k]

def entangler(reg, pairs):
    for a, b in pairs:
        CNOT | (reg[a], reg[b])


def execute_qcbm(reg, n, depth, pairs):
    first_rotation(reg, n)
    entangler(reg, pairs)
    for k in range(depth-1):
        mid_rotation(reg, n)
        entangler(reg, pairs)

    last_rotation(reg, n)


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
    run_bench(benchmark, ops.CNOT, (2, 3), nqubits)

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_CY(benchmark, nqubits):
    benchmark.group = "C-Rx(0.5)"
    run_bench(benchmark, ops.C(ops.Rx(0.5)), (2, 3), nqubits)

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_Toffoli(benchmark, nqubits):
    benchmark.group = "Toffoli"
    run_bench(benchmark, ops.Toffoli, (2, 3, 0), nqubits)

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_Measure(benchmark, nqubits):
    benchmark.group = "Measure"
    run_bench(benchmark, ops.All(ops.Measure), None, nqubits)

@pytest.mark.parametrize('nqubits', nqubits_list)
def test_qcbm(benchmark, nqubits):
    pairs = [(i, (i + 1) % nqubits) for i in range(nqubits)]
    benchmark.group = "QCBM"
    eng = MainEngine()
    reg = eng.allocate_qureg(nqubits)
    execute_qcbm(reg, nqubits, 9, pairs)
    benchmark(eng.flush)
