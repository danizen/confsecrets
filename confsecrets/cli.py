import sys
from collections import abc
import argparse
from Crypto import Random

COMMANDS = {}


def command(parser=None, name=None):
    """
    Decorator to make it intuitive and easy to make several commands in a single command-line,
    each with a different parser
    """
    # call the function that generates the parser, if that's needed
    if isinstance(parser, abc.Callable):
        parser = parser()
    # assert that the code is properly instrumented
    assert parser is None or isinstance(parser, argparse.ArgumentParser)

    def wrapper(func):
        # get the default name
        nonlocal name
        fname = name or func.__name__
        # associate the parser with the function
        func.parser = parser
        COMMANDS[fname] = func
        return func
    return wrapper


def call_command(name, args):
    """
    Calls a command, parsing its arguments if appropriate
    """
    if name not in COMMANDS:
        sys.stderr.write('%s - not recognized\n' % name)
        return usage()

    func = COMMANDS[name]
    if func.parser is None:
        return func(*args)

    opts = func.parser.parse_args(args)
    return func(opts)


def usage():
    sys.stderr.write('Usage: pbetool <command> [options]\n')
    return 1


@command(name='help')
def help_call():
    for name in sorted(COMMANDS.keys()):
        func = COMMANDS[name]
        if func.parser is not None:
            description = func.parser.description
        else:
            description = None
        if description:
            print('    %s ......... %s' % (name, description))
        else:
            print('    %s' % name)


@command()
def salt():
    print(Random.new().read(8))


def main(args):
    if not args:
        usage()
        sys.exit(1)
    if len(args) == 0:
        command = 'help'
        args = []
    elif len(args) == 1:
        command = args[0]
        args = []
    else:
        command = argss[0]
        args = args[1:]
    retcode = call_command(command, args)
    sys.exit(retcode)


if __name__ == '__main__':
    main(sys.argv[1:])
