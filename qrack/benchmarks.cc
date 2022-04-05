#include <benchmark/benchmark.h>
#include "qrack/qfactory.hpp"

#include <algorithm>
#include <iostream>

using namespace Qrack; 

// This suite is meant to test "ket" simulation performance specifically,
// but Qrack can sometimes do much better than this with its default optimal layer stack!
// Toggle the bool below to try both methods.
const bool isKet = true;
const auto SimType = isKet ? QINTERFACE_HYBRID : QINTERFACE_OPTIMAL_MULTI;

auto min_estimator = [](const std::vector<double>& v) -> double {return *(std::min_element(std::begin(v), std::end(v)));};

static void BM_sim_X(benchmark::State& state) {
	QInterfacePtr qReg = CreateQuantumInterface({ SimType }, state.range(0), 0);
	for (auto _ : state){
		qReg->X(state.range(0) - 1);
	}
	qReg->Finish();
	state.SetLabel("X");
}
// Register the function as a benchmark
BENCHMARK(BM_sim_X)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

static void BM_sim_H(benchmark::State& state) {
	QInterfacePtr qReg = CreateQuantumInterface({ SimType }, state.range(0), 0);
	for (auto _ : state){
		qReg->H(state.range(0) - 1);
	}
	qReg->Finish();
	state.SetLabel("H");
}
// Register the function as a benchmark
BENCHMARK(BM_sim_H)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

static void BM_sim_T(benchmark::State& state) {
	QInterfacePtr qReg = CreateQuantumInterface({ SimType }, state.range(0), 0);
	for (auto _ : state){
		qReg->T(state.range(0) - 1);
	}
	qReg->Finish();
	state.SetLabel("T");
}
// Register the function as a benchmark
BENCHMARK(BM_sim_T)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

static void BM_sim_CNOT(benchmark::State& state) {
	QInterfacePtr qReg = CreateQuantumInterface({ SimType }, state.range(0), 0);
	for (auto _ : state){
		qReg->CNOT(0,1);
	}
	qReg->Finish();
	state.SetLabel("CNOT");
}
// Register the function as a benchmark
BENCHMARK(BM_sim_CNOT)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

static void BM_sim_Toffoli(benchmark::State& state) {
	QInterfacePtr qReg = CreateQuantumInterface({ SimType }, state.range(0), 0);
	for (auto _ : state){
		qReg->CCNOT(0,1,2);
	}
	qReg->Finish();
	state.SetLabel("Toffoli");
}
// Register the function as a benchmark
BENCHMARK(BM_sim_Toffoli)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

static void BM_sim_Rx(benchmark::State& state) {
	QInterfacePtr qReg = CreateQuantumInterface({ SimType }, state.range(0), 0);
	for (auto _ : state){
		qReg->RX(0.5, 2);
	}
	qReg->Finish();
	state.SetLabel("Rx");
}
// Register the function as a benchmark
BENCHMARK(BM_sim_Rx)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

static void BM_sim_Ry(benchmark::State& state) {
	QInterfacePtr qReg = CreateQuantumInterface({ SimType }, state.range(0), 0);
	for (auto _ : state){
		qReg->RY(0.5, 2);
	}
	qReg->Finish();
	state.SetLabel("Ry");
}

// Register the function as a benchmark
BENCHMARK(BM_sim_Ry)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

float get_random() {
	// https://stackoverflow.com/questions/686353/random-float-number-generation
	static std::default_random_engine e;
	static std::uniform_real_distribution<> dis(0, 1); // rage 0 - 1
	return dis(e);
}

static void BM_sim_QCBM(benchmark::State& state) {
        QInterfacePtr qReg = CreateQuantumInterface({ SimType }, state.range(0), 0);
        for (auto _: state){

               // First rotation
               for (int i = 0; i < qReg->GetQubitCount(); i++) {
                       qReg->RX(get_random(), i);
                       qReg->RZ(get_random(), i);
               }

		// Entangler
               for (int i = 0; i < qReg->GetQubitCount(); i++) {
                       qReg->CNOT(i, (i+1) % qReg->GetQubitCount());
               }


		for (int depth = 0; depth < 9; depth++){
			// Mid Rotation
			for (int i = 0; i < qReg->GetQubitCount(); i++) {
			        qReg->RZ(get_random(), i);
                               qReg->RX(get_random(), i);
                               qReg->RZ(get_random(), i);
                       }

			// Entangler
                       for (int i = 0; i < qReg->GetQubitCount(); i++) {
                               qReg->CNOT(i, (i+1) % qReg->GetQubitCount());
			}
		}

		// Last Rotation
		for (int i = 0; i < qReg->GetQubitCount(); i++) {
                       qReg->RZ(get_random(), i);
                       qReg->RX(get_random(), i);
               }

	}
	qReg->Finish();
	state.SetLabel("QCBM");
}

BENCHMARK(BM_sim_QCBM)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

BENCHMARK_MAIN();
