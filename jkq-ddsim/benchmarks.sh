#!/usr/bin/env bash

FILE_PATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
ROOT_PATH=$(dirname "$FILE_PATH")
. "$ROOT_PATH/bin/utils/constants.sh"

# env vars do not work https://github.com/google/benchmark/issues/913
#export BENCHMARK_OUT_FORMAT='csv'
#export BENCHMARK_OUT="$BENCHMARK_DATA_PATH/jku-ddsim.csv"

# to restrict the benchmarks to the single gate ones, use --benchmark_filter=BM_sim_[XHTC]
mkdir -p "$BENCHMARK_DATA_PATH"
build/apps/ddsim_benchmark --benchmark_filter=BM_sim_ --benchmark_out_format=json --benchmark_out="$BENCHMARK_DATA_PATH/jkq-ddsim.json" 

