import sublime
import sublime_plugin

class PeerRefreshViewCommand(sublime_plugin.TextCommand):
	def run(self, edit, data, viewport):
		# Refresh view title
		if (data == None):
			return

		self.view.set_name(data[0])

		# Refresh view content
		region = sublime.Region(0, self.view.size())
		self.view.replace(edit, region, data[1])

		# Refresh view viewport
		self.view.set_viewport_position(viewport)
