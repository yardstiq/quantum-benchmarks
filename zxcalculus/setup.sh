#!/bin/bash
FILE_PATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
ROOT_PATH=`dirname $FILE_PATH`
BINDIR="$ROOT_PATH/bin"
. $BINDIR/utils/constants.sh

$JULIA --color=yes -e "using Pkg;Pkg.activate(@__DIR__);Pkg.instantiate(verbose=true);Pkg.precompile()"
