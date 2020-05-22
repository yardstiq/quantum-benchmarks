#!/bin/sh
BINDIR="$(dirname $0)"
source $BINDIR/utils/constants.sh
source $BINDIR/utils/colors.sh

JULIA_DOWNLOAD=$JULIA_PATH JULIA_INSTALL=$JULIA_PATH REPLY=Y bash -ci "$(curl -fsSL https://raw.githubusercontent.com/abelsiqueira/jill/master/jill.sh)"
