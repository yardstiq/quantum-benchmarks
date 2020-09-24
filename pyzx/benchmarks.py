import random, math, os, time
import pyzx as zx
import pytest

dir = 'circuits/'
filenames = os.listdir(dir)
filenames.sort()

def run_phase_teleportation(benchmark, circ_name):
    circ_path = dir + circ_name
    c = zx.Circuit.load(circ_path).to_basic_gates()
    g = c.to_graph()
    benchmark(zx.simplify.teleport_reduce, g)

@pytest.mark.parametrize('circ_name', filenames)
def test_PyZX(benchmark, circ_name):
    benchmark.group = circ_name
    run_phase_teleportation(benchmark, circ_name)
