import bottle

import urls
import session

# ID for the next session.
nextSessionID = 0

# Map from active session IDs to sessions.
sessions = {}

@bottle.post(urls.start)
@bottle.post(urls.start + '/<code>')
def start(code = ''):
	global nextSessionID
	global sessions
	sessions[nextSessionID] = session.Session(nextSessionID, code)
	nextSessionID += 1

	# Return the old sessionID.
	return {"sessionID": nextSessionID - 1}

@bottle.post(urls.cmd + '/<sessionID:int>/<cmd>')
def cmd(sessionID, cmd):
	try:
		session = sessions[sessionID]
	except:
		# TODO: should we react differently here?
		return bottle.HTTPError(404, "Invalid session ID.")

	return session.cmd(cmd)

@bottle.post(urls.end + '/<sessionID:int>')
def end(sessionID):
	global sessions
	try:
		session = sessions[sessionID]
	except:
		# TODO: should we do something different here?
		return bottle.HTTPError(404, "Invalid session ID.")

	session.end()
	del sessions[sessionID]

@bottle.route('/static/<filepath:path>')
def static(filepath):
    return bottle.static_file(filepath, root='static')

bottle.run(host='localhost', port=8080)
