var fs = require('fs');
var CleanCSS = require('clean-css');
var rework = require('rework');
var reworkPluginUrl = require('rework-plugin-url');

var service = function(data, response) {
	var css = data.css;
	if (!css) {
		var pathToFile = data.path_to_file;
		if (!fs.existsSync(pathToFile)) {
			var message = 'The file specified by path_to_file, "' + pathToFile + '", cannot be found.';
			response.status(500).send(message);
			console.error(new Error(message));
			return;
		}
		css = fs.readFileSync(pathToFile);
		css = css.toString('utf-8');
	}

	var options = data.options;
	if (options) {
		options = JSON.parse(options);
	}

	var prependToRelativeUrls = data.prepend_to_relative_urls;
	if (prependToRelativeUrls) {
		css = rework(css)
			.use(reworkPluginUrl(function(url) {
				if (
					url.indexOf('data:') === 0 ||
					url.indexOf('http:') === 0 ||
					url.indexOf('https:') === 0 ||
					url.indexOf('/') === 0
				) {
					return url;
				}
				if (url.indexOf('./') === 0) {
					return prependToRelativeUrls + url.slice(2);
				}
				return prependToRelativeUrls + url;
			}))
			.toString('utf-8');
	}

	try {
		css = new CleanCSS(options).minify(css).styles;
	} catch(err) {
		response.status(500).send(err);
		console.error(new Error(err));
		return;
	}

	response.send(css);
};

module.exports = service;