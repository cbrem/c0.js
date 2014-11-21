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

// Clear the terminal, and run the code currently in the editor in a fresh
// session.
function run() {
  _term.clear();
  _term.echo(GREETING);

  _session = new Session(_editor.getValue());
  _session.start();
}


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
  _term = $('#term').terminal(_onCommand, {
    prompt: '--> ',
    greetings: GREETING
  });

  // Set up editor.
  _editor = ace.edit('editor');
  _editor.setTheme("ace/theme/twilight");
  _editor.getSession().setMode("ace/mode/c_cpp");
  _editor.setValue(DEFAULT_CODE);

  // Start an initial session.
  _session = new Session();
  _session.start();
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
var _editor = null;
var _term = null;
var DEFAULT_CODE = 'int main() {\n\treturn 0;\n}';
var GREETING = 'Welcome to c0.js!\n';
var RUN_GREETING = 'Thanks for the code!\n';

// Event handlers.
$(document).ready(_onReady);
$(window).unload(_onUnload);
