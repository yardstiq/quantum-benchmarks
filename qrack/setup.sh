#!/bin/bash

FILE_PATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
ROOT_PATH=`dirname $FILE_PATH`
BINDIR="$ROOT_PATH/bin"
. $BINDIR/utils/constants.sh

cd "$FILE_PATH"

# Install Google Benchmark
# https://github.com/google/benchmark
rm -rf benchmark qrack
git clone https://github.com/google/benchmark.git

cmake -DBENCHMARK_DOWNLOAD_DEPENDENCIES=ON -DBENCHMARK_ENABLE_GTEST_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -S benchmark -B "build"
cmake --build "build" --config Release


git clone https://github.com/vm6502q/qrack.git
cd qrack
mkdir _build && cd _build && sudo cmake .. && sudo make all install -j$(nproc --all)
cd ${FILE_PATH}

g++ benchmarks.cc -std=c++11 -isystem benchmark/include -Lbuild/src -lbenchmark -lOpenCL -lpthread -lqrack -o benchmarks
