import bottle

import urls
import session

# ID for the next session.
nextSessionID = 0

# Map from active session IDs to sessions.
sessions = {}

@bottle.post(urls.start)
def start():
	global nextSessionID
	global sessions
	sessions[nextSessionID] = session.Session(nextSessionID)
	nextSessionID += 1

	# Return the old sessionID.
	return {"sessionID": nextSessionID - 1}

@bottle.post(urls.cmd + '/<sessionID>/<cmd>')
def cmd(sessionID, cmd):
	try:
		session = sessions[int(sessionID)]
	except:
		# TODO: should we react differently here?
		return

	return session.cmd(cmd)

@bottle.post(urls.end + '/<sessionID>')
def end(sessionID):
	global sessions
	try:
		session = sessions[int(sessionID)]
	except:
		# TODO: should we do something different here?
		return

	session.end()
	del sessions[sessionID]

@bottle.route('/static/<filepath:path>')
def static(filepath):
    return bottle.static_file(filepath, root='static')

bottle.run(host='localhost', port=8080)
