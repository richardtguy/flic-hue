class TerminalLog:

	# ANSI escape codes for text colours
	RED = '\033[31m'
	GREEN = '\033[32m'
	YELLOW = '\033[33m'
	RESET = '\033[0m'

	def print_to_log(self, colour, status, msg):
		string = '[{}{:^4}'+self.RESET+'] {}'
		print(string.format(colour, status, msg))

	def err(self, message):
		self.print_to_log(self.RED, 'Fail', message)

	def success(self, message):
		self.print_to_log(self.GREEN, 'OK', message)

	def warning(self, message):
		self.print_to_log(self.YELLOW, 'Warn', message)

	def info(self, message):
		print(message)
