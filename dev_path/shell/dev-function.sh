#!/bin/echo "*** must be sourced: . dev-funcion.sh"

# dev_path : Move, via pushd, to the first development path matching <pattern>.
#
# Generates shell commands to do move
#
# Alternatively, if an action is specified, perform it instead.
#
# installation:  python -m pip install --user .
#
# usage:  dev --help
#
# docopt.ParsedOptions({
#     '--show': False,
#  a  '--regex': False,
#  a  '--glob': False,
#     '--help': False,
#     '--version': False,
#     '--debug': True,
#  a  '<pattern>': 'logtool',
#     '--display': None,
#     '--append': False,
#  a  '<path>': None,
#     '--insert': False,
#     '--set': False,
#     'display': False,
#     'show': False,
#     'append': False,
#     'add': False,
#     'insert': False,
#     'wedge': False,
#     '--delete': False,
#     'delete': False,
#     'remove': False,
#     'set': False,
#     'assign': False
# })

# dev [options] [ -d <string> | -a <path> | -i <path> | -s <string> <path> ]

function dev() {
    output="$( dev-path $@ )"
    if [[ "$output" = pushd* ]] ; then
        eval "${output}"
    else
        echo "${output}"
    fi
}
