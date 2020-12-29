#include <benchmark/benchmark.h>
#include <QuEST.h>
#include <iostream>

auto min_estimator = [](const std::vector<double>& v) -> double {return *(std::min_element(std::begin(v), std::end(v)));};

static void BM_sim_X(benchmark::State& state) {
  	// load QuEST
	QuESTEnv  env = createQuESTEnv();	
	for (auto _: state){
		Qureg qubits = createQureg(state.range(0), env);
		initZeroState(qubits);
		pauliX(qubits, state.range(0) - 1);
		destroyQureg(qubits, env); 
	}
	destroyQuESTEnv(env);
	state.SetLabel("X");
}
BENCHMARK(BM_sim_X)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

static void BM_sim_Hadamard(benchmark::State& state) {
  	// load QuEST
	QuESTEnv  env = createQuESTEnv();	
	for (auto _: state){
		Qureg qubits = createQureg(state.range(0), env);
		initZeroState(qubits);
		hadamard(qubits, state.range(0) - 1);
		destroyQureg(qubits, env); 
	}
	destroyQuESTEnv(env);
	state.SetLabel("hadamard");
}
BENCHMARK(BM_sim_Hadamard)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

static void BM_sim_T(benchmark::State& state) {
  	// load QuEST
	QuESTEnv  env = createQuESTEnv();	
	for (auto _: state){
		Qureg qubits = createQureg(state.range(0), env);
		initZeroState(qubits);
		tGate(qubits, state.range(0) - 1);
		destroyQureg(qubits, env); 
	}
	destroyQuESTEnv(env);
	state.SetLabel("T");
}
BENCHMARK(BM_sim_T)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

static void BM_sim_CNOT(benchmark::State& state) {
  	// load QuEST
	QuESTEnv  env = createQuESTEnv();	
	for (auto _: state){
		Qureg qubits = createQureg(state.range(0), env);
		initZeroState(qubits);
		controlledNot(qubits, 0, state.range(0) - 1);
		destroyQureg(qubits, env); 
	}
	destroyQuESTEnv(env);
	state.SetLabel("CNOT");
}
BENCHMARK(BM_sim_CNOT)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

static void BM_sim_Toffoli(benchmark::State& state) {
  	// load QuEST
	QuESTEnv  env = createQuESTEnv();
	ComplexMatrix2 u = {
		.real = {{0, 1},{1, 0}},
		.imag = {{0, 0},{0, 0}}
	};	
	int targetQubits[2];
	targetQubits[0] = 0;
	targetQubits[1] = 1;
	for (auto _: state){
		Qureg qubits = createQureg(state.range(0), env);
		initZeroState(qubits);
		multiControlledUnitary(qubits, targetQubits, 2, state.range(0) - 1, u);
		destroyQureg(qubits, env); 
	}
	destroyQuESTEnv(env);
	state.SetLabel("CNOT");
}
BENCHMARK(BM_sim_Toffoli)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

static void BM_sim_Rx(benchmark::State& state) {
  	// load QuEST
	QuESTEnv  env = createQuESTEnv();	
	for (auto _: state){
		Qureg qubits = createQureg(state.range(0), env);
		initZeroState(qubits);
		rotateX(qubits, state.range(0) - 1, 0.5);
		destroyQureg(qubits, env); 
	}
	destroyQuESTEnv(env);
	state.SetLabel("Rx");
}
BENCHMARK(BM_sim_Rx)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

static void BM_sim_Ry(benchmark::State& state) {
  	// load QuEST
	QuESTEnv  env = createQuESTEnv();	
	for (auto _: state){
		Qureg qubits = createQureg(state.range(0), env);
		initZeroState(qubits);
		rotateY(qubits, state.range(0) - 1, 0.5);
		destroyQureg(qubits, env); 
	}
	destroyQuESTEnv(env);
	state.SetLabel("Ry");
}
BENCHMARK(BM_sim_Ry)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

static void BM_sim_Rz(benchmark::State& state) {
  	// load QuEST
	QuESTEnv  env = createQuESTEnv();	
	for (auto _: state){
		Qureg qubits = createQureg(state.range(0), env);
		initZeroState(qubits);
		rotateY(qubits, state.range(0) - 1, 0.5);
		destroyQureg(qubits, env); 
	}
	destroyQuESTEnv(env);
	state.SetLabel("Rz");
}
BENCHMARK(BM_sim_Ry)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

BENCHMARK_MAIN();
