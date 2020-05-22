#!/bin/bash
BINDIR="$(dirname $0)"
. $BINDIR/utils/constants.sh
. $BINDIR/utils/colors.sh

version="1.4"
ARCH=`uname -m`

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    SYS="linux"
else
    printf "${RED}system $OSTYPE not supported${NC}" >&2;
    exit 1;
fi

URL="https://julialang-s3.julialang.org/bin/linux/x64/$version/julia-$version-latest-linux-x86_64.tar.gz"

function install_julia_linux() {
  mkdir -p $JULIA_PATH
  cd $JULIA_PATH

  echo "Downloading Julia version $version"
  if [ ! -f julia-$version.tar.gz ]; then
    curl -L -o julia-$version.tar.gz $URL
  else
    echo "already downloaded"
  fi
  if [ ! -d julia-$version ]; then
    mkdir -p julia-$version
    tar zxf julia-$version.tar.gz -C julia-$version --strip-components 1
  fi

  major=${version:0:3}
  rm -f $JULIA_PATH/julia{,-$major,-$version}
  julia=$PWD/julia-$version/bin/julia
  ln -s $julia $JULIA_PATH/julia
  ln -s $julia $JULIA_PATH/julia-$major
  ln -s $julia $JULIA_PATH/julia-$version
}

unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*) install_julia_linux ;;
    *)
        echo "Unsupported platform $(unameOut)" >&2
        exit 1
        ;;
esac
