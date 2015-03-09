var fs = require('fs');
var CleanCSS = require('clean-css');

var service = function(req, res) {
	var css = req.query.css;
	if (!css) {
		var pathToFile = req.query.path_to_file;
		if (!fs.existsSync(pathToFile)) {
			var message = 'The file specified by path_to_file, "' + pathToFile + '", cannot be found.';
			res.status(500).send(message);
			console.error(new Error(message));
			return;
		}
		css = fs.readFileSync(pathToFile);
	}

	var options = req.query.options;
	if (options) {
		options = JSON.parse(options);
	}

	try {
		var output = new CleanCSS(options).minify(css).styles;
	} catch(err) {
		res.status(500).send(err);
		console.error(new Error(err));
		return;
	}

	res.send(output);
};

module.exports = service;