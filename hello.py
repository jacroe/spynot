#!/usr/bin/python

import cherrypy, spynot
#cherrypy.engine.autoreload.unsubscribe()

class SpyNot():

	@cherrypy.expose
	def index(self):
		return "SpyNot, playa."

	@cherrypy.expose
	def api(self, json=None):
		cherrypy.response.headers['Content-Type'] = 'application/json'
		return spynot.api(json)

cherrypy.quickstart(SpyNot())