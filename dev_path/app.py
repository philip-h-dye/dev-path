# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------

from __future__ import print_function

__doc__ = """
Move to a specified active development path via pushd.  Or rather,
it generates the shell command to do so.

Usage:  dev [options] <string>
        dev [options] ( -d | --display | show    | list    ) <string>
        dev [options] ( -a | --append  | append  | add     ) <path>
        dev [options] ( -p | --prepend | first   | start   ) <path>
        dev [options] ( -s | --set     | set     | assign  ) <string> <path>
        dev [options] (      --insert-before     | before  ) <string> <path>
        dev [options] (      --insert-after      | after   ) <string> <path>
        dev [options] (      --delete  | delete  | remove  ) <string>

  Move, via pushd, to the first development path containing <string>.

  With '--regexp', <string> may be a python regular expression.

  With '--glob', <string> may be a shell glob pattern.

  If an action is specified, do not change directories, perform
  the specified action.  <path> is always converted to an absolute
  path with '~' expansion if applicable.  If --force isn't specified,
  it is an error to specify a non-existent path.

  DEV_PATHS is typically '~/.dev-paths' but this may be controlled
  by setting DEV_PATHS to an alternate file name.

  Comments, blanklines and whitespace are ignored.  Comments start
  with '#' and they may be full lines or trailing.

  All added/inserted/set paths are converted to an absolute path
  if the provided <path> is relative.

Path Actions :
  -d, --display  Display matching paths, do not push
    --show       Alias for --display
    --list       Alias for --display
  -a, --append   Append <path> to the end of the file.
  -i, --insert   Insert <path> at the start of the file.
  --delete       Delete the first path line matching <string>
                 or report error if <string> is not found.
  -s, --set      Replace first path line matching <string> with
    --assign     <path> or report error if not found.

Options :
  -f, --force   Apply action regardless of whether <path> exists
  -r, --regex   <string> is a python regular expression.
  -g, --glob    <string> is a shell glob patttern.
  -h, --help    Show this usage message.
  --version     Show version and exit.
  --debug       Show internal handlingy
  --debug-argv  Show arguments exactly as received by main()
  --debug-args  Show arguments after being parsed by docopt().
  --debug-attr  Show arguments after being converted to attributes.

Future :

X -N            Go to the Nth matching path.
X -q, --quiet   Quiet unnessary informational output.
X -s, --silent  Silence even warnings like output to '.' due
X               to an unwritable <dll> directory.
X -i, --ignore  Ignore errors, simply continue on to the next <dll>.

Examples:

  [ 0 ] phdyex @ xps-ne ~
  $ dev_path cygapi
  pushd ~/src/cygapi

  [ 0 ] phdyex @ xps-ne ~
  $ function dev() {
        eval "$( dev_path '$@' )"
        if [ -r .alias ] ; then source .alias ; fi    
  }
  # See dev_path/shell/dev-function.sh for a nuanced implementation.

  [ 0 ] phdyex @ xps-ne ~
  $ dev cygapi
  ~/src/cygwin/cygapi ~

  [ 0 ] phdyex @ xps-ne ~/src/cygwin/cygapi
  $ dev add ~/src/foobar
  added

  [ 0 ] phdyex @ xps-ne ~
  $

Report bugs to <philip@phd-solutions.com>.
"""

import sys
import os
import re
import fnmatch
import tempfile
import shutil
import shlex

from collections import namedtuple
from pathlib import Path

from prettyprinter import register_pretty, pretty_call, cpprint as pp

from docopt import docopt

from dev_path import __version__

from .p import hash_pp

#------------------------------------------------------------------------------

try :
    DEV_PATHS = Path( os.environ['DEV_PATHS'] ).expanduser()
except:
    DEV_PATHS = Path('~', '.dev-paths').expanduser()

#------------------------------------------------------------------------------

def main ( argv = sys.argv ) :

    if '--debug-argv' in argv:
        print("# [ main : argv ]")
        hash_pp(argv)
        print('')

    args = docopt(__doc__, argv=argv[1:], options_first=True,
                  version=__version__ )

    if args['--debug-args']:
        print("# [ args : after docopt() ]")
        hash_pp(args)
        print('')

    cfg = fields ( args )

    if args['--debug-attr']:
        print("# [ args : options and arguments as attributes ]")
        hash_pp(cfg)
        print('')

    # Recast <path> operand as Path() and ensure that it is absolute
    if cfg.val.path is not None :
        cfg.val.path = Path(cfg.val.path).resolve()
        if not cfg.val.path.exists() and not cfg.force: 
            raise ValueError(f"<path> does not exist: '{cfg.val.path}'")

    if args['--debug']:
        print("# [ args : fields ]")
        hash_pp(cfg)
        print('')

    # Each command exits, there is no fall through
    
    if cfg.opt.display:
        display(cfg)

    if cfg.opt.append:
        append(cfg)

    if cfg.opt.prepend:
        prepend(cfg)

    if cfg.opt.insert_before:
        insert_before(cfg)

    if cfg.opt.insert_after:
        insert_after(cfg)

    if cfg.opt.delete:
        delete(cfg)

    if cfg.opt.assign:
        assign(cfg)

    pushd(cfg)

