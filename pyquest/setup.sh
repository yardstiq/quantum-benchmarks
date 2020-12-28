#!/bin/bash
FILE_PATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
ROOT_PATH=`dirname $FILE_PATH`
BINDIR="$ROOT_PATH/bin"
. $BINDIR/utils/constants.sh

$CONDA create -y --prefix=env python=3.8
$ACTIVATE ./env
$CONDA install -p env -y numpy mkl-service pytest pybind11 pytest-benchmark cffi
./env/bin/pip install pyquest-cffi
