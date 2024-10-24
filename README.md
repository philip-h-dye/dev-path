Maintains an list of software development projects in a text file with a few very simple actions available:

  pushd <s>    pushd to the first path containing <s>
  append <s>   append <s> the the bottom of the list
  insert <s>   insert <s> at the top of the list
  delete <s>   delete the first path containing <s>
  set <s> <p>  Set the first path containing <s> to <p>
  show <s>     Show the first path containing <s>

Also supports glob and regular expression matching.

Default path file is '~/.dev-paths' but this may be altered using the DEV_PATHS environment variable.

.dev-path.rc   yaml configuration file, such as default shell

Shell: *Not Yet Implemented*
  --shell <shell>  Generate commands for <shell>   [default 'sh']
  -a, --ash        Almquist shell                  pushd?
  -c, --csh        C Shell, csh
  -d, --dash       Debian Almquist Shell           pushd?
  -f, --fish       Fish Shell
  -k, --ksh        Korn Shell                      (alias for '--sh')
  -i, --ion        Ion Shell
  -p, --psh        Public Domain Korn Shell,
      --ps         Powershell                      pushd?
  -s, --sh         Bourne Shell
  -t, --tcsh       TENEX C Shell                   (alias for --csh')
  -x, --xonsh      Xonsh Shell
  -z, --zsh        Z Shell

PowerShell:
  Get-Alias Pushd : pushd -> Push-Location
  Get-Alias Popd : popd -> Pop-Location

