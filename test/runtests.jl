using Test
using QuantumBenchmarks
using Comonicon.PATH

ncores()

scan_projects(PATH.project(QuantumBenchmarks, "test"))

path = PATH.project(QuantumBenchmarks, "test", "fake")
read_version(path)

execute(path)
setup_project(path)
