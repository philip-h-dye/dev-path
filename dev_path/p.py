import io

from contextlib import redirect_stdout

from prettyprinter import register_pretty, pretty_call, cpprint as pp

#------------------------------------------------------------------------------

def pp_str(obj):
    sio = io.StringIO()
    with redirect_stdout(sio):
        pp(obj)
    return sio.getvalue()

def hash_pp(obj):
    prefix = '# '
    print(prefix + pp_str(obj).replace("\n", f"\n{prefix}"))

#------------------------------------------------------------------------------
