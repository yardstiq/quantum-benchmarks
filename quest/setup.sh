#!/bin/bash

FILE_PATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
ROOT_PATH=`dirname $FILE_PATH`
BINDIR="$ROOT_PATH/bin"
. $BINDIR/utils/constants.sh

cd "$FILE_PATH"

rm -rf benchmark QuEST

ls

if [ ! -d "QuEST" ]; then
    git clone https://github.com/QuEST-Kit/QuEST.git
fi

git clone https://github.com/google/benchmark.git
cd benchmark
cmake -DBENCHMARK_DOWNLOAD_DEPENDENCIES=ON -DBENCHMARK_ENABLE_GTEST_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -S benchmark -B "build"
cmake --build "build" --config Release
sudo cmake --build "build" --config Release --target install
