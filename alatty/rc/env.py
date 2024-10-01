#!/usr/bin/env python
# License: GPLv3 Copyright: 2020, Kovid Goyal <kovid at kovidgoyal.net>

from typing import Any, Optional

from .base import ArgsType, Boss, PayloadGetType, PayloadType, RCOptions, RemoteCommand, ResponseType, Window


class Env(RemoteCommand):

    protocol_spec = __doc__ = '''
    env+/dict.str: Dictionary of environment variables to values. When a env var ends with = it is removed from the environment.
    '''

    short_desc = 'Change environment variables seen by future children'
    desc = (
        'Change the environment variables that will be seen in newly launched windows.'
        ' Similar to the :opt:`env` option in :file:`alatty.conf`, but affects running alatty instances.'
        ' If no = is present, the variable is removed from the environment.'
    )
    args = RemoteCommand.Args(spec='env_var1=val env_var2=val ...', minimum_count=1, json_field='env')

    def message_to_alatty(self, global_opts: RCOptions, opts: Any, args: ArgsType) -> PayloadType:
        if len(args) < 1:
            self.fatal('Must specify at least one env var to set')
        env = {}
        for x in args:
            if '=' in x:
                key, val = x.split('=', 1)
                env[key] = val
            else:
                env[x + '='] = ''
        return {'env': env}

    def response_from_alatty(self, boss: Boss, window: Optional[Window], payload_get: PayloadGetType) -> ResponseType:
        from alatty.child import default_env, set_default_env
        from alatty.utils import expandvars
        new_env = payload_get('env') or {}
        env = default_env().copy()
        for k, v in new_env.items():
            if k.endswith('='):
                env.pop(k[:-1], None)
            else:
                env[k] = expandvars(v or '', env)
        set_default_env(env)
        return None


env = Env()
