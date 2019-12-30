#!/bin/bash

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(greadlink -f $ARG0)
FILE_DIR=$(dirname $FILE_PATH)


main(){
    python -m unittest ohri.tool.tests.test_duckling_tool.TestDucklingTool.test_02
}

main
