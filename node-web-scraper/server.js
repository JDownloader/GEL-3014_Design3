var express = require('express');
var fs = require('fs');
var request = require('request');
var cheerio = require('cheerio');
var app     = express();

app.get('/scrape', function(req, res){
	// Let's scrape Anchorman 2
	//url = 'http://www.imdb.com/title/tt1229340/';
	url = 'https://www.cia.gov/library/publications/the-world-factbook/geos/af.html';

	request(url, function(error, response, html){
		if(!error){
			var $ = cheerio.load(html);
			var category_data = [];
			var category = [];

			var title, release, rating;
			var json = { title : "", release : "", rating : ""};

			$('.category').filter(function(){
		        var data = $(this);
		        title = data.text();
		        

		        category.push(title);
		        
	        })
    
	        $('.category_data').filter(function(){
	        	
	        	var data = $(this);
	        	
	        	rating = data.text();

	        	category_data.push(rating);
	        })
		}

		json.title = category;
		json.rating = category_data;
		fs.writeFile('output.json', JSON.stringify(json, null, 4), function(err){
        	console.log('File successfully written! - Check your project directory for the output.json file');
        })

        res.send('Check your console!')
	})
})

app.listen('8081')
console.log('Magic happens on port 8081');
exports = module.exports = app; 	