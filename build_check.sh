#!/bin/bash
# usage: ./build_check.sh mycode.s [extra quickasm flags, e.g. --32 -v]

set -e

SRC="$1"
shift                              # remove $1 (the source file) from the argument list
BASE="${SRC%.s}"
BIN="${BASE}.elf"

python3 quickasm.py "$SRC" -o "$BIN" "$@"    # "$@" = whatever flags you passed after the source file, forwarded as-is

echo "[+] Built $BIN, running against /challenge/check..."
/challenge/check "$BIN"
