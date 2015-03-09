var autoprefixer = require('autoprefixer');

var service = function(data, response) {
	var css = data.css;

	var options = data['options'];
	if (options) {
		options = JSON.parse(options);
	}

	try {
		var output = autoprefixer(options).process(css).css;
	} catch(err) {
		response.status(500).send(e);
		console.error(new Error(err));
		return;
	}

	response.send(output);
};

module.exports = service;