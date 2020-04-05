#!/bin/sh

FILE_PATH=$(readlink -f "$0")
BASE_PATH=$(dirname "$FILE_PATH")

cd "$BASE_PATH"

if [ ! -d "ddsim" ]; then
    git clone https://github.com/iic-jku/ddsim ddsim
else
    git -C ddsim pull
fi
git -C ddsim submodule update --init --recursive


cmake -DGIT_SUBMODULE=OFF -DBENCHMARK_ENABLE_LTO=true -DCMAKE_BUILD_TYPE=Release -S ddsim -B build
cmake --build build --config Release --target ddsim_benchmark

