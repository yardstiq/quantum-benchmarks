#!/usr/bin/env bash

FILE_PATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
ROOT_PATH=$(dirname "$FILE_PATH")
. "$ROOT_PATH/bin/utils/constants.sh"

pwd
mkdir -p "$BENCHMARK_DATA_PATH"
echo "$BENCHMARK_DATA_PATH"
echo "$FILE_PATH"
#Clear CMAKE cache
rm -rf CMakeCache.txt CMakeFiles/ Makefile cmake_install.cmake benchmarks

cmake -DUSER_SOURCE="benchmarks.cc" -DCMAKE_CXX_STANDARD_LIBRARIES="-lbenchmark -lpthread"  -DOUTPUT_EXE="benchmarks"   QuEST/
make

./benchmarks --benchmark_out=${BENCHMARK_DATA_PATH}/quest.json --benchmark_out_format=json --benchmark_filter=BM_sim_QFT
