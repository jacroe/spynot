#!/usr/bin/python

# Do not remove
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

import sys

from config import *
from googleplay import GooglePlayAPI
import json as libjson

def GetDetails(packageName):
	api = GooglePlayAPI(ANDROID_ID)
	api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)

	try:
		message = api.toDict(api.details(packageName))
	except:
		print "Error: something went wrong."
		return
	
	if "docV2" not in message:
		return dict(method="GetDetails", id=1, searchString=packageName, GooglePlayData=None)

	app = message['docV2']

	permissions = []
	if "permission" in app["details"]["appDetails"]:
		for i in range(len(app['details']['appDetails']['permission'])): permissions.append(app['details']['appDetails']['permission'][i])

	appData = dict(title=app['title'], author=app['creator'], description=app['descriptionHtml'], cost=app['offer'][0]['formattedAmount'], icon=app['image'][0]['imageUrl'], category=str(app['details']['appDetails']['appCategory'][0]), permissions=permissions, numDownloads=app['details']['appDetails']['numDownloads'], playRating="%.2f" % app['aggregateRating']['starRating'], url=app['shareUrl'], packageName=app['docid'])

	return dict(method="GetDetails", id=1, searchString=packageName, GooglePlayData=appData)

def GetAppPermissionsByCategory(category, subcategory, numResults=20):
	api = GooglePlayAPI(ANDROID_ID)
	api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)

	try:
		message = api.toDict(api.list(category, subcategory, str(numResults), None))
	except:
		print "Error: something went wrong."
		return
	
	if "doc" not in message:
		return dict(method="GetAppPermissionsByCategory", id=1, category=category, subcategory=subcategory, results=None)

	doc = message["doc"][0]
	appList = []
	for c in doc["child"]:
		appList.append(c["docid"])

	try:
		message = api.toDict(api.bulkDetails(appList))
	except:
		print "Error: something went wrong."
		return
	appList = []
	for i in range(len(message["entry"])):
		app = message["entry"][i]["doc"]
		permissions = []
		print app["docid"]
		if "permission" in app["details"]["appDetails"]:
			for i in range(len(app['details']['appDetails']['permission'])): permissions.append(app['details']['appDetails']['permission'][i])
		appList.append(dict(packageName=app["docid"], permissions=permissions))

	return dict(method="GetAppPermissionsByCategory", id=1, category=category, subcategory=subcategory, results=appList)

def SearchApp(searchString):
	api = GooglePlayAPI(ANDROID_ID)
	api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)

	try:
		message = api.toDict(api.search(searchString, None, None))
	except:
		print "Error: something went wrong. Maybe the nb_res you specified was too big?"
		return

	if "doc" not in message:
		return dict(method="SearchApp", id=1, searchString=searchString, results=None)

	doc = message["doc"][0]
	appList = []
	for c in doc["child"]:
		if "badgeForCreator" in c["annotations"]:
			badge = True
		else:
			badge = False
		appList.append(dict(title=c["title"], author=c["creator"], superDeveloper=badge, playRating="%.2f" % c["aggregateRating"]["starRating"], icon=c["image"][0]["imageUrl"], packageName=c["docid"]))

	return dict(method="SearchApp", id=1, searchString=searchString, results=appList)

def api(json=None):
	if json is None or json == "":
		return libjson.dumps(dict(method="NoJSON", id=None, response="bad"), indent=2)
	json = libjson.loads(json)

	if json["method"] == "GetDetails":
		if "searchString" in json:
			return libjson.dumps(GetDetails(json["searchString"]), indent=2)
		else:
			return libjson.dumps(dict(method=json["method"], id=json["id"], response="bad", reason="Missing 'searchString'"), indent=2)
	elif json["method"] == "SearchApp":
		if "searchString" in json:
			return libjson.dumps(SearchApp(json["searchString"]), indent=2)
		else:
			return libjson.dumps(dict(method=json["method"], id=json["id"], response="bad", reason="Missing 'searchString'"), indent=2)
	elif json["method"] == "GetAppPermissionsByCategory":
		if "category" in json and "subcategory" in json:
			if "numResults" in json:
				return libjson.dumps(GetAppPermissionsByCategory(json["category"], json["subcategory"], json["numResults"]), indent=2)
			else:
				return libjson.dumps(GetAppPermissionsByCategory(json["category"], json["subcategory"]), indent=2)
		else:
			return libjson.dumps(dict(method=json["method"], id=json["id"], response="bad", reason="Missing 'category' | 'subcategory'"), indent=2)
	else:
			return libjson.dumps(dict(method="NoValidMethod", id=json["id"], response="bad", reason="Method name not recognized."), indent=2)