#------------------------------------------------------------------------------

def display(cfg):  # path
    m = matcher(cfg)
    with open(DEV_PATHS, 'r') as in_f :
        for line in in_f :
            candidate = line.strip()
            try :
                candidate = candidate [ : candidate.index('#') ].strip()
            except :
                pass
            if m.has_pattern(candidate):
                print(candidate)
    sys.exit(0)

#------------------------------------------------------------------------------

def append(cfg):  # path
    # print('# append() : [cfg]') ; hash_pp(cfg) ; print("# - - - - -\n")
    with open(DEV_PATHS, 'a') as out_f :
        print(cfg.val.path, file=out_f)
    sys.exit(0)

#------------------------------------------------------------------------------

def prepend(cfg):  # path
    with tempfile.NamedTemporaryFile('w') as out_f :
        print(cfg.val.path, file=out_f)
        with open(DEV_PATHS, 'r') as in_f :
            out_f.write( in_f.read() )
        out_f.flush()
        shutil.copy(out_f.name, DEV_PATHS)
    sys.exit(0)

#------------------------------------------------------------------------------

def insert_before(cfg):  # string
    m = matcher(cfg)
    with tempfile.NamedTemporaryFile('w') as out_f :
        with open(DEV_PATHS, 'r') as in_f :
            line = copy_until_match(m, in_f, out_f)
            print(cfg.val.path, file=out_f)
            if line:
                out_f.write(line+'\n')
                out_f.write( in_f.read() )
        out_f.flush()
        shutil.copy(out_f.name, DEV_PATHS)
    sys.exit(0)

#------------------------------------------------------------------------------

def insert_after(cfg):  # string
    m = matcher(cfg)
    with tempfile.NamedTemporaryFile('w') as out_f :
        with open(DEV_PATHS, 'r') as in_f :
            if line := copy_until_match(m, in_f, out_f):
                out_f.write(line+'\n')
            print(cfg.val.path, file=out_f)
            if line:
                out_f.write( in_f.read() )
        out_f.flush()
        shutil.copy(out_f.name, DEV_PATHS)
    sys.exit(0)

#------------------------------------------------------------------------------

def delete(cfg):  # string
    m = matcher(cfg)
    with tempfile.NamedTemporaryFile('w') as out_f :
        with open(DEV_PATHS, 'r') as in_f :
            if not copy_until_match(m, in_f, out_f):
                if cfg.opt.force:
                    return 0
                print(f"dev-path: {m.type_} '{cfg.val.string}' {m.verb}  "
                      f"any path in '{DEV_PATHS}'.", file=sys.stderr)
                raise SystemExit
            out_f.write( in_f.read() )
        out_f.flush()
        shutil.copy(out_f.name, DEV_PATHS)
    sys.exit(0)

#------------------------------------------------------------------------------

def assign(cfg):	  # string path
    m = matcher(cfg)
    with tempfile.NamedTemporaryFile('w') as out_f :
        with open(DEV_PATHS, 'r') as in_f :
            if not copy_until_match(m, in_f, out_f):
                print(f"dev-path: {m.type_} '{cfg.val.string}' {m.verb}  "
                      f"any path in '{DEV_PATHS}'.", file=sys.stderr)
                raise SystemExit
            print(cfg.val.path, file=out_f)
            out_f.write( in_f.read() )
        out_f.flush()
        shutil.copy(out_f.name, DEV_PATHS)
    sys.exit(0)

#------------------------------------------------------------------------------

def pushd(cfg):

    m = matcher(cfg)

    with DEV_PATHS.open('r') as dev_paths :
        for line in dev_paths :
            candidate = line.strip()
            try :
                candidate = candidate [ : candidate.index('#') ].strip()
            except Exception as _ :
                pass
            if m.has_pattern(candidate):
                print(f"pushd {shlex.quote(candidate)}")
                print(f"if [ -r .alias ] ; then source .alias ; fi")
                return 0

    print(f"dev-path: {m.type_} '{cfg.val.string}' {m.verb}  "
          f"any path in '{DEV_PATHS}'.", file=sys.stderr)
    sys.exit(0)

#------------------------------------------------------------------------------

