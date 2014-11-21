"""
	A coin session.

	TODO:
	* follow method naming conventions (start, cmd, end)?
	* how do we handle multi-line output?
	* how do we handle incomplete lines? i.e. the user sends what they think
	  is a complete line, but C0 expects more?
"""

import subprocess

class Session(object):
	def __init__(self, sessionID):
		self.sessionID = sessionID
		self.process = subprocess.Popen(
			'coin',
			shell=True,
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE,
			stderr=subprocess.STDOUT)

		# Consume header text.
		headerLines = 2
		for i in xrange(headerLines):
			self.process.stdout.readline()

	# Writes a command line, and returns the output to (STDOUT, STDERR).
	def cmd(self, line):
		self.process.stdin.write(line + "\n")

		# TODO: This is currently broken, because we pipe err to out
		# when we create the process. Is there some way to take the
		# output that comes from stderr?
		out = self.process.stdout.readline()
		err = ''

		# Strip the leading '->', as well as leading/trailing whitespace.
		# TODO: is this too aggressive?
		toStrip = '-> \n'
		return (out.strip(toStrip), err.strip(toStrip))

	# Ends a session.
	def end(self):
		self.process.kill()
