#!/bin/sh

FILE_PATH=$(readlink -f "$0")
BASE_PATH=$(dirname "$FILE_PATH")

BENCHMARK_LOG_PATH="$1"
BENCHMARK_DATA_PATH="$2"

cd "$BASE_PATH"

# env vars do not work https://github.com/google/benchmark/issues/913
#export BENCHMARK_OUT_FORMAT='csv'
#export BENCHMARK_OUT="$BENCHMARK_DATA_PATH/jku-ddsim.csv"


build/apps/ddsim_benchmark --benchmark_filter=BIM_sim_ --benchmark_out_format=json --benchmark_out="$BENCHMARK_DATA_PATH/jkq-ddsim.json" 
