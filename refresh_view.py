import sublime
import sublime_plugin

class PeerRefreshViewCommand(sublime_plugin.TextCommand):
	def run(self, edit, data, viewport, selection):
		# Refresh view title
		if (data == None):
			return

		self.view.set_name('📡 ' + data[0])

		# Refresh view content
		region = sublime.Region(0, self.view.size())
		self.view.replace(edit, region, data[1])

		# Refresh view viewport
		self.view.set_viewport_position(viewport)

		# Refresh view selection
		regions = [sublime.Region(sel['a'], sel['b']) for sel in selection]
		self.view.sel().clear()
		self.view.sel().add_all(regions)
