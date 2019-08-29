#!/usr/bin/env python
"""
This module runs basic Quil text files against the Forest QVM API.
"""

from __future__ import print_function
from pyquil.quil import Program
from pyquil.api import WavefunctionSimulator

def quil_run(prog):
    wf_sim = WavefunctionSimulator()
    print("Running Quil Program:\n", prog)
    print("---------------------------")
    print("Output: ")
    wf = wf_sim.wavefunction(Program(prog))
    print(wf.amplitudes)

if __name__ == '__main__':
    quil_run("H 0\nCNOT 0 1")
