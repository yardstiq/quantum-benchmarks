#!/bin/bash

FILE_PATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
ROOT_PATH=`dirname $FILE_PATH`
BINDIR="$ROOT_PATH/bin"
. $BINDIR/utils/constants.sh

cd "$FILE_PATH"

if [ ! -d "ddsim" ]; then
    git clone --branch "v1.1" --depth 1  https://github.com/iic-jku/ddsim ddsim
    git -C ddsim submodule update --init --recursive
fi

# these options require cmake >= 3.13
cmake -DGIT_SUBMODULE=OFF -DBENCHMARK_ENABLE_LTO=true -DCMAKE_BUILD_TYPE=Release -S ddsim -B build 
cmake --build build --config Release --target ddsim_benchmark

