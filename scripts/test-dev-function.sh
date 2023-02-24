#!/bin/echo "*** must be sourced: . dev-funcion.sh"

# Development version of ./dev_path/shell/dev-function.sh

function test-dev() {
    # echo "#"
    # echo "# module base = '${module_base}'" > /dev/tty
    action=$( ${module_base}/scripts/test-dev-path $@ )
    echo "${action}" | egrep '^#' > /dev/tty
    action=$( echo "${action}" | grep -v '^#' )
    if [ -z "${action}" ] ; then
	( echo '[action]' ; echo "${action}" ; echo ) > /dev/tty
    else
	eval "${action}"
    fi
}

#

function test-dev_CONTEXT() {
    pwd=$( /bin/pwd )
    nam=$( basename ${pwd} )
    if [ "${nam}" == "dev-path" ]; then
	eval "$( ./scripts/test-dev-path $@ )"
    else
	# eval "$( dev-path $@ )"	
	cmd=$( dev-path "$@" )
	eval "${cmd}"
    fi
}

#
