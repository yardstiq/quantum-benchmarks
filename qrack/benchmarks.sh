#!/usr/bin/env bash

FILE_PATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
ROOT_PATH=$(dirname "$FILE_PATH")
. "$ROOT_PATH/bin/utils/constants.sh"

cd "${FILE_PATH}"

# to restrict the benchmarks to the single gate ones, use --benchmark_filter=BM_sim_[XHTC]
mkdir -p "$BENCHMARK_DATA_PATH"
./benchmarks --benchmark_filter=BM_sim_ --benchmark_out_format=json --benchmark_out="$BENCHMARK_DATA_PATH/qrack.json" 
