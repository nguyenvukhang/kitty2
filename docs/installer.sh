#!/bin/sh
# Copyright (C) 2018 Kovid Goyal <kovid at kovidgoyal.net>
#
# Distributed under terms of the GPLv3 license.

{ \unalias command; \unset -f command; } >/dev/null 2>&1
tdir=''
cleanup() {
    [ -n "$tdir" ] && {
        command rm -rf "$tdir"
        tdir=''
    }
}

die() {
    cleanup
    printf "\033[31m%s\033[m\n\r" "$*" > /dev/stderr;
    exit 1;
}

detect_network_tool() {
    if command -v curl 2> /dev/null > /dev/null; then
        fetch() {
            command curl -fL "$1"
        }
        fetch_quiet() {
            command curl -fsSL "$1"
        }
    elif command -v wget 2> /dev/null > /dev/null; then
        fetch() {
            command wget -O- "$1"
        }
        fetch_quiet() {
            command wget --quiet -O- "$1"
        }
    else
        die "Neither curl nor wget available, cannot download alatty"
    fi
}


detect_os() {
    arch=""
    case "$(command uname)" in
        'Darwin') OS="macos";;
        'Linux')
            OS="linux"
            case "$(command uname -m)" in
                amd64|x86_64) arch="x86_64";;
                aarch64*) arch="arm64";;
                armv8*) arch="arm64";;
                *) die "alatty binaries not available for architecture $(command uname -m)";;
            esac
            ;;
        *) die "alatty binaries are not available for $(command uname)"
    esac
}

expand_tilde() {
    tilde_less="${1#\~/}"
    [ "$1" != "$tilde_less" ] && tilde_less="$HOME/$tilde_less"
    printf '%s' "$tilde_less"
}

parse_args() {
    dest='~/.local'
    [ "$OS" = "macos" ] && dest="/Applications"
    launch='y'
    installer=''
    while :; do
        case "$1" in
            dest=*) dest="${1#*=}";;
            launch=*) launch="${1#*=}";;
            installer=*) installer="${1#*=}";;
            "") break;;
            *) die "Unrecognized command line option: $1";;
        esac
        shift
    done
    dest=$(expand_tilde "${dest}")
    [ "$launch" != "y" -a "$launch" != "n" ] && die "Unrecognized command line option: launch=$launch"
    dest="$dest/alatty.app"
}


get_file_url() {
    url="https://github.com/kovidgoyal/alatty/releases/download/$1/alatty-$2"
    if [ "$OS" = "macos" ]; then
        url="$url.dmg"
    else
        url="$url-$arch.txz"
    fi
}

get_release_url() {
    release_version=$(fetch_quiet "https://sw.kovidgoyal.net/alatty/current-version.txt")
    [ $? -ne 0 -o -z "$release_version" ] && die "Could not get alatty latest release version"
    get_file_url "v$release_version" "$release_version"
}

get_version_url() {
    get_file_url "v$1" "$1"
}

get_nightly_url() {
    get_file_url "nightly" "nightly"
}

get_download_url() {
    installer_is_file="n"
    case "$installer" in
        "nightly") get_nightly_url ;;
        "") get_release_url ;;
        version-*) get_version_url "${installer#*-}";;
        *) installer_is_file="y" ;;
    esac
}

download_installer() {
    tdir=$(command mktemp -d "/tmp/alatty-install-XXXXXXXXXXXX")
    [ "$installer_is_file" != "y" ] && {
        printf '%s\n\n' "Downloading from: $url"
        if [ "$OS" = "macos" ]; then
            installer="$tdir/alatty.dmg"
        else
            installer="$tdir/alatty.txz"
        fi
        fetch "$url" > "$installer" || die "Failed to download: $url"
        installer_is_file="y"
    }
}

ensure_dest() {
    printf "%s\n" "Installing to $dest"
    command rm -rf "$dest" || die "Failed to delete $dest"
    command mkdir -p "$dest" || die "Failed to mkdir -p $dest"
    command rm -rf "$dest" || die "Failed to delete $dest"
}

linux_install() {
    command mkdir "$tdir/mp"
    command tar -C "$tdir/mp" "-xJof" "$installer" || die "Failed to extract alatty tarball"
    ensure_dest
    command mv "$tdir/mp" "$dest" || die "Failed to move alatty.app to $dest"
}

macos_install() {
    command mkdir "$tdir/mp"
    command hdiutil attach "$installer" "-mountpoint" "$tdir/mp" || die "Failed to mount alatty.dmg"
    ensure_dest
    command ditto -v "$tdir/mp/alatty.app" "$dest"
    rc="$?"
    command hdiutil detach "$tdir/mp"
    [ "$rc" != "0" ] && die "Failed to copy alatty.app from mounted dmg"
}

exec_alatty() {
    if [ "$OS" = "macos" ]; then
        exec "open" "$dest"
    else
        exec "$dest/bin/alatty" "--detach"
    fi
    die "Failed to launch alatty"
}

main() {
    detect_os
    parse_args "$@"
    detect_network_tool
    get_download_url
    download_installer
    if [ "$OS" = "macos" ]; then
        macos_install
    else
        linux_install
    fi
    cleanup
    [ "$launch" = "y" ] && exec_alatty
    exit 0
}

main "$@"
