#!/usr/bin/env bash

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(greadlink -f $ARG0)
FILE_DIR=$(dirname $FILE_PATH)

errcho(){ >&2 echo $@; }
func_count2reduce(){
    local v="${1?missing}"; local cmd="${2?missing}"; local n=${3?missing};
    for ((i=0;i<$n;i++)); do v=$($cmd $v) ; done; echo "$v"
}

REPO_DIR=$(func_count2reduce $FILE_DIR dirname 1)

main(){
    jupyter notebook --notebook-dir=$REPO_DIR $REPO_DIR/ohri/tool/duckling/tests/test.ipynb
}

main