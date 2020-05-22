#!/bin/bash
# constants
FILE_PATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
ROOT_PATH=$(dirname "$FILE_PATH")
BENCHMARK_DATA_PATH="$ROOT_PATH/data"
BENCHMARK_LOG_PATH="$ROOT_PATH/log"
CONDA_PATH=$ROOT_PATH/bin/conda
CONDA=$CONDA_PATH/bin/conda
ACTIVATE=$CONDA_PATH/bin/activate
JULIA_PATH=$ROOT_PATH/bin/julia
JULIA=$JULIA_PATH/bin/julia

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    NCORES=$(grep ^cpu\\scores /proc/cpuinfo | uniq |  awk '{print $4}')
elif [[ "$OSTYPE" == "darwin"* ]]; then
    NCORES=$(sysctl -n hw.physicalcpu)
else
    printf "${RED}system $OSTYPE not supported${NC}" >&2;
    exit 1;
fi
