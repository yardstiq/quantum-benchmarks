#!/bin/bash
BINDIR="$(dirname $0)"
. $BINDIR/utils/constants.sh
. $BINDIR/utils/colors.sh

version="1.5"
ARCH=`uname -m`

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    SYS="linux"
else
    printf "${RED}system $OSTYPE not supported${NC}" >&2;
    exit 1;
fi

URL="https://julialang-s3.julialang.org/bin/linux/x64/$version/julia-$version-latest-linux-x86_64.tar.gz"

function install_julia_linux() {
  echo "Downloading Julia version $version"
  if [ ! -f julia-$version.tar.gz ]; then
    curl -L -o $BINDIR/julia-$version.tar.gz $URL
  else
    echo "already downloaded"
  fi
  if [ ! -d julia-$version ]; then
    mkdir -p $JULIA_PATH
    tar zxf $BINDIR/julia-$version.tar.gz -C $JULIA_PATH --strip-components 1
  fi
}

install_julia_linux
