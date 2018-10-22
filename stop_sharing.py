import sublime
import sublime_plugin
from . import consumer
from . import sender
from . import utils

class PeerStopSharingCommand(sublime_plugin.WindowCommand):
	NONE = 0 # Why would i need this?
	CONSUME = 1
	SEND = 2
	BOTH = 3

	def run(self, which = 3):
		consume = which & PeerStopSharingCommand.CONSUME
		send = which & PeerStopSharingCommand.SEND

		if consume and utils.fileExists(consumer.PeerConsumerCommand.PID):
			utils.unlink(consumer.PeerConsumerCommand.PID)

		if send and utils.fileExists(sender.PeerSenderCommand.PID):
			utils.unlink(sender.PeerSenderCommand.PID)