def matcher(cfg):

    # print("matcher(cfg): ", end='')
    # hash_pp(cfg)

    if cfg.opt.regex:
        type_ = 'Regexp'
        verb = 'does not match'
        has_pattern = re.compile(cfg.val.string).search
    elif cfg.opt.glob:
        type_ = 'Glob'
        verb = 'does not match'
        expr = f"*{cfg.val.string}*"
        has_pattern = lambda path : fnmatch.fnmatch(path, expr)
    else:
        type_ = 'String'
        verb = 'not found in'
        has_pattern = lambda path : cfg.val.string in path

    return ( namedtuple('Matcher','type_ verb has_pattern') \
             (type_, verb, has_pattern ) )

#------------------------------------------------------------------------------

def copy_until_match(m, in_f, out_f):

    for line in in_f :
        candidate = line.strip()
        try :
            candidate = candidate [ : candidate.index('#') ].strip()
        except :
            pass
        if m.has_pattern(candidate):
            return candidate
        out_f.write(line)

    return None

#------------------------------------------------------------------------------

# Options:  -<letter> or --<word>
# Values:   '<'<word>'>' or plain word
#
# All words folded to lowercase.
#
# Resolve to arguments object with values and options in separate name spaces :
#   a.opt.<option_name>
#   a.val.<value_name>
#
# i.e. --test-name => f.opt.test_name
#      FILE        => f.val.file

opt_mapping = { "show"      : "display",
                "list"      : "display",
                "add"       : "append",
                "first"     : "prepend",
                "start"     : "prepend",
                "before"    : "insert_before",
                "after"     : "insert_after",
                "set"       : "assign",
              }

def fields(args):

    # { <field-name> : <value> , ... }
    options = { }
    values = { }

    # Options: -<letter> or --<word>
    def option ( key ):
        field = key.lower()
        if field.startswith('-'):
            field = field[1:]
        if field.startswith('-'):
            field = field[1:]
        field = field.replace('-','_')
        if field in opt_mapping:
            field = opt_mapping[field]
        # if field in options:
        #     raise ValueError(f"Options, resolved field name clash '{field}' -- please address")
        if field not in options or args[key]:
            options[field] = args[key]

    # Positional arguments: <name> , or name, or NAME
    def value ( key ):
        field = key.lower().strip('<>')
        if field in values:
            raise ValueError(f"Values, resolved field name clash '{field}' -- please address")
        values[field] = args[key]

    for key in args:
        if key.startswith('-') or isinstance(args[key], bool):
            option(key)
        else:
            value(key)

    # if args['--debug']:
    #     print('[options]') ; pp(options) ; print("\n- - - - -\n")
    # Options = namedtuple('Options', ' '.join(options.keys()))
    create_dataclass('Options', ' '.join(options.keys()))
    opt = Options(*options.values())
    # if args['--debug']:
    #     print('[options]') ; pp(opt) ; print("\n- - - - -\n")

    # if args['--debug']:
    #     print('[values]') ; pp(values) ; print("\n- - - - -\n")
    # Values = namedtuple('Values', ' '.join(values.keys()))
    create_dataclass('Values', ' '.join(values.keys()))
    val = Values(*values.values())
    # if args['--debug']:
    #     print('[values]') ; pp(val) ; print("\n- - - - -\n")

    def Arguments_init ( self, opt, val ):
        self.opt = opt
        self.val = val

    Arguments = type("Arguments", (object,), {"__init__" : Arguments_init})

    @register_pretty(Arguments)
    def pretty_Arguments(value, ctx):
        return pretty_call(
            ctx,
            Arguments,
            opt=value.opt,
            val=value.val,
        )

    argx = Arguments(opt, val)

    def argx_str ( a ):
        return "Arguments( opt = {repr(a.opt)}, val = {repr(a.val)} )"
    setattr ( argx, '__str__', argx_str )
    setattr ( argx, '__repr__', argx_str )

    # pp(argx)

    return argx

# ------------------------------------------------------------------------------

# NamedTuples cannot be modified.
def create_dataclass(name, field_name_string, bases=(object,)):

    if not isinstance(bases, tuple):
        bases = (bases,)

    bases = list(bases)

    for idx in range(len(bases)):
        base = bases[idx]
        if isinstance(base, type):
            base = bases[idx] = base.__name__
        if not isinstance(base, str):
            raise TypeError("Members the <base> tuple may be either a type "
                            f"or type name (str), not '{str(type(base))}' "
                            f"(base member {1+idx})")

    bases_string = ', '.join(bases)

    code = f"""
from dataclasses import dataclass
@dataclass
class {name} ({bases_string}):
"""
    from keyword import iskeyword

    for field_name in field_name_string.split():
        if iskeyword(field_name):
            field_name += '_'
        code += f"    {field_name} : object\n"

    # print(code)

    exec(code, globals())

#------------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main(sys.argv))

#------------------------------------------------------------------------------
