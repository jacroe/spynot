#!/usr/bin/python

import cherrypy, spynot
#cherrypy.engine.autoreload.unsubscribe()

class SpyNot():

	@cherrypy.expose
	def index(self):
		return """
<!doctype html>
<html>
<head>
<title>Don't blink.</title>
<link href="http://findicons.com/icon/download/146056/the_tardis/32/ico?id=317407" rel="icon" type="image/x-icon" />
<style>
  html {background:url(http://i.imgur.com/P9gvk3Hh.jpg) no-repeat center center fixed; background-size:cover}
</style>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
</head>
<body>
<article>
</article>
<script>
images = ["http://i.imgur.com/P9gvk3Hh.jpg", "http://i.imgur.com/ZaGrJMRh.jpg", "http://i.imgur.com/r9PgjFZh.jpg", "http://i.imgur.com/chfxpVph.jpg", "http://i.imgur.com/fANm8IGh.jpg", "http://i.imgur.com/HmRD9XIh.jpg"]
for (i = 0; i < images.length; i++)	new Image().src = images[i]
function updateBackground(url)
{
	$("html").css('background', 'url(' + url + ') no-repeat center center fixed');
	$("html").css('background-size', 'cover');
}
$(document).ready(function()
{
	setTimeout(function(){
		updateBackground(images[1]);
		document.title = "Blink and you're dead.";
	}, 3000);
	setTimeout(function(){
		updateBackground(images[2]);
		document.title = "They are fast. Faster than you can believe.";
	}, 13000);
	setTimeout(function(){
		updateBackground(images[3]);
		document.title = "Don't turn your back. Don't look away.";
	}, 15000);
	setTimeout(function(){
		updateBackground(images[4]);
		document.title = "And don't blink.";
	}, 30000);
	setTimeout(function(){
		updateBackground(images[5]);
		document.title = "Good luck.";
	}, 35000);
});
</script>
</body>
</html>"""

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
cherrypy.config.update({'server.socket_host': '127.0.0.1', 'server.socket_port': 9999, })
cherrypy.quickstart(SpyNot())