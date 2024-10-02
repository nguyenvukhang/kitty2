#!/usr/bin/env python
# License: GPLv3 Copyright: 2019, Kovid Goyal <kovid at kovidgoyal.net>

import os
import time
from contextlib import suppress
from typing import NamedTuple
from urllib.request import urlopen

from .config import atomic_save
from .constants import Version, cache_dir, website_url
from .utils import open_url

CHANGELOG_URL = website_url('changelog')
RELEASED_VERSION_URL = website_url() + 'current-version.txt'
CHECK_INTERVAL = 24 * 60 * 60.


class Notification(NamedTuple):
    version: Version
    time_of_last_notification: float
    notification_count: int


def notification_activated() -> None:
    open_url(CHANGELOG_URL)


def version_notification_log() -> str:
    override = getattr(version_notification_log, 'override', None)
    if isinstance(override, str):
        return override
    return os.path.join(cache_dir(), 'new-version-notifications-1.txt')


def get_released_version() -> str:
    try:
        raw = urlopen(RELEASED_VERSION_URL).read().decode('utf-8').strip()
    except Exception:
        raw = '0.0.0'
    return str(raw)


def parse_line(line: str) -> Notification:
    parts = line.split(',')
    version, timestamp, count = parts
    parts = version.split('.')
    v = Version(int(parts[0]), int(parts[1]), int(parts[2]))
    return Notification(v, float(timestamp), int(count))


def read_cache() -> dict[Version, Notification]:
    notified_versions = {}
    with suppress(FileNotFoundError):
        with open(version_notification_log()) as f:
            for line in f:
                try:
                    n = parse_line(line)
                except Exception:
                    continue
                notified_versions[n.version] = n
    return notified_versions


def already_notified(version: tuple[int, int, int]) -> bool:
    notified_versions = read_cache()
    return version in notified_versions


def save_notification(version: Version) -> None:
    notified_versions = read_cache()
    if version in notified_versions:
        v = notified_versions[version]
        notified_versions[version] = v._replace(time_of_last_notification=time.time(), notification_count=v.notification_count + 1)
    else:
        notified_versions[version] = Notification(version, time.time(), 1)
    lines = []
    for version in sorted(notified_versions):
        n = notified_versions[version]
        lines.append('{},{},{}'.format(
            '.'.join(map(str, n.version)),
            n.time_of_last_notification,
            n.notification_count))
    atomic_save('\n'.join(lines).encode('utf-8'), version_notification_log())


def run_worker() -> None:
    import random
    import time
    time.sleep(random.randint(1000, 4000) / 1000)
    with suppress(BrokenPipeError):  # happens if parent process is killed before us
        print(get_released_version())
