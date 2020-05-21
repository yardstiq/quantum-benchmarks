#!/bin/sh

FILE_PATH=$(readlink -f "$0")
BASE_PATH=$(dirname "$FILE_PATH")

cd "$BASE_PATH"

if [ ! -d "ddsim" ]; then
    git clone --branch "v1.0.1a" --depth 1  https://github.com/iic-jku/ddsim ddsim
    git -C ddsim submodule update --init --recursive
fi


cmake -DGIT_SUBMODULE=OFF -DBENCHMARK_ENABLE_LTO=true -DCMAKE_BUILD_TYPE=Release -S ddsim -B ddsim/build
cmake --build build --config Release --target ddsim_benchmark

