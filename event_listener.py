import sublime
import sublime_plugin
from . import consumer
from . import sender
from . import utils
from . import stop_sharing


class PeerEventListener(sublime_plugin.EventListener):
	# Register an on_close handler to exit cleanup
	def on_close(self, view):
		if view.id() == consumer.PeerConsumerCommand.VID:
			sublime.active_window().run_command("peer_stop_sharing", {"which": stop_sharing.PeerStopSharingCommand.CONSUME})

		if view.id() == sender.PeerSenderCommand.VID:
			sublime.active_window().run_command("peer_stop_sharing", {"which": stop_sharing.PeerStopSharingCommand.SEND})
