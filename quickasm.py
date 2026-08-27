#!/usr/bin/env python3
"""quickasm — assemble, link, and (optionally) run raw x86 asm in one shot."""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def check_syntax_consistency(src: Path) -> None:
    text = src.read_text()
    has_directive = ".intel_syntax" in text
    looks_intel = bool(re.search(r"\bmov\s+\w+,\s*\w+", text)) and "%" not in text.split("mov", 1)[0]

    if looks_intel and not has_directive:
        print("warning: looks like Intel syntax but no '.intel_syntax noprefix' found", file=sys.stderr)
    elif has_directive:
        print("detected: Intel syntax")
    else:
        print("detected: AT&T syntax")


def build(src: Path, out: Path, bits: int, keep_obj: bool, verbose: bool) -> int:
    obj = out.with_suffix(".o")

    as_cmd = ["as", "-o", str(obj), str(src)]
    ld_cmd = ["ld", "-o", str(out), str(obj)]

    if bits == 32:
        as_cmd.insert(1, "--32")
        ld_cmd[1:1] = ["-m", "elf_i386"]

    for cmd in (as_cmd, ld_cmd):
        if verbose:
            print("+", " ".join(cmd))
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f"failed: {' '.join(cmd)}", file=sys.stderr)
            return result.returncode

    if not keep_obj:
        obj.unlink(missing_ok=True)

    out.chmod(0o755)
    return 0


def main():
    parser = argparse.ArgumentParser(description="Assemble + link raw asm, fast.")
    parser.add_argument("source", type=Path, help=".s file (Intel or AT&T)")
    parser.add_argument("-o", "--output", type=Path, help="output binary path")
    parser.add_argument("--32", dest="bits32", action="store_true", help="build 32-bit ELF")
    parser.add_argument("--run", action="store_true", help="execute after building")
    parser.add_argument("--keep-obj", action="store_true", help="don't delete the .o file")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    check_syntax_consistency(args.source)

    out = args.output or args.source.with_suffix("")
    bits = 32 if args.bits32 else 64

    rc = build(args.source, out, bits, args.keep_obj, args.verbose)
    if rc != 0:
        sys.exit(rc)

    print(f"built: {out}")
    if args.run:
        subprocess.run([str(out.resolve())])


if __name__ == "__main__":
    main()
