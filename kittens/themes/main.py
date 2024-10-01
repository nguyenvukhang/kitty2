#!/usr/bin/env python
# License: GPLv3 Copyright: 2021, Kovid Goyal <kovid at kovidgoyal.net>

import sys
from typing import List

from alatty.cli import CompletionSpec

help_text = (
    'Change the alatty theme. If no theme name is supplied, run interactively, otherwise'
    ' change the current theme to the specified theme name.'
)
usage = '[theme name to switch to]'
OPTIONS = '''
--cache-age
type=float
default=1
Check for new themes only after the specified number of days. A value of
zero will always check for new themes. A negative value will never check
for new themes, instead raising an error if a local copy of the themes
is not available.


--reload-in
default=parent
choices=none,parent,all
By default, this kitten will signal only the parent alatty instance it is
running in to reload its config, after making changes. Use this option
to instead either not reload the config at all or in all running
alatty instances.


--dump-theme
type=bool-set
default=false
When running non-interactively, dump the specified theme to STDOUT
instead of changing alatty.conf.


--config-file-name
default=alatty.conf
The name or path to the config file to edit. Relative paths are interpreted
with respect to the alatty config directory. By default the alatty config file,
alatty.conf is edited. This is most useful if you add :code:`include themes.conf`
to your alatty.conf and then have the kitten operate only on :file:`themes.conf`,
allowing :code:`alatty.conf` to remain unchanged.
'''.format

def main(args: List[str]) -> None:
    raise SystemExit('This must be run as kitten themes')

if __name__ == '__main__':
    main(sys.argv)
elif __name__ == '__doc__':
    cd = sys.cli_docs  # type: ignore
    cd['usage'] = usage
    cd['options'] = OPTIONS
    cd['help_text'] = help_text
    cd['short_desc'] = 'Manage alatty color schemes easily'
    cd['args_completion'] = CompletionSpec.from_string('type:special group:complete_themes')
