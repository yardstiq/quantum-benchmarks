import os
from utils import BenchmarkReport, JuliaProject, PythonProject, image_path
from utils.project import Plot
import matplotlib
import matplotlib.pyplot as plt

COLOR = {
    'yao': 'tab:red',
    'yao (cuda)': 'tab:orange',
    'yao x 1000': 'tab:blue',
    'yao x 64': 'tab:blue',
    'qiskit': 'tab:green',
    'qiskit (cuda)': 'tab:gray',
    'projectq': 'tab:blue',
    'cirq': 'tab:cyan',
    'quest': 'tab:olive',
    'qulacs': 'tab:brown',
    'qulacs (cuda)': 'tab:pink',
    'pennylane': 'tab:purple',
    'jkq-ddsim': 'darkblue'
}

projects = [
    JuliaProject('yao'),
    PythonProject('qiskit'),
    PythonProject('cirq'),
    PythonProject('projectq'),
    PythonProject('pennylane'),
    PythonProject('quest', 'pyquest-cffi'),
    PythonProject('qulacs'),
]

# Single Gate Benchmark Report
labels = ['X', 'H', 'CNOT', 'T']
report = BenchmarkReport(
    projects,
    layout = {l + ' gate' : [l] for l in labels},
    colors = {
        projects[0] : {l: COLOR['yao'] for l in labels},
        projects[1] : {l: COLOR['qiskit'] for l in labels},
        projects[2] : {l: COLOR['cirq'] for l in labels},
        projects[3] : {l: COLOR['projectq'] for l in labels},
        projects[4] : {l: COLOR['pennylane'] for l in labels},
        projects[5] : {l: COLOR['quest'] for l in labels},
        projects[6] : {l: COLOR['qulacs'] for l in labels},
    },
)

fig, ax = plt.subplots(2, 2, figsize=(10, 8))
plots = report.plot_absolute(ax)
plt.tight_layout()
plt.subplots_adjust(top=0.85)
lgd = fig.legend(
    plots[0].lines,
    labels=report.project_names(),
    loc="upper center",
    ncol=4,
    frameon=False,
    prop={'size': 15},
    borderaxespad=-0.4,
    bbox_to_anchor=(0.5, 0.97)
)

plt.savefig(image_path('gate.png'), bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.savefig(image_path('gate.pdf'), bbox_extra_artists=(lgd,), bbox_inches='tight')

fig, ax = plt.subplots(2, 2, figsize=(10, 8))
plots = report.plot_relative(projects[0], ax)
plt.tight_layout()
plt.subplots_adjust(top=0.85)
lgd = fig.legend(
    plots[0].lines,
    labels=report.project_names(),
    loc="upper center",
    ncol=4,
    frameon=False,
    prop={'size': 15},
    borderaxespad=-0.4,
    bbox_to_anchor=(0.5, 0.97))

plt.savefig(image_path('gates_relative.png'), bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.savefig(image_path('gates_relative.pdf'), bbox_extra_artists=(lgd,), bbox_inches='tight')


# Parameterized Circuit Benchmark Report
labels = ['QCBM', 'QCBM (cuda)']
colors = {
        projects[0] : {
            'QCBM': COLOR['yao'],
            'QCBM (cuda)': COLOR['yao (cuda)']
        },
        projects[1] : {
            'QCBM': COLOR['qiskit'],
            'QCBM (cuda)': COLOR['qiskit (cuda)'],
        },
        projects[2] : {'QCBM': COLOR['cirq']},
        projects[3] : {'QCBM': COLOR['projectq']},
        projects[4] : {'QCBM': COLOR['pennylane']},
        projects[5] : {'QCBM': COLOR['quest']},
        projects[6] : {
            'QCBM': COLOR['qulacs'],
            'QCBM (cuda)': COLOR['qulacs (cuda)'],
        },
}

report = BenchmarkReport(
    projects,
    layout = {
        'Parameterized Circuit Benchmark' : labels,
    },
    colors = colors,
)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), sharey=False)
plots = report.plot_absolute(ax1)
labels = []
for each in plots[0]._lines:
    for (k, l) in enumerate(plots[0]._lines[each]):
        labels.append(each.name + plots[0].labels[k][4:])

lgd1 = plots[0].ax.legend(
    plots[0].lines,
    labels=labels,
    loc='upper left', ncol=2
)

yao_project = projects[0]
ax2.set_title('Batched Parameterized Circuit Benchmark')
yao_project.update_table(['QCBM', 'QCBM (batch)', 'QCBM (batch) (cuda)'])
d = yao_project.table['QCBM']
ax2.semilogy(d["nqubits"], d["times"], '-o', markersize=4, color=COLOR['yao x 1000'])
d = yao_project.table['QCBM (batch)']
ax2.semilogy(d["nqubits"], d["times"], '-o', markersize=4, color=COLOR['yao'])
d = yao_project.table['QCBM (batch) (cuda)']
ax2.semilogy(d["nqubits"], d["times"], '-o', markersize=4, color=COLOR['yao (cuda)'])

lgd2 = ax2.legend(['yao x 1000', 'yao', 'yao (cuda)'], loc='upper left', ncol=1)

plt.tight_layout()
plt.savefig(image_path('pcircuit.png'), bbox_extra_artists=(lgd1, lgd2), bbox_inches='tight')
plt.savefig(image_path('pcircuit.pdf'), bbox_extra_artists=(lgd1, lgd2), bbox_inches='tight')
