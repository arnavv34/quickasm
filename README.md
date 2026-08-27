# quickasm

A one-command wrapper around `as`/`ld` for building raw x86-64 assembly
into executables, without hand-typing the assemble+link+chmod dance
every time.

## Usage
    ./quickasm.py examples/hello.s --run

## Why
Built while doing low-level syscall/binary exploitation practice
(pwn.college, OverTheWire) — got tired of retyping the same
`as -o x.o x.s && ld -o x x.o && chmod +x x` sequence for every
throwaway asm file.

## Options
- `--32`        build a 32-bit ELF
- `--run`       execute immediately after building
- `--keep-obj`  keep the intermediate .o file
- `-o PATH`     custom output path
