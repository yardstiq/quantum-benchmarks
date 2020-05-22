#!/bin/bash
FILE_PATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
ROOT_PATH=`dirname $FILE_PATH`
BINDIR="$ROOT_PATH/bin"
. $BINDIR/utils/constants.sh

source activate ./env
pytest benchmarks.py --benchmark-storage="file://data" --benchmark-sort=name --benchmark-min-rounds=5 \
        > "log.out" 2> "log.err"
