using JSON, DataFrames, CSV, Plots, JLD2

file = JSON.parsefile("cirq/.benchmarks/Darwin-CPython-3.7-64bit/0001_0246ecb3dfce8dae170ccdf222c115ce318fcdb9_20190702_184140_uncommited-changes.json")

qcbm_benchmark = Dict()
qcbm_benchmark["cirq"] = [each["stats"]["min"] * 1e9 for each in file["benchmarks"] if each["group"] == "QCBM"]

benchmarks_cirq = Dict()
benchmarks_cirq["X"] = [each["stats"]["min"] * 1e9 for each in file["benchmarks"] if each["group"] == "X"]
benchmarks_cirq["H"] = [each["stats"]["min"] * 1e9 for each in file["benchmarks"] if each["group"] == "H"]
benchmarks_cirq["T"] = [each["stats"]["min"] * 1e9 for each in file["benchmarks"] if each["group"] == "T"]
benchmarks_cirq["CNOT"] = [each["stats"]["min"] * 1e9 for each in file["benchmarks"] if each["group"] == "CNOT"]
benchmarks_cirq["Toffoli"] = [each["stats"]["min"] * 1e9 for each in file["benchmarks"] if each["group"] == "Toffoli"]

data = DataFrame(nqubits=4:25,
    CirqX=benchmarks_cirq["X"],
    CirqH=benchmarks_cirq["H"],
    CirqT=benchmarks_cirq["T"],
    CirqCNOT=benchmarks_cirq["CNOT"],
    CirqToffoli=benchmarks_cirq["Toffoli"])

CSV.write("cirq.csv", data)

file = JSON.parsefile("qiskit/.benchmarks/Darwin-CPython-3.7-64bit/0001_e5b779f8cec7ee91655814cb360026fad83667bd_20190703_201317_uncommited-changes.json")

qcbm_benchmark["qiskit"] = [each["stats"]["min"] * 1e9 for each in file["benchmarks"] if each["group"] == "QCBM"]

benchmarks_qiskit = Dict()
benchmarks_qiskit["X"] = [each["stats"]["min"] * 1e9 for each in file["benchmarks"] if each["group"] == "X"]
benchmarks_qiskit["H"] = [each["stats"]["min"] * 1e9 for each in file["benchmarks"] if each["group"] == "H"]
benchmarks_qiskit["T"] = [each["stats"]["min"] * 1e9 for each in file["benchmarks"] if each["group"] == "T"]
benchmarks_qiskit["CNOT"] = [each["stats"]["min"] * 1e9 for each in file["benchmarks"] if each["group"] == "CNOT"]
benchmarks_qiskit["Toffoli"] = [each["stats"]["min"] * 1e9 for each in file["benchmarks"] if each["group"] == "Toffoli"]

data = DataFrame(nqubits=4:17,
    qiskitX=benchmarks_qiskit["X"],
    qiskitH=benchmarks_qiskit["H"],
    qiskitT=benchmarks_qiskit["T"],
    qiskitCNOT=benchmarks_qiskit["CNOT"],
    qiskitToffoli=benchmarks_qiskit["Toffoli"])

CSV.write("qiskit.csv", data)

file = JSON.parsefile("projectq/.benchmarks/Darwin-CPython-3.7-64bit/0001_e5b779f8cec7ee91655814cb360026fad83667bd_20190703_230034_uncommited-changes.json")

benchmarks_projectq = Dict()
benchmarks_projectq["X"] = [each["stats"]["min"] * 1e9 for each in file["benchmarks"] if each["group"] == "X"]
benchmarks_projectq["H"] = [each["stats"]["min"] * 1e9 for each in file["benchmarks"] if each["group"] == "H"]
benchmarks_projectq["T"] = [each["stats"]["min"] * 1e9 for each in file["benchmarks"] if each["group"] == "T"]
benchmarks_projectq["CNOT"] = [each["stats"]["min"] * 1e9 for each in file["benchmarks"] if each["group"] == "CNOT"]
benchmarks_projectq["Toffoli"] = [each["stats"]["min"] * 1e9 for each in file["benchmarks"] if each["group"] == "Toffoli"]


data = DataFrame(nqubits=4:25,
X=benchmarks_projectq["X"],
H=benchmarks_projectq["H"],
T=benchmarks_projectq["T"],
CNOT=benchmarks_projectq["CNOT"],
Toffoli=benchmarks_projectq["Toffoli"])

CSV.write("projectq.csv", data)

@load "yao/shortlist.jld" benchmarks

benchmarks["X"]

benchmarks_yao = Dict()
benchmarks_yao["X"] = [each[2] for each in benchmarks["X"]]
benchmarks_yao["H"] = [each[2] for each in benchmarks["H"]]
benchmarks_yao["T"] = [each[2] for each in benchmarks["T"]]
benchmarks_yao["CNOT"] = [each[2] for each in benchmarks["CNOT"]]
benchmarks_yao["Toffoli"] = [each[2] for each in benchmarks["Toffoli"]]

data = DataFrame(nqubits=4:26,
X=benchmarks_yao["X"],
H=benchmarks_yao["H"],
T=benchmarks_yao["T"],
CNOT=benchmarks_yao["CNOT"],
Toffoli=benchmarks_yao["Toffoli"])

CSV.write("yao.csv", data)


file = JSON.parsefile("/Users/roger/.julia/dev/YaoBenchmarks/qcbm/0001_d8bf6f271550614cbf4e5f7f030cf145977f27d7_20190526_230620_uncommited-changes.json")
qcbm_benchmark["projectq"] = [each["stats"]["min"] * 1e9 for each in file["benchmarks"] if each["group"] == "qcbm"]

@load "/Users/roger/.julia/dev/YaoBenchmarks/qcbm.jld" qcbm

qcbm_benchmark["yao"] = qcbm

data = DataFrame(nqubits=4:14,
    yao=qcbm_benchmark["yao"][1:end-1],
    projectq=qcbm_benchmark["projectq"][1:end-1],
    cirq=qcbm_benchmark["cirq"],
    qiskit=qcbm_benchmark["qiskit"]
)

CSV.write("qcbm.csv", data)
