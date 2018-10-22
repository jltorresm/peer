import sublime
import sublime_plugin
import os
from threading import Timer
from . import peer
from . import utils

class PeerSenderCommand(sublime_plugin.TextCommand):
	# The wait in seconds to refresh data
	TICK = .300

	# Lock file
	PID = utils.plugin_directory + '/sending'

	# The view id
	VID = None

	def run(self, edit):
		self.init(edit)

	def init(self, edit):
		self.server = peer.Client(peer.Client.SENDER);

		try:
			self.server.createTopic()

			# Initialize file to keep process running
			utils.touch(self.PID)

			# Start the loop that syncs the content
			Timer(self.TICK, self.send).start()

			# Start the view to show the content
			PeerSenderCommand.VID = self.view.id()

			# Start visual aids for the user
			self.visualAid()
		except Exception as e:
			pass

	def send(self):
		# Get the data from the view
		region = sublime.Region(0, self.view.size())
		data = self.view.substr(region)

		if self.view.file_name() == None:
			title = self.view.name()
		else:
			title = os.path.basename(self.view.file_name())

		# Send it to the server
		try:
			self.server.syncContent(data, title)
			self.server.syncViewport(*self.view.viewport_position())
		except Exception as e:
			self.showError(e)

		if (utils.fileExists(self.PID)):
			Timer(self.TICK, self.send).start()
		else:
			self.server.closeTopic()

	def visualAid(self):
		# Show the current topic for sharing
		sublime.active_window().show_input_panel('Session Id', self.server.getTopicId(), None, None, None)
