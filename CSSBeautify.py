# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sublime, sublime_plugin
import os, sys, subprocess, codecs, webbrowser

try:
  import commands
except ImportError:
  pass

PLUGIN_FOLDER = os.path.dirname(os.path.realpath(__file__))
OPT_FILE = ".cssbeautify-opt"
SETTINGS_FILE = "CSSBeautify.sublime-settings"
KEYMAP_FILE = "Default ($PLATFORM).sublime-keymap"
OUTPUT_VALID = b"*** CSSBeautify output ***"

class CssbeautifyCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    if PLUGIN_FOLDER.find(u".sublime-package") != -1:
      # Can't use this plugin if installed via the Package Manager in Sublime
      # Text 3, because it will be zipped into a .sublime-package archive.
      # Thus executing scripts *located inside this archive* via node.js
      # will, unfortunately, not be possible.
      url = "https://github.com/victorporof/Sublime-HTMLPrettify#manually"
      msg = """You won't be able to use this plugin in Sublime Text 3 when \
installed via the Package Manager.\n\nPlease remove it and install manually, \
following the instructions at:\n"""
      sublime.ok_cancel_dialog(msg + url)
      webbrowser.open(url)
      return

    # Get the current text in the buffer.
    bufferText = self.view.substr(sublime.Region(0, self.view.size()))
    # ...and save it in a temporary file. This allows for scratch buffers
    # and dirty files to be beautified as well.
    namedTempFile = ".__temp__"
    tempPath = PLUGIN_FOLDER + "/" + namedTempFile
    print("Saving buffer to: " + tempPath)
    f = codecs.open(tempPath, mode='w', encoding='utf-8')
    f.write(bufferText)
    f.close()

    # Simply using `node` without specifying a path sometimes doesn't work :(
    settings = sublime.load_settings(SETTINGS_FILE)
    if exists_in_path("nodejs"):
      node = "nodejs"
    elif exists_in_path("node"):
      node = "node"
    else:
      node = settings.get("node_path")

    output = ""
    try:
      print("Plugin folder is: " + PLUGIN_FOLDER)
      scriptPath = PLUGIN_FOLDER + "/scripts/run.js"
      filePath = self.view.file_name()
      output = get_output([node, scriptPath, tempPath, filePath or "?"])

      # Make sure the correct/expected output is retrieved.
      if output.find(OUTPUT_VALID) == -1:
        print(output)
        cmd = node + " " + scriptPath + " " + tempPath + " " + filePath
        msg = "Command " + cmd + " created invalid output"
        raise Exception(msg)

    except:
      # Something bad happened.
      print("Unexpected error({0}): {1}".format(sys.exc_info()[0], sys.exc_info()[1]))

      # Usually, it's just node.js not being found. Try to alleviate the issue.
      msg = "Node.js was not found in the default path. Please specify the location." + node
      if sublime.ok_cancel_dialog(msg):
        open_cssbeautify_sublime_settings(self.view.window())
      else:
        msg = "You won't be able to use this plugin without specifying the path to Node.js."
        sublime.error_message(msg)
      return

    # Remove the output identification marker (first line).
    output = output[len(OUTPUT_VALID) + 1:]
    os.remove(tempPath)

    # We're done with beautifying, change the text shown in the current buffer.
    self.view.erase_regions("jshint_errors")

    if len(output) > 0:
      region = sublime.Region(0, self.view.size())
      text = output.decode("utf-8")
      self.view.replace(edit, region, text)

class PreSaveFormatListner(sublime_plugin.EventListener):
  def on_pre_save(self, view):
    settings = sublime.load_settings(SETTINGS_FILE)
    if settings.get("format_on_save") == True:
      view.run_command("cssbeautify")

class CssbeautifySetBeautifyPrefsCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    open_cssbeautify_opt(self.view.window())

class CssbeautifySetPluginOptionsCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    open_cssbeautify_sublime_settings(self.view.window())

class CssbeautifySetKeyboardShortcutsCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    open_jshint_sublime_keymap(self.view.window(), {
      "windows": "Windows", "linux": "Linux", "osx": "OSX"
    }.get(sublime.platform()))

class CssbeautifySetNodePathCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    open_cssbeautify_sublime_settings(self.view.window())

def open_cssbeautify_opt(window):
  window.open_file(PLUGIN_FOLDER + "/" + OPT_FILE)

def open_cssbeautify_sublime_settings(window):
  window.open_file(PLUGIN_FOLDER + "/" + SETTINGS_FILE)

def open_jshint_sublime_keymap(window, platform):
  window.open_file(PLUGIN_FOLDER + "/" + KEYMAP_FILE.replace("$PLATFORM", platform))

def exists_in_path(cmd):
  # Can't search the path if a directory is specified.
  assert not os.path.dirname(cmd)
  path = os.environ.get("PATH", "").split(os.pathsep)
  extensions = os.environ.get("PATHEXT", "").split(os.pathsep)

  # For each directory in PATH, check if it contains the specified binary.
  for directory in path:
    base = os.path.join(directory, cmd)
    options = [base] + [(base + ext) for ext in extensions]
    for filename in options:
      if os.path.exists(filename):
        return True

  return False

def get_output(cmd):
  if int(sublime.version()) < 3000:
    if sublime.platform() != "windows":
      # Handle Linux and OS X in Python 2.
      run = '"' + '" "'.join(cmd) + '"'
      return commands.getoutput(run)
    else:
      # Handle Windows in Python 2.

      # Hack to prevent console window from showing. Stolen from
      # http://stackoverflow.com/questions/1813872/running-a-process-in-pythonw-with-popen-without-a-console
      startupinfo = subprocess.STARTUPINFO()
      startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

      return subprocess.Popen(cmd, stdout=subprocess.PIPE, startupinfo=startupinfo).communicate()[0]
  else:
    # Handle all OS in Python 3.
    run = '"' + '" "'.join(cmd) + '"'
    return subprocess.check_output(run, stderr=subprocess.STDOUT, shell=True)
