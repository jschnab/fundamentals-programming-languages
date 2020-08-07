import dis
import importlib
import os
import sys


JUMP_OPS = [
    "POP_JUMP_IF_FALSE",
    "JUMP_FORWARD",
]



def disassemble(func):
    if hasattr(func, "__code__"):
        co = func.__code__
    else:
        print(f"Can't make sense of '{func}', you should pass a function")

    print(f"Function: {co.co_name}/{co.co_argcount}")
    print(f"Constants: {', '.join(map(repr, co.co_consts))}")
    print(f"Locals: {', '.join(map(str, co.co_varnames))}")
    print(f"Globals: {', '.join(map(str, co.co_names))}")
    print(f"BEGIN")

    labels = {}
    label_index = 0
    indentation = 1

    for i in dis.get_instructions(func):
        label = ""

        if i.arg is not None:
            arg = i.arg
        else:
            arg = ""

        if i.opname in JUMP_OPS:
            labels[i.argval] = f"label{label_index}"
            label_index += 1
            print(
                    "{}{:>7}  {:<20} {}".format(
                        "\t"*indentation,
                        label,
                        i.opname,
                        labels[i.argval],
                    )
            )

        elif i.is_jump_target:
            label = labels[i.offset]
            print(
                    "{}{:>7}: {:<20} {}".format(
                        "\t"*indentation,
                        label,
                        i.opname,
                        i.arg,
                    )
            )

        else:
            print(
                    "{}{:>7}  {:<20} {}".format(
                        "\t"*indentation,
                        label,
                        i.opname,
                        arg,
                    )
            )

    print("END")


def main():
    if len(sys.argv) > 2:
        print("usage: disassembler <module>")
        sys.exit(1)
    module_name = os.path.splitext(sys.argv[1])[0]
    module = importlib.import_module(module_name)
    disassemble(module.main)


if __name__ == "__main__":
    main()
