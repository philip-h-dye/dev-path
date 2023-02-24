# $ grep cyga .dev-paths | strip-cr - | tr -d '\n'
# ~phdye/src/python.cygwin/cygwin/version/cygapi/009/cyg-api
#
# Oddly though :
#
# $ cd $( grep cygapi .dev-paths | strip-cr - | tr -d '\n' )
# bash: /home/phdye/src/python.cygwin/cygwin/version/cygapi/009/cyg-api: Is a directory
#
# Oddly though :
#
# $ cd $( eval " echo $( grep /cygapi .dev-paths | head -1 ) " )
# $ pwd
# /home/phdye/src/python.cygwin/cygwin/version/cygapi/009/cyg-api
#

DEV_PATHS=$HOME/.dev-paths

# Push to a known development path -- may use a pattern if necessary
function dev () {
    function usage() {
	echo
	echo "Usage:  dev [options] <pattern>"
	echo "        dev --add <path>"
	echo "        dev --set <pattern> <path>"
	echo
	echo "Usage:  dev [options] <pattern>"
	echo
        echo "  Pushd to the first development path identified by <pattern>."
	echo
	echo "  Development paths found in ${DEV_PATHS}."
	echo
	echo "  Could use '.' to get the first listed path."
	echo
	echo "Options :"
	echo
	echo "  -a, --add     Append <path> to ${DEV_PATHS}"
	echo	
	echo "  -i, --prefix  Insert <path> at the top of ${DEV_PATHS}"
	echo	
	echo "  -s, --set     Replace first path matching <pattern> with <path>."
	echo "                  report error if not found."
	echo
	echo "  -h, --help    Show this usage message."
	echo
	echo "Future :"
	echo
	echo "  -N            Go to the Nth matching path."
	echo
	return
    }

    if [ $# -gt 1 -o "$1" = "--help" -o "$1" = "-h" ] ; then
	usage
	return
    fi
    
    # 001 : Initial
    #   0. set pattern
    #   1. skip comment lines
    #   2. skip blank lines
    #   3. use the first line
    # Works :
    #   $ pattern=cygapi
    #   $ egrep -v '^\s*#' ${DEV_PATHS} | sed -e '/^\s*$/d' | egrep "$pattern" | head -1
    #   /home/phdye/src/python.cygwin/cygwin/version/cygapi/009/cyg-api
    # Issue :
    #   Can still pick up invalid paths since DEV_PATHS is simply text.
    #
    # 002 : Simpler and avoids junk at the start
    #   0. set pattern
    #   1. Require paths to start with either '/' or '~'
    #   2. use the first line
    # Works :
    #   $ pattern=cygapi
    #   $ egrep "^[/|~].*${pattern}" ${DEV_PATHS} | head -1
    #   /home/phdye/src/python.cygwin/cygwin/version/cygapi/009/cyg-api
    # Issues :
    #   Trailing junk would break it but this is good enough for a quick
    #   and dirty personal tool.

    pattern="$1"
    target=$( egrep "^[/|~].*${pattern}" ${DEV_PATHS} | head -1 )
    # echo "target: '${target}'"
    target=$( eval "echo $target" )
    # echo "target: '${target}'"
    msg=
    if [ ! -e "${target}" ] ; then
	msg="does not exist"
    else
	prefix="is not"
	if [ ! -d "${target}" ] ; then
	    msg="${msg}$( echo ; echo 'a directory')"
	    prefix=
	fi
	if [ ! -r "${target}" ] ; then
	    if [ -n "${msg}" ] ; then msg="${msg} / " ; fi
	    msg="${msg}$( echo ; echo 'readable')"
	    prefix=
	fi
	if [ ! -x "${target}" ] ; then
	    if [ -n "${msg}" ] ; then msg="${msg} / " ; fi
	    msg="${msg}$( echo ; echo 'writable')"
	fi
    fi
    if [ -n "${msg}" ] ; then
	echo "Error: '${target}' ${msg}"
	return
    fi
    pushd ${target}
    # put it on the stack second time for insurance :)
    pushd . > /dev/null
    if [ -r .alias ] ; then
	source .alias
    fi
}
