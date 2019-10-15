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
        time_data = [each['stats']['min']*1e9
            for each in data['benchmarks'] if each['group']==lb]
        if len(time_data) is not len(cols):
            time_data.append([float('inf') for _ in range(len(cols) - len(time_data) + 1)])

        dd[lb] = time_data
    return pd.DataFrame(data=dd)

gate_data = {}
gate_set = ['X', 'H', 'T', 'CNOT', 'Toffoli']
packages = ['projectq', 'qiskit', 'cirq', 'quest', 'yao']

for each_package in packages:
    if each_package == 'yao':
        gate_data['yao'] = pd.read_csv('yao.csv')
    else:
        gate_data[each_package] = wash_benchmark_data(each_package, gate_set)


def subplot_dataset(dataset, ax, gate):
    ls = [ax.semilogy(dataset[each]["nqubits"], dataset[each][gate], '-o', markersize=3) for each in packages]
    return ls

def subplot_gate(ax, gate):
    ls = subplot_dataset(gate_data, ax, gate)
    ax.set(title=' '.join([gate, 'gate']), xlabel="nqubits", ylabel="ns")
    return ls

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8), sharey=True)

ls = subplot_gate(ax1, 'X')
subplot_gate(ax2, 'H')
subplot_gate(ax3, 'CNOT')
subplot_gate(ax4, 'Toffoli')

lgd = fig.legend(
    ls,
    labels=packages,
    loc="upper right",
    borderaxespad=0.1,
    bbox_to_anchor=(1.09, 0.9))

plt.tight_layout()
plt.savefig('gates.png', bbox_extra_artists=(lgd,), bbox_inches='tight')

circuit_data = {}
for each_package in packages:
    if each_package == 'yao':
        circuit_data['yao'] = pd.read_csv('yao_qcbm.csv')
    elif each_package == 'qiskit':
        continue # skip qiskit, since not supported
    else:
        circuit_data[each_package] = wash_benchmark_data(each_package, ['QCBM'])

packages.append('pennylane')
circuit_data['pennylane'] = wash_benchmark_data('pennylane', ['QCBM'])
packages = [each for each in packages if each != 'qiskit']

fig = plt.figure(figsize=(8, 6))
ax = plt.subplot(111)
ls = subplot_dataset(circuit_data, ax, 'QCBM')

packages.append('yao (cuda)')
ls.append(ax.semilogy(circuit_data['yao']["nqubits"], circuit_data['yao']["QCBM_cuda"], '-o', markersize=3))
ax.set(title="Parameterized Circuit", xlabel="nqubits", ylabel="ns")

lgd = ax.legend(
    ls,
    labels=packages,
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
