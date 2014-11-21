"""
	A coin session.

	TODO:
	* follow method naming conventions (start, cmd, end)?
	* how do we handle multi-line output?
	* how do we handle incomplete lines? i.e. the user sends what they think
	  is a complete line, but C0 expects more?
	* use threading to handle multiple requests simultaneously?
	* todo: treat stderr seperately?
"""

import subprocess

WAITING_CHARS = '...'
FINISHED_CHARS = '\n-->'

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

		# TODO: this may need some work. How can we be sure that
		# the user hasn't just put '...' in a string?
		res = {}
		out = ''
		while True:
			if out.endswith(FINISHED_CHARS):
				res['out'] = out.strip(FINISHED_CHARS)
				break
			elif out.endswith(WAITING_CHARS):
				res['out_waiting'] = True
				break
			else:
				out += self.process.stdout.read(1)
		return res

	# Ends a session.
	def end(self):
		self.process.kill()
