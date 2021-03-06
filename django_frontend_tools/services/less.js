var fs = require('fs');
var less = require('less');

var service = function(data, response) {
	var pathToFile = data.path_to_file;

	if (!fs.existsSync(pathToFile)) {
		var message = 'The file specified by path_to_file, "' + pathToFile + '", cannot be found.';
		response.status(500).send(message);
		console.error(new Error(message));
		return;
	}

	var options = data.options;
	if (options) {
		options = JSON.parse(options);
	} else {
		options = {};
	}

	var lessInput = fs.readFileSync(pathToFile);
	lessInput = lessInput.toString('utf-8');

	options.filename = pathToFile;

	less.render(lessInput, options)
		.then(function(output) {
			// output.css = string of css
			// output.map = string of sourcemap
			// output.imports = array of string filenames of the imports referenced
			response.send(output.css);
		},
		function(error) {
			response.status(500).send(error);
			console.error(new Error(error));
		});
};

module.exports = service;