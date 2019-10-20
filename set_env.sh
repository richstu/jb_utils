#!/bin/bash
export JB_UTILS_DIR=$(dirname $(readlink -e "$BASH_SOURCE"))
export PYTHONPATH=$JB_UTILS_DIR/libs:$PYTHONPATH
