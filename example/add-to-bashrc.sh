# dev-path : Move, via pushd, to the first development path matching <pattern>.
#            * actually generates shell commands to do move
#
# Alternatively, if an action is specified, perform it instead.
#
# DEV_PATHS is typically '~/.dev-paths' but this may be controlled
# by setting DEV_PATHS to an alternate file name.

function dev() {
    # eval "$( dev_s $@ )"
    eval "$( dev-path $@ )"
}

