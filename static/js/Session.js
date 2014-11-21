/*
	The client-side representation of a coin session.
*/

/*
	TODO:
	* make sure that the lifecycle is followed correctly (sendLine after
	startSession, etc.)
*/

function Session() { }
Session.prototype = {
	// Creates a new session, and calls the success or failure callbacks as
	// appropriate.
	start: function(succ, fail) {
		$.ajax({
		    type: "POST",
		    url: "/start",
		    success: function(data) {
		    	console.log("sessionID", data, data.sessionID);
		    	this.sessionID = data.sessionID;
		    	succ && succ();
		    }.bind(this),
		    error: fail
		  });
	},

	// Sends a command line to this session.
	cmd: function(cmd, succ, fail) {
		 $.ajax({
		    type: "POST",
		    url: "/cmd/" + this.sessionID + "/" + encodeURIComponent(cmd),
		    success: succ
		 });
	},

	// Ends the session.
	end: function(succ, fail) {
		$.ajax({
		    type: "POST",
		    url: "/end/" + this.sessionID,
		    success: succ
		});
	}
};
