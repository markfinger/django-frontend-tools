var fs = require('fs');
var UglifyJS = require('uglify-js');

var service = function(req, res) {
	var js = req.query.js;

	var options = req.query.options;
	if (options) {
		options = JSON.parse(options);
	} else {
		options = {};
	}

	if (js) {
		options.fromString = true;
	} else {
		var pathToFile = req.query.path_to_file;
		if (!fs.existsSync(pathToFile)) {
			var message = 'The file specified by path_to_file, "' + pathToFile + '", cannot be found.';
			res.status(500).send(message);
			console.error(new Error(message));
			return;
		}
		js = pathToFile;
	}

	try {
		var output = UglifyJS.minify(js, options).code;
	} catch(err) {
		res.status(500).send(err);
		console.error(new Error(err));
		return;
	}

	res.send(output);
};

module.exports = service;