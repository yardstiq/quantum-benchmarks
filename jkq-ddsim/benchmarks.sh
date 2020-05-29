#!/bin/sh

# FILE_PATH=$(readlink -f "$0")
# BASE_PATH=$(dirname "$FILE_PATH")

# BENCHMARK_DATA_PATH="$1"

# cd "$BASE_PATH"

# # env vars do not work https://github.com/google/benchmark/issues/913
# #export BENCHMARK_OUT_FORMAT='csv'
# #export BENCHMARK_OUT="$BENCHMARK_DATA_PATH/jku-ddsim.csv"

# # to restrict the benchmarks to the single gate ones, use --benchmark_filter=BM_sim_[XHTC]
# build/apps/ddsim_benchmark --benchmark_filter=BM_sim_ --benchmark_out_format=json --benchmark_out="$BENCHMARK_DATA_PATH/jkq-ddsim.json" 

echo "benchmarking jkq-ddsim..."
sleep 5
echo "finished $(basename $(dirname $0))"