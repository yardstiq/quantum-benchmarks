import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import os
import json

def find_json(name):
    benchmark_path = os.path.join('.benchmarks', os.listdir('.benchmarks')[0])
    list = []
    for each in os.listdir(benchmark_path):
        if name in each:
            list.append(each)
    return os.path.join(benchmark_path, list[-1])

def wash_benchmark_data(name, labels):
    with open(find_json(name)) as f:
        data = json.load(f)

    cols = [each['params']['nqubits'] for each in data['benchmarks'] if each['group']==labels[0]]    
    dd = {}
    dd['nqubits'] = cols
    for lb in labels:
        dd[lb] = [each['stats']['min']*1e9
            for each in data['benchmarks'] if each['group']==lb]
    return pd.DataFrame(data=dd)

df_projectq = wash_benchmark_data('projectq', ['X', 'H', 'T', 'CNOT', 'Toffoli'])
df_qiskit = wash_benchmark_data('qiskit', ['X', 'H', 'T', 'CNOT', 'Toffoli'])
df_cirq = wash_benchmark_data('cirq', ['X', 'H', 'T', 'CNOT', 'Toffoli'])
df_yao = pd.read_csv('yao.csv')

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8), sharey=True)

l1 = ax1.semilogy(df_cirq["nqubits"], df_cirq["X"], '-o', markersize=3)
l2 = ax1.semilogy(df_qiskit["nqubits"], df_qiskit["X"], '-o', markersize=3)
l3 = ax1.semilogy(df_projectq["nqubits"], df_projectq["X"], '-o', markersize=3)
l4 = ax1.semilogy(df_yao["nqubits"], df_yao["X"], '-o', markersize=3)
ax1.set(title="X gate", xlabel="nqubits", ylabel="ns")

ax2.semilogy(df_cirq["nqubits"], df_cirq["H"], '-o', markersize=3)
ax2.semilogy(df_qiskit["nqubits"], df_qiskit["H"], '-o', markersize=3)
ax2.semilogy(df_projectq["nqubits"], df_projectq["H"], '-o', markersize=3)
ax2.semilogy(df_yao["nqubits"], df_yao["H"], '-o', markersize=3)
ax2.set(title="H gate", xlabel="nqubits", ylabel="ns")

ax3.semilogy(df_cirq["nqubits"], df_cirq["CNOT"], '-o', markersize=3)
ax3.semilogy(df_qiskit["nqubits"], df_qiskit["CNOT"], '-o', markersize=3)
ax3.semilogy(df_projectq["nqubits"], df_projectq["CNOT"], '-o', markersize=3)
ax3.semilogy(df_yao["nqubits"], df_yao["CNOT"], '-o', markersize=3)
ax3.set(title="CNOT gate", xlabel="nqubits", ylabel="ns")

ax4.semilogy(df_cirq["nqubits"], df_cirq["Toffoli"], '-o', markersize=3)
ax4.semilogy(df_qiskit["nqubits"], df_qiskit["Toffoli"], '-o', markersize=3)
ax4.semilogy(df_projectq["nqubits"], df_projectq["Toffoli"], '-o', markersize=3)
ax4.semilogy(df_yao["nqubits"], df_yao["Toffoli"], '-o', markersize=3)
ax4.set(title="Toffoli gate", xlabel="nqubits", ylabel="ns")

lgd = fig.legend(
    [l1, l2, l3, l4],
    labels=["Cirq", "qiskit", "ProjectQ", "Yao"],
    loc="upper right",
    borderaxespad=0.1,
    bbox_to_anchor=(1.09, 0.9))

plt.tight_layout()
plt.savefig('gates.png', bbox_extra_artists=(lgd,), bbox_inches='tight')

df_projectq = wash_benchmark_data('projectq', ['QCBM'])
df_qiskit = wash_benchmark_data('qiskit', ['QCBM'])
df_cirq = wash_benchmark_data('cirq', ['QCBM'])
df_yao = pd.read_csv('yao_qcbm.csv')
df_pennylane = wash_benchmark_data('pennylane', ['QCBM'])

fig = plt.figure(figsize=(8, 6))
ax = plt.subplot(111)
l1 = ax.semilogy(df_projectq["nqubits"], df_projectq["QCBM"], '-o', markersize=3)
l2 = ax.semilogy(df_qiskit["nqubits"], df_qiskit["QCBM"], '-o', markersize=3)
l3 = ax.semilogy(df_cirq["nqubits"], df_cirq["QCBM"], '-o', markersize=3)
l4 = ax.semilogy(df_yao["nqubits"], df_yao["QCBM"], '-o', markersize=3)
l5 = ax.semilogy(df_yao["nqubits"], df_yao["QCBM_cuda"], '-o', markersize=3)
l6 = ax.semilogy(df_pennylane['nqubits'], df_yao['QCBM'], '-o', markersize=3)

ax.set(title="Parameterized Circuit", xlabel="nqubits", ylabel="ns")
lgd = ax.legend(
    [l1, l2, l3, l4, l5, l6],
    labels=["ProjectQ", "qiskit", "Cirq", "Yao", "Yao (cuda)", "PennyLane (default)"],
    loc="upper right",
    borderaxespad=0.1,
    bbox_to_anchor=(1.2, 0.9))
plt.savefig('pcircuit.png', bbox_extra_artists=(lgd,), bbox_inches='tight')

df_yao = pd.read_csv('yao_qcbm_batch.csv')
fig = plt.figure(figsize=(8, 6))
ax = plt.subplot(111)
l1 = ax.semilogy(df_yao["nqubits"], df_yao["QCBM_batch"], '-o', markersize=3)
l2 = ax.semilogy(df_yao["nqubits"], df_yao["QCBM_cuda_batch"], '-o', markersize=3)
ax.set(title="Batched Parameterized Circuit", xlabel="nqubits", ylabel="ns")
lgd = ax.legend(
    [l1, l2],
    labels=["CPU", "CUDA"],
    loc="upper right",
    borderaxespad=0.1,
    bbox_to_anchor=(1.2, 0.9))
plt.savefig('pcircuit_batch.png', bbox_extra_artists=(lgd,), bbox_inches='tight')
