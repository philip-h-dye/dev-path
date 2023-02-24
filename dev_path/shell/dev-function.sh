#!/bin/echo "*** must be sourced: . dev-funcion.sh"

# dev_path : Move, via pushd, to the first development path matching <pattern>.
#         * actually generates shell commands to do move
# 
# Alternatively, if an action is specified, perform it instead.
# 
# DEV_PATHS is typically '~/.dev-paths' but this may be controlled
# by setting DEV_PATHS to an alternate file name.
#
# installation:  python -m pip install dev_path
#
# usage:  dev --help

function dev() {
    eval "$( dev_path $@ )"
}
