# CSS Beautify for Sublime Text

CSS-Beautify is a Sublime Text 2 and 3 plugin allowing you to format your CSS code. The formatters are written in JavaScript, so you'll need something (node.js) to interpret JavaScript code outside the browser.

## Installation
First of all, be sure you have [node.js](http://nodejs.org/#download) installed in order to run the beautifier. After you've installed node.js, you will need to setup this plugin.
Each OS has a different `Packages` folder required by Sublime Text. Open it via Preferences -> Browse Packages, and copy this repository contents to the `Sublime-CSSBeautify` folder there.

The shorter way of doing this is:
### Through [Sublime Package Manager](http://wbond.net/sublime_packages/package_control)

* `Ctrl+Shift+P` or `Cmd+Shift+P` in Linux/Windows/OS X
* type `install`, select `Package Control: Install Package`
* type `prettify`, select `HTML-CSS-JS Prettify`

### Manually
Make sure you use the right Sublime Text folder. For example, on OS X, packages for version 2 are in `~/Library/Application\ Support/Sublime\ Text\ 2`, while version 3 is labeled `~/Library/Application\ Support/Sublime\ Text\ 3`.

These are for Sublime Text 3:

#### Mac
`git clone https://github.com/wangwen1220/css-beautify.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/Sublime-CSSBeautify`

#### Linux
`git clone https://github.com/wangwen1220/css-beautify.git ~/.config/sublime-text-3/Packages/Sublime-CSSBeautify`

#### Windows
`git clone https://github.com/wangwen1220/css-beautify.git %APPDATA%/Sublime\ Text\ 3/Packages/Sublime-CSSBeautify`

## Usage
Tools -> Command Palette (`Cmd+Shift+P` or `Ctrl+Shift+P`) and type `CSSBeautify`.

-- or --

`Ctrl+Shift+H` (or `Cmd+Shift+H` if you're on a Mac).

-- or --

Right click in the current buffer and select `CSS Beautify` -> 'Beautify CSS`.

-- or --

Open a HTML, CSS or JavaScript file, pop out the console in Sublime Text from View -> Show Console, and type `view.run_command("cssbeautify")`.

Writing commands in the console is ugly. Set up your own key combo for this, by going to Preferences -> Key Bindings - User, and adding a command in that array: `{ "keys": ["super+shift+h"], "command": "cssbeautify" }`. You can use any other command you want, thought most of them are already taken.

## Options
The plugin looks for a `.jsbeautifyrc` file in the same directory as the source file you're prettifying (or one directory above if it doesn't exist, or in your home folder if everything else fails) and uses those options along the default ones. [Here](https://github.com/einars/js-beautify/blob/master/js/config/defaults.json)'s an example of how it can look like.

These are the default options used by this plugin:
```javascript
{
  // Details: https://github.com/victorporof/Sublime-CSSBeautify#using-your-own-jsbeautifyrc-options
  // Documentation: https://github.com/einars/js-beautify/
  "html": {
    "brace_style": "collapse", // "expand", "end-expand", "expand-strict"
    "indent_char": " ",
    "indent_scripts": "keep", // "separate", "normal"
    "indent_size": 4,
    "max_preserve_newlines": 10,
    "preserve_newlines": true,
    "unformatted": ["a", "sub", "sup", "b", "i", "u"],
    "wrap_line_length": 0
  },
  "css": {
    "indent_char": " ",
    "indent_size": 4
  },
  "js": {
    "brace_style": "collapse", // "expand", "end-expand", "expand-strict"
    "break_chained_methods": false,
    "e4x": false,
    "eval_code": false,
    "indent_char": " ",
    "indent_level": 0,
    "indent_size": 4,
    "indent_with_tabs": false,
    "jslint_happy": false,
    "keep_array_indentation": false,
    "keep_function_indentation": false,
    "max_preserve_newlines": 10,
    "preserve_newlines": true,
    "space_before_conditional": true,
    "space_in_paren": false,
    "unescape_strings": false,
    "wrap_line_length": 0
  }
}
```

And here's how a `.jsbeautifyrc` file in your home folder could look like:
```javascript
{
  "html": {
    "indent_char": "\t",
    "indent_size": 1
  }
  "js": {
    "indent_char": " ",
    "indent_size": 2
  }
}
```

### Beautify on Save

To Beautify your code when saving the document, set the `format_on_save` setting to `true` in `CSSBeautify.sublime-settings`:

* `Ctrl+Shift+P` or `Cmd+Shift+P` in Linux/Windows/OS X
* type `cssbeautify`, select `Set Plugin Options`

To add different file extensions (like jsp/gsp/php) edit `scripts/run.js`.

# Links
#### [Sublime Text 3](http://www.sublimetext.com/3)
#### [cssbeautify](https://github.com/senchalabs/cssbeautify)
#### [node.js](http://nodejs.org/#download)

---

Steven

Email: wangwen1220@gmail.com

Blog: http://wangwen1220.github.com