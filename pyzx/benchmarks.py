import random, math, os, time
import pyzx as zx

def run_benchmark():
    dir = 'circuits/'
    filenames = os.listdir(dir)
    bms = dict()
    for circ_name in filenames:
        circ_path = dir + circ_name
        c = zx.Circuit.load(circ_path).to_basic_gates()
        g = c.to_graph()
        t0 = time.time()
        g = zx.simplify.teleport_reduce(g)
        t1 = time.time()
        t = t1 - t0
        tc = zx.tcount(g)
        print(circ_name + '\t time =', t, '\t tcount =', tc)
        bms[circ_name] = t
    return bms

print('Benchmarking PyZX...')
bms = run_benchmark()
