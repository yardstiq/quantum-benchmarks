import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df_cirq = pd.read_csv('cirq.csv')
df_qiskit = pd.read_csv('qiskit.csv')
df_yao = pd.read_csv('yao.csv')
df_projectq = pd.read_csv('projectq.csv')

df_qcbm = pd.read_csv('qcbm.csv')

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8), sharey=True)

l1 = ax1.semilogy(df_cirq["nqubits"], df_cirq["CirqX"], '-o', markersize=3)
l2 = ax1.semilogy(df_qiskit["nqubits"], df_qiskit["qiskitX"], '-o', markersize=3)
l3 = ax1.semilogy(df_projectq["nqubits"], df_projectq["X"], '-o', markersize=3)
l4 = ax1.semilogy(df_yao["nqubits"], df_yao["X"], '-o', markersize=3)
ax1.set(title="X gate", xlabel="nqubits", ylabel="ns")

ax2.semilogy(df_cirq["nqubits"], df_cirq["CirqH"], '-o', markersize=3)
ax2.semilogy(df_qiskit["nqubits"], df_qiskit["qiskitH"], '-o', markersize=3)
ax2.semilogy(df_projectq["nqubits"], df_projectq["H"], '-o', markersize=3)
ax2.semilogy(df_yao["nqubits"], df_yao["H"], '-o', markersize=3)
ax2.set(title="H gate", xlabel="nqubits", ylabel="ns")

ax3.semilogy(df_cirq["nqubits"], df_cirq["CirqCNOT"], '-o', markersize=3)
ax3.semilogy(df_qiskit["nqubits"], df_qiskit["qiskitCNOT"], '-o', markersize=3)
ax3.semilogy(df_projectq["nqubits"], df_projectq["CNOT"], '-o', markersize=3)
ax3.semilogy(df_yao["nqubits"], df_yao["CNOT"], '-o', markersize=3)
ax3.set(title="CNOT gate", xlabel="nqubits", ylabel="ns")

ax4.semilogy(df_cirq["nqubits"], df_cirq["CirqToffoli"], '-o', markersize=3)
ax4.semilogy(df_qiskit["nqubits"], df_qiskit["qiskitToffoli"], '-o', markersize=3)
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
plt.savefig('gates.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')

fig = plt.figure(figsize=(8, 6))
ax = plt.subplot(111)
l1 = ax.semilogy(df_qcbm["nqubits"], df_qcbm["cirq"], '-o', markersize=3)
l2 = ax.semilogy(df_qcbm["nqubits"], df_qcbm["qiskit"], '-o', markersize=3)
l3 = ax.semilogy(df_qcbm["nqubits"], df_qcbm["projectq"], '-o', markersize=3)
l4 = ax.semilogy(df_qcbm["nqubits"], df_qcbm["yao"], '-o', markersize=3)
ax.set(title="Parameterized Circuit", xlabel="nqubits", ylabel="ns")
lgd = ax.legend(
    [l1, l2, l3, l4],
    labels=["Cirq", "qiskit", "ProjectQ", "Yao"],
    loc="upper right",
    borderaxespad=0.1,
    bbox_to_anchor=(1.2, 0.9))
plt.savefig('qcbm.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
