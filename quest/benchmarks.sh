#!/usr/bin/env bash

FILE_PATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
ROOT_PATH=$(dirname "$FILE_PATH")
. "$ROOT_PATH/bin/utils/constants.sh"

mkdir -p "$BENCHMARK_DATA_PATH"

#Clear CMAKE cache
rm -rf CMakeCache.txt CMakeFiles/ Makefile cmake_install.cmake

cmake -DUSER_SOURCE="benchmarks.cc" -DCMAKE_CXX_STANDARD_LIBRARIES="-lbenchmark -lpthread"  -DOUTPUT_EXE="benchmarks"   QuEST/
make

./benchmarks
