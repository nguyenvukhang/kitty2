#!/usr/bin/env python
# License: GPL v3 Copyright: 2018, Kovid Goyal <kovid at kovidgoyal.net>


import importlib
import os
import sys
from contextlib import contextmanager
from functools import partial
from typing import TYPE_CHECKING, Any, Callable, Dict, FrozenSet, Generator, List, NamedTuple, Optional, cast

from alatty.constants import list_alatty_resources
from alatty.types import run_once
from alatty.typing import BossType, WindowType
from alatty.utils import resolve_abs_or_config_path

aliases = {'url_hints': 'hints'}
if TYPE_CHECKING:
    from alatty.conf.types import Definition
else:
    Definition = object


def resolved_kitten(k: str) -> str:
    ans = aliases.get(k, k)
    head, tail = os.path.split(ans)
    tail = tail.replace('-', '_')
    return os.path.join(head, tail)


def path_to_custom_kitten(config_dir: str, kitten: str) -> str:
    path = resolve_abs_or_config_path(kitten, conf_dir=config_dir)
    return os.path.abspath(path)


@contextmanager
def preserve_sys_path() -> Generator[None, None, None]:
    orig = sys.path[:]
    try:
        yield
    finally:
        if sys.path != orig:
            del sys.path[:]
            sys.path.extend(orig)


class CLIOnlyKitten(TypeError):
    def __init__(self, kitten: str):
        super().__init__(f'The {kitten} kitten must be run only at the commandline, as: kitten {kitten}')


def import_kitten_main_module(config_dir: str, kitten: str) -> Dict[str, Any]:
    if kitten.endswith('.py'):
        with preserve_sys_path():
            path = path_to_custom_kitten(config_dir, kitten)
            if os.path.dirname(path):
                sys.path.insert(0, os.path.dirname(path))
            with open(path) as f:
                src = f.read()
            code = compile(src, path, 'exec')
            g = {'__name__': 'kitten'}
            exec(code, g)
            hr = g.get('handle_result', lambda *a, **kw: None)
        return {'start': g['main'], 'end': hr}

    kitten = resolved_kitten(kitten)
    m = importlib.import_module(f'kittens.{kitten}.main')
    if not hasattr(m, 'main'):
        raise CLIOnlyKitten(kitten)
    return {
        'start': getattr(m, 'main'),
        'end': getattr(m, 'handle_result', lambda *a, **k: None),
    }


class KittenMetadata(NamedTuple):
    handle_result: Callable[[Any, int, BossType], None] = lambda *a: None

    type_of_input: Optional[str] = None
    no_ui: bool = False
    has_ready_notification: bool = False



def create_kitten_handler(kitten: str, orig_args: List[str]) -> KittenMetadata:
    from alatty.constants import config_dir
    kitten = resolved_kitten(kitten)
    m = import_kitten_main_module(config_dir, kitten)
    handle_result = m['end']
    return KittenMetadata(
        handle_result=partial(handle_result, [kitten] + orig_args),
        type_of_input=getattr(handle_result, 'type_of_input', None),
        no_ui=getattr(handle_result, 'no_ui', False),
        has_ready_notification=getattr(handle_result, 'has_ready_notification', False))


def set_debug(kitten: str) -> None:
    import builtins

    from kittens.tui.loop import debug
    setattr(builtins, 'debug', debug)


def launch(args: List[str]) -> None:
    config_dir, kitten = args[:2]
    kitten = resolved_kitten(kitten)
    del args[:2]
    args = [kitten] + args
    os.environ['ALATTY_CONFIG_DIRECTORY'] = config_dir
    set_debug(kitten)
    m = import_kitten_main_module(config_dir, kitten)
    try:
        result = m['start'](args)
    finally:
        sys.stdin = sys.__stdin__
    if result is not None:
        import base64
        import json
        data = base64.b85encode(json.dumps(result).encode('utf-8'))
        sys.stdout.buffer.write(b'\x1bP@kitty-kitten-result|')
        sys.stdout.buffer.write(data)
        sys.stdout.buffer.write(b'\x1b\\')
    sys.stderr.flush()
    sys.stdout.flush()


def run_kitten(kitten: str, run_name: str = '__main__') -> None:
    import runpy
    original_kitten_name = kitten
    kitten = resolved_kitten(kitten)
    set_debug(kitten)
    if kitten in all_kitten_names():
        runpy.run_module(f'kittens.{kitten}.main', run_name=run_name)
        return
    # Look for a custom kitten
    if not kitten.endswith('.py'):
        kitten += '.py'
    from alatty.constants import config_dir
    path = path_to_custom_kitten(config_dir, kitten)
    if not os.path.exists(path):
        print('Available builtin kittens:', file=sys.stderr)
        for kitten in all_kitten_names():
            print(kitten, file=sys.stderr)
        raise SystemExit(f'No kitten named {original_kitten_name}')
    m = runpy.run_path(path, init_globals={'sys': sys, 'os': os}, run_name='__run_kitten__')
    from alatty.fast_data_types import set_options
    try:
        m['main'](sys.argv)
    finally:
        set_options(None)


@run_once
def all_kitten_names() -> FrozenSet[str]:
    ans = []
    for name in list_alatty_resources('kittens'):
        if '__' not in name and '.' not in name and name != 'tui':
            ans.append(name)
    return frozenset(ans)


def list_kittens() -> None:
    print('You must specify the name of a kitten to run')
    print('Choose from:')
    print()
    for kitten in all_kitten_names():
        print(kitten)


def get_kitten_cli_docs(kitten: str) -> Any:
    setattr(sys, 'cli_docs', {})
    run_kitten(kitten, run_name='__doc__')
    ans = getattr(sys, 'cli_docs')
    delattr(sys, 'cli_docs')
    if 'help_text' in ans and 'usage' in ans and 'options' in ans:
        return ans


def get_kitten_wrapper_of(kitten: str) -> str:
    setattr(sys, 'cli_docs', {})
    run_kitten(kitten, run_name='__wrapper_of__')
    ans = getattr(sys, 'cli_docs')
    delattr(sys, 'cli_docs')
    return ans.get('wrapper_of') or ''


def get_kitten_completer(kitten: str) -> Any:
    run_kitten(kitten, run_name='__completer__')
    ans = getattr(sys, 'kitten_completer', None)
    if ans is not None:
        delattr(sys, 'kitten_completer')
    return ans


def get_kitten_conf_docs(kitten: str) -> Optional[Definition]:
    setattr(sys, 'options_definition', None)
    run_kitten(kitten, run_name='__conf__')
    ans = getattr(sys, 'options_definition')
    delattr(sys, 'options_definition')
    return cast(Definition, ans)


def get_kitten_extra_cli_parsers(kitten: str) -> Dict[str,str]:
    setattr(sys, 'extra_cli_parsers', {})
    run_kitten(kitten, run_name='__extra_cli_parsers__')
    ans = getattr(sys, 'extra_cli_parsers')
    delattr(sys, 'extra_cli_parsers')
    return cast(Dict[str, str], ans)


def main() -> None:
    try:
        args = sys.argv[1:]
        launch(args)
    except Exception:
        print('Unhandled exception running kitten:')
        import traceback
        traceback.print_exc()
        input('Press Enter to quit')
