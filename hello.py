#!/usr/bin/python

import cherrypy, spynot
#cherrypy.engine.autoreload.unsubscribe()

class SpyNot():

	@cherrypy.expose
	def index(self):
		return "YOU SHALL NOT PASS!"

	@cherrypy.expose
	def api(self, json=None):
		cherrypy.response.headers['Content-Type'] = 'application/json'
		if json is None and cherrypy.request.method == "POST":
			body = cherrypy.request.body.read()
			print body
			return spynot.api(body)
		else:
			print json
			return spynot.api(json)

cherrypy.quickstart(SpyNot())