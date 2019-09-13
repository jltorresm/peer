import sublime
import sublime_plugin
from threading import Timer
from . import peer
from . import utils

class PeerConsumerCommand(sublime_plugin.WindowCommand):
	# The wait in seconds to refresh data
	TICK = .300

	# Lock file
	PID = utils.plugin_directory + '/consuming'

	# The view id
	VID = None

	def run(self):
		self.window.show_input_panel('Enter Session Id', '', self.init, None, None)

	def init(self, topic):
		self.server = peer.Client(peer.Client.CONSUMER);

		self.server.subscribeToTopic(topic);

		# Initialize file to keep process running
		utils.touch(self.PID)

		# Start the loop that syncs the content
		Timer(self.TICK, self.consume).start()

		# Start the view to show the content
		self.session = self.initView()
		PeerConsumerCommand.VID = self.session.id()

	def consume(self):
		data = self.server.syncContent()
		viewport = self.server.syncViewport()
		selection = self.server.syncSelection()

		self.session.run_command("peer_refresh_view", {"data": data, "viewport": viewport, "selection": selection})

		if (utils.fileExists(self.PID)):
			Timer(self.TICK, self.consume).start()
		else:
			utils.echo('Finished receiving from session ' + self.server.getTopicId())

	def initView(self):
		view = self.window.new_file()
		view.set_name('Getting Content...')
		return view
