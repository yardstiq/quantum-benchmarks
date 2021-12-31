#include <benchmark/benchmark.h>
#include "qrack/qfactory.hpp"

#include <algorithm>
#include <iostream>

using namespace Qrack; 

auto min_estimator = [](const std::vector<double>& v) -> double {return *(std::min_element(std::begin(v), std::end(v)));};

static void BM_sim_X(benchmark::State& state) {
	QInterfacePtr qReg = CreateQuantumInterface({ QINTERFACE_HYBRID }, state.range(0), 0); 
	for (auto _ : state){
		qReg->X(state.range(0) - 1);
	}
	qReg->Finish();
	state.SetLabel("X");
}
// Register the function as a benchmark
BENCHMARK(BM_sim_X)->DenseRange(4,25); //->ComputeStatistics("min", min_estimator);

static void BM_sim_H(benchmark::State& state) {
	QInterfacePtr qReg = CreateQuantumInterface({ QINTERFACE_HYBRID }, state.range(0), 0);
	for (auto _ : state){
		qReg->H(state.range(0) - 1);
	}
	qReg->Finish();
	state.SetLabel("H");
}
// Register the function as a benchmark
BENCHMARK(BM_sim_H)->DenseRange(4,25); //->ComputeStatistics("min", min_estimator);

static void BM_sim_T(benchmark::State& state) {
	QInterfacePtr qReg = CreateQuantumInterface({ QINTERFACE_HYBRID }, state.range(0), 0);
	for (auto _ : state){
		qReg->T(state.range(0) - 1);
	}
	qReg->Finish();
	state.SetLabel("T");
}
// Register the function as a benchmark
BENCHMARK(BM_sim_T)->DenseRange(4,25); //->ComputeStatistics("min", min_estimator);

static void BM_sim_CNOT(benchmark::State& state) {
	QInterfacePtr qReg = CreateQuantumInterface({ QINTERFACE_HYBRID }, state.range(0), 0);
	for (auto _ : state){
		qReg->CNOT(0,1);
	}
	qReg->Finish();
	state.SetLabel("CNOT");
}
// Register the function as a benchmark
BENCHMARK(BM_sim_CNOT)->DenseRange(4,25); //->ComputeStatistics("min", min_estimator);

static void BM_sim_Toffoli(benchmark::State& state) {
	QInterfacePtr qReg = CreateQuantumInterface({ QINTERFACE_HYBRID }, state.range(0), 0);
	for (auto _ : state){
		qReg->CCNOT(0,1,2);
	}
	qReg->Finish();
	state.SetLabel("Toffoli");
}
// Register the function as a benchmark
BENCHMARK(BM_sim_Toffoli)->DenseRange(4,25); //->ComputeStatistics("min", min_estimator);

static void BM_sim_Rx(benchmark::State& state) {
	QInterfacePtr qReg = CreateQuantumInterface({ QINTERFACE_HYBRID }, state.range(0), 0);
	for (auto _ : state){
		qReg->RX(0.5, 2);
	}
	qReg->Finish();
	state.SetLabel("Rx");
}
// Register the function as a benchmark
BENCHMARK(BM_sim_Rx)->DenseRange(4,25); //->ComputeStatistics("min", min_estimator);

static void BM_sim_Ry(benchmark::State& state) {
	QInterfacePtr qReg = CreateQuantumInterface({ QINTERFACE_HYBRID }, state.range(0), 0);
	for (auto _ : state){
		qReg->RY(0.5, 2);
	}
	qReg->Finish();
	state.SetLabel("Ry");
}
// Register the function as a benchmark
BENCHMARK(BM_sim_Ry)->DenseRange(4,25); //->ComputeStatistics("min", min_estimator);

BENCHMARK_MAIN();
