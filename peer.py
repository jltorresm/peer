import http.client
import urllib
import json
from . import utils

class Client:
	SENDER = 0
	CONSUMER = 1

	def __init__(self, type):
		# Load server URL from settings
		self.url = utils.settings().get('peer_server_url')

		# Type of client
		self.type = type;

		# Obj var that will hold the current topic id
		self.topicId = None

		# Init the http connection
		self.conn = http.client.HTTPConnection(self.url)
		self.headers = {"Content-type": "application/json"}

	def createTopic(self):
		params = urllib.parse.urlencode({})

		try:
			self.conn.request('POST', "/topic", params, self.headers)
			response = self.conn.getresponse()

			encoding = response.headers.get_content_charset('utf-8')

			if (response.status != 200):
				utils.echo('Error ' + str(response.status) + ' (' + response.reason + '): ' + response.read().decode(encoding))
				return

			body = json.loads(response.read().decode(encoding))

			self.topicId = body['uuid']
			utils.echo('Session Created with id: ' + self.topicId)
		except Exception as e:
			utils.handleError(e, True)
			raise e

	def subscribeToTopic(self, topicId):
		self.topicId = topicId
		utils.echo('subscribe topic: ' + topicId)

	def syncContent(self, data = None, title = None):
		params = json.dumps({'data': data, 'title': title})
		method = 'GET' if data == None else 'PUT'

		try:
			self.conn.request(method, "/topic/" + self.topicId + '/content', params, self.headers)
			response = self.conn.getresponse()

			encoding = response.headers.get_content_charset('utf-8')

			if ((method == 'PUT' and response.status != 204) or (method == 'GET' and response.status != 200)):
				utils.echo('Error ' + str(response.status) + ' (' + response.reason + '): ' + response.read().decode(encoding))
				return

			body = response.read().decode(encoding)

			if (len(body) == 0):
				return

			body = json.loads(body)

			return (body['title'], body['data'])
		except Exception as e:
			utils.handleError(e, True)

	def syncViewport(self, x = None, y = None):
		params = json.dumps({'x': x, 'y': y})
		method = 'GET' if x == None else 'PUT'

		try:
			self.conn.request(method, "/topic/" + self.topicId + '/viewport', params, self.headers)
			response = self.conn.getresponse()

			encoding = response.headers.get_content_charset('utf-8')

			if ((method == 'PUT' and response.status != 204) or (method == 'GET' and response.status != 200)):
				utils.echo('Error ' + str(response.status) + ' (' + response.reason + '): ' + response.read().decode(encoding))
				return

			body = response.read().decode(encoding)

			if (len(body) == 0):
				return

			body = json.loads(body)

			return (body["x"], body["y"])
		except Exception as e:
			utils.handleError(e, True)

	def closeTopic(self):
		params = urllib.parse.urlencode({})

		try:
			self.conn.request('DELETE', "/topic/" + self.topicId, params, self.headers)
			response = self.conn.getresponse()

			encoding = response.headers.get_content_charset('utf-8')

			if (response.status != 204):
				utils.echo('Error ' + str(response.status) + ' (' + response.reason + '): ' + response.read().decode(encoding))
				return

			utils.echo('Session Closed with id: ' + self.topicId)
			self.topicId = None;

		except Exception as e:
			utils.handleError(e)

	# Helper method for outsiders
	def getTopicId(self):
		return self.topicId;
