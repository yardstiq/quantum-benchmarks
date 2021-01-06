#include <benchmark/benchmark.h>
#include <QuEST.h>
#include <iostream>
#include <random>

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
		rotateZ(qubits, state.range(0) - 1, 0.5);
		destroyQureg(qubits, env); 
	}
	destroyQuESTEnv(env);
	state.SetLabel("Rz");
}
BENCHMARK(BM_sim_Ry)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

float get_random() {
	// https://stackoverflow.com/questions/686353/random-float-number-generation
	static std::default_random_engine e;
	static std::uniform_real_distribution<> dis(0, 1); // rage 0 - 1
    	return dis(e);
}

static void BM_sim_QCBM(benchmark::State& state) {
  	// load QuEST
	QuESTEnv  env = createQuESTEnv();	
	for (auto _: state){
		Qureg qubits = createQureg(state.range(0), env);
		initZeroState(qubits);

		// First rotation
		for(int i=0; i<state.range(0); i++){
			rotateX(qubits, i, get_random());
			rotateZ(qubits, i, get_random());
		}

		// Entangler
		for(int i=0; i<state.range(0); i++){
			controlledNot(qubits, i, (i+1) % state.range(0));
		}


		for(int depth=0; depth<9; depth++){
			// Mid Rotation
			for(int i=0; i<state.range(0); i++){
				rotateZ(qubits, i, get_random());
				rotateX(qubits, i, get_random());
				rotateZ(qubits, i, get_random());
			}

			// Entangler
			for(int i=0; i<state.range(0); i++){
				controlledNot(qubits, i, (i+1) % state.range(0));
			}
		}

		// Last Rotation
		for(int i=0; i<state.range(0); i++){
			rotateZ(qubits, i, get_random());
			rotateX(qubits, i, get_random());
		}

		destroyQureg(qubits, env); 
	}
	destroyQuESTEnv(env);
	state.SetLabel("QCBM");
}
BENCHMARK(BM_sim_QCBM)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

Qureg qft_rotations(Qureg qubits, int n){
  const float  PI_F=3.14159265358979f;
	if(n==0){
		return qubits;
	}

	n -= 1;
	hadamard(qubits, n);
	for(int i=0; i<n; i++){
		controlledPhaseShift(qubits, i, n, PI_F/pow(2, n-i));
	}
	return qft_rotations(qubits, n);
}

Qureg swap_registers(Qureg qubits, int n){
  const float  PI_F=3.14159265358979f;
	for(int i = 0; i < n/2; i++){
		swapGate(qubits, i, n - i - 1);
	}
	return qubits;
}

static void BM_sim_QFT(benchmark::State& state) {
  	// load QuEST
	QuESTEnv  env = createQuESTEnv();	
	for (auto _: state){
		Qureg qubits = createQureg(state.range(0), env);
		initZeroState(qubits);

		// Reference: https://qiskit.org/textbook/ch-algorithms/quantum-fourier-transform.html
		qubits = qft_rotations(qubits, state.range(0));
		qubits = swap_registers(qubits, state.range(0));			

		destroyQureg(qubits, env); 
	}
	destroyQuESTEnv(env);
	state.SetLabel("QFT");
}
BENCHMARK(BM_sim_QFT)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);




BENCHMARK_MAIN();
