Maintains an list of software development projects in a text file with a few very simple actions available:

  pushd <s>    pushd to the first path containing <s>
  append <s>   append <s> the the bottom of the list
  insert <s>   insert <s> at the top of the list
  delete <s>   delete the first path containing <s>
  set <s> <p>  Set the first path containing <s> to <p>

Also supports glob and regular expression matching.

Default path file is '~/.dev-paths' but this may be altered using the DEV_PATHS environment variable.

