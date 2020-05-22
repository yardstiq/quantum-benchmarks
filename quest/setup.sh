#!/bin/bash
FILE_PATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
ROOT_PATH=`dirname $FILE_PATH`
CONDA="$ROOT_PATH/bin/conda/bin/conda"

if ![ -d "$CONDA" ]; then
    sh "$ROOT_PATH/bin/install_conda.sh"
fi

$CONDA create -y --prefix=env python=3.8
$CONDA activate ./env
$CONDA install -p env -y numpy mkl-service pytest pybind11 pytest-benchmark cffi
./env/bin/pip install pyquest-cffi
