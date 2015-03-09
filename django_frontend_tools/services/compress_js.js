var fs = require('fs');
var UglifyJS = require('uglify-js');

var service = function(data, response) {
	console.log('in js service')
	var js = data.js;

	var options = data.options;
	if (options) {
		console.log(options)
		options = JSON.parse(options);
	} else {
		options = {};
	}

	if (js) {
		options.fromString = true;
	} else {
		var pathToFile = data.path_to_file;
		if (!fs.existsSync(pathToFile)) {
			var message = 'The file specified by path_to_file, "' + pathToFile + '", cannot be found.';
			response.status(500).send(message);
			console.error(new Error(message));
			return;
		}
		js = pathToFile;
	}

	try {
		var output = UglifyJS.minify(js, options).code;
	} catch(err) {
		response.status(500).send(err);
		console.error(new Error(err));
		return;
	}

	response.send(output);
};

module.exports = service;