#include <benchmark/benchmark.h>
#include "qrack/qfactory.hpp"

#include <algorithm>
#include <iostream>

using namespace Qrack; 

auto min_estimator = [](const std::vector<double>& v) -> double {return *(std::min_element(std::begin(v), std::end(v)));};

static void BM_sim_X(benchmark::State& state) {
	QInterfacePtr qReg = CreateQuantumInterface(QINTERFACE_QUNIT, QINTERFACE_OPTIMAL, state.range(0), 0);
	qReg->X(state.range(0) - 1);

	for (auto _ : state){
		qReg->M(state.range(0) - 1);
	}
	state.SetLabel("X");
}
// Register the function as a benchmark
BENCHMARK(BM_sim_X)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

static void BM_sim_H(benchmark::State& state) {
	QInterfacePtr qReg = CreateQuantumInterface(QINTERFACE_QUNIT, QINTERFACE_OPTIMAL, state.range(0), 0);
	qReg->H(state.range(0) - 1);

	for (auto _ : state){
		qReg->M(state.range(0) - 1);
	}
	state.SetLabel("H");
}
// Register the function as a benchmark
BENCHMARK(BM_sim_H)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

static void BM_sim_T(benchmark::State& state) {
	QInterfacePtr qReg = CreateQuantumInterface(QINTERFACE_QUNIT, QINTERFACE_OPTIMAL, state.range(0), 0);
	qReg->T(state.range(0) - 1);

	for (auto _ : state){
		qReg->M(state.range(0) - 1);
	}
	state.SetLabel("T");
}
// Register the function as a benchmark
BENCHMARK(BM_sim_T)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

static void BM_sim_CNOT(benchmark::State& state) {
	QInterfacePtr qReg = CreateQuantumInterface(QINTERFACE_QUNIT, QINTERFACE_OPTIMAL, state.range(0), 0);
	qReg->CNOT(0,1);

	for (auto _ : state){
		qReg->M(1);
	}
	state.SetLabel("CNOT");
}
// Register the function as a benchmark
BENCHMARK(BM_sim_CNOT)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

static void BM_sim_Toffoli(benchmark::State& state) {
	QInterfacePtr qReg = CreateQuantumInterface(QINTERFACE_QUNIT, QINTERFACE_OPTIMAL, state.range(0), 0);
	qReg->CCNOT(0,1,2);

	for (auto _ : state){
		qReg->M(1);
	}
	state.SetLabel("Toffoli");
}
// Register the function as a benchmark
BENCHMARK(BM_sim_Toffoli)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

static void BM_sim_Rx(benchmark::State& state) {
	QInterfacePtr qReg = CreateQuantumInterface(QINTERFACE_QUNIT, QINTERFACE_OPTIMAL, state.range(0), 0);
	qReg->RX(0.5, 2);

	for (auto _ : state){
		qReg->M(2);
	}
	state.SetLabel("Rx");
}
// Register the function as a benchmark
BENCHMARK(BM_sim_Rx)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

static void BM_sim_Ry(benchmark::State& state) {
	QInterfacePtr qReg = CreateQuantumInterface(QINTERFACE_QUNIT, QINTERFACE_OPTIMAL, state.range(0), 0);
	qReg->RY(0.5, 2);

	for (auto _ : state){
		qReg->M(2);
	}
	state.SetLabel("Ry");
}
// Register the function as a benchmark
BENCHMARK(BM_sim_Ry)->DenseRange(4,25)->ComputeStatistics("min", min_estimator);

BENCHMARK_MAIN();
