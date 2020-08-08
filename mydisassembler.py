"""
This disassembler for the JCoCo virtual machine does not work on closures
"""


import types
import dis
import importlib
import os
import sys


JUMP_OPS = [
    "FOR_ITER",
    "JUMP_ABSOLUTE",
    "JUMP_FORWARD",
    "POP_JUMP_IF_FALSE",
    "POP_JUMP_IF_TRUE",
    "SETUP_EXCEPT",
    "SETUP_FINALLY",
    "SETUP_LOOP",
]


def disassemble(obj, indent_level=1):
    if hasattr(obj, "__code__"):
        co = obj.__code__
    elif isinstance(obj, types.CodeType):
        co = obj
    else:
        print(
            f"Can't make sense of '{obj}', you should pass a function "
            "or an object of type CodeType"
        )

    indentation = "\t" * (indent_level-1)

    print(f"{indentation}Function: {co.co_name}/{co.co_argcount}")

    for constant in co.co_consts:
        if isinstance(constant, types.CodeType):
            disassemble(constant, indent_level+1)

    constants = []
    for c in co.co_consts:
        if isinstance(c, types.CodeType):
            constants.append(f"code({c.co_name})")
        elif isinstance(c, str):
            if not c.startswith("main"):
                constants.append(repr(c))
        else:
            constants.append(repr(c))
    if constants is not None:
        print(f"{indentation}Constants: {', '.join(constants)}")

    locs = ", ".join(map(str, co.co_varnames))
    if locs != "":
        print(f"{indentation}Locals: {locs}")

    globs = ", ".join(map(str, co.co_names))
    if globs != "":
        print(f"{indentation}Globals: {globs}")

    # free variables are variables used in a function, that are neither
    # local variables nor function parameters (i.e. non-local)
    freevars = ", ".join(map(str, co.co_freevars))
    if freevars != "":
        print(f"{indentation}FreeVars: {freevars}")

    # cell variables are indirect references to values
    cellvars = ", ".join(map(str, co.co_cellvars))
    if cellvars != "":
        print(f"{indentation}CellVars: {cellvars}")

    print(f"{indentation}BEGIN")

    # need to make labels in advance
    labels = {}
    label_index = 0
    for i in dis.get_instructions(obj):
        if i.opname in JUMP_OPS:
            labels[i.argval] = f"label{label_index}"
            label_index += 1

    for i in dis.get_instructions(obj):
        label = ""

        if i.arg is not None:
            arg = i.arg
        else:
            arg = ""

        if i.opname in JUMP_OPS:
            if i.is_jump_target:
                label = labels[i.offset] + ":"

            print(
                    "{}{:>7} {:<20} {}".format(
                        "\t"*indent_level,
                        label,
                        i.opname,
                        labels[i.argval],
                    )
            )

        elif i.is_jump_target:
            label = labels[i.offset] + ":"
            print(
                    "{}{:>7} {:<20} {}".format(
                        "\t"*indent_level,
                        label,
                        i.opname,
                        i.arg if i.arg is not None else "",
                    )
            )

        else:
            print(
                    "{}{:>7} {:<20} {}".format(
                        "\t"*indent_level,
                        label,
                        i.opname,
                        arg,
                    )
            )

    print(f"{indentation}END\n")


def main():
    if len(sys.argv) > 2:
        print("usage: disassembler <module>")
        sys.exit(1)
    module_name = os.path.splitext(sys.argv[1])[0]
    module = importlib.import_module(module_name)
    disassemble(module.main)


if __name__ == "__main__":
    main()
