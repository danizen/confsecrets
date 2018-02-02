import sys
from collections import abc
import argparse
from Crypto import Random

memoized_commands = {}


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
		if name is None:
			name = func.__name__
		# associate the parser with the function
		func.parser = parser
		memoized_commands[name] = func
		return func
	return wrapper

def call_command(command, args):
	"""
	Calls a command, parsing its arguments if appropriate
	"""
	if command not in memoized_commands:
		sys.stderr.write('%s - not recognized\n' % command)
		return usage()
	else:
		func = memoized_commands[command]
		if func.parser is None:
			return func(args)
		else:
			opts = func.parser.parse_args(args)
			return func(opts)

def usage():
	sys.stderr.write('Usage: pbetool <command> [options]\n')
	return 1
	sys.exit(1)


@command
def help():
	for command in sorted(memoized_commands.keys()):
		func = memoized_commands[command]
		if func.parser is not None:
			desrciption = func.parser.description
		else:
			description = None
		if description:
			print('    %s ......... %s' % (command, description))
		else:
			print('    %s' % command)


@command
def salt():
	print(Random.new().read(8))


def main(args):
	if len(args) == 0:
		usage()
		sys.exit(1)
	retcode = call_command(args[0], args[1:])
	sys.exit(retcode)


if __name__ == '__main__':
	main(sys.argv[1:])