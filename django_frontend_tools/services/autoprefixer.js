var autoprefixer = require('autoprefixer');

var service = function(req, res) {
	var css = req.query.css;

	var options = req.query['options'];
	if (options) {
		options = JSON.parse(options);
	}

	try {
		var output = autoprefixer(options).process(css).css;
	} catch(err) {
		res.status(500).send(e);
		console.error(new Error(err));
		return;
	}

	res.send(output);
};

module.exports = service;