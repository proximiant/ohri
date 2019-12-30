#!/bin/bash -eu

FILE_PATH=$(readlink -f $0)
FILE_NAME=$(basename $FILE_PATH)
FILE_DIR=$(dirname $FILE_PATH)
# FILE_DIR=`pwd`/../scripts/test
SCRIPTS_DIR=$FILE_DIR

errcho(){ >&2 echo $@; }
func_count2reduce(){
    local v="${1?missing}"; local cmd="${2?missing}"; local n=${3?missing};
    for ((i=0;i<$n;i++)); do v=$($cmd $v) ; done; echo "$v"
}

REPO_DIR=$(func_count2reduce $FILE_DIR dirname 1)
LINC_DIR=$(dirname $REPO_DIR)
COMMONUTILS_DIR=${COMMONUTILS_DIR:-"$LINC_DIR/common-utils"}

main(){
    pushd $REPO_DIR
    export PYTHONPATH=$COMMONUTILS_DIR
    python -m scripts.test
    popd
}

errcho "[$FILE_NAME] START"
main
errcho "[$FILE_NAME] END"
