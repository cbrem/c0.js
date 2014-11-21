/*
  TODO:
  * Figure out how to load a C0 file when the interpreter starts.
  * add foundation stuff
*/

/*
  TODO: interface methods:
    * run
    * download
    * upload
*/

// Run the code currently in the editor in a fresh session.
/*
TODO: for this to work, we need to be able to provide a source file when we
start the session

function run() {
  _session = new Session();
  _session.start();
}
*/


// Process a command typed into the terminal.
// Send the command to the current session.
function _onCommand(cmd, term) {
  if (!_session) {
    // TODO: this should never happen, right?
    return;
  }

  // TODO: fail callback?
  _session.cmd(cmd, function(res) {
    if (res.out_waiting) {
      term.set_prompt('... ');
    } else if (res.out) {
      term.set_prompt('--> ');
      term.echo(res.out);
    }
  }, undefined);
}

// Sets up the app.
function _onReady() {
  // Set up jQuery terminal.
  $('#term').terminal(_onCommand, {
    prompt: '--> ',
    greetings: 'Welcome to c0.js!\n'
  });

  // Start an initial session.
  _session = new Session();
  _session.start();

  // TODO: set up editor?
}

// Kills the current session (if any) when we leave the page.
function _onUnload() {
  if (_session) {
    // TODO: if we fail to end the session, keep trying?
    _session.end();
  }
}

// Globals.
var _session = null;

// Event handlers.
$(document).ready(_onReady);
$(window).unload(_onUnload);
