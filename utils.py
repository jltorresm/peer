import os
import sublime

settings_filename = 'Peer.sublime-settings'
plugin_directory = os.path.dirname(os.path.realpath(__file__))

def echo(msg):
	print ("[Peer Sender] %s" % msg)

def settings():
	return sublime.load_settings(settings_filename)

def save_settings():
	return sublime.save_settings(settings_filename)

def touch(path):
	file = open(path, 'w+')
	os.utime(path, None)
	file.close()

def fileExists(path):
	return os.path.isfile(path)

def unlink(path):
	return os.remove(path)

def handleError(exception, popupError = False):
	# If the error is of this type just silently ignore.
	# It's a request sent after the server connection was closed
	if exception.args[0] == "Request-sent":
		return

	errorMesage = "ERROR %s" % exception
	echo(errorMesage)

	sublime.active_window().run_command("peer_stop_sharing")

	if popupError:
		sublime.error_message("An error occurred: %s" % exception)

	return errorMesage
