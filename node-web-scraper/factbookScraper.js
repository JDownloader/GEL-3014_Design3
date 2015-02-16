var express = require('express');
var fs 		= require('fs');
var request = require('request');
var cheerio = require('cheerio');
var app     = express();
var rest 	= require('restler');

app.get('/scrape', function(req, res){

	var countryCodes = ["af", "sf", "al", "ag", "gm", "an", "ao", "ac", "sa", "ar", "am", "as", "au", "aj", "bf", "ba", "bg", "bb", "bo", "be", "bh", "bn",
						"bt", "bl", "bk", "bc", "br", "bx", "bu", "uv", "by", "cb", "cm", "ca", "cv", "ct", "ci", "ch", "cy", "co", "cn", "cf", "cg", "kn", 
						"ks", "cs", "iv", "hr", "cu", "da", "dj", "do", "eg", "es", "ae", "ec", "er", "sp", "en", "us", "et", "fi", "fr", "gb", "ga", "gg", 
						"gh", "gr", "gj", "gt", "gv", "pu", "ek", "gy", "ha", "ho", "hu", "cw", "fj", "rm", "bp", "in", "id", "iz", "ir", "ic", "ei", "is", 
						"it", "jm", "ja", "jo", "kz", "ke", "kg", "kr", "ku", "la", "lt", "lg", "le", "li", "ly", "ls", "lh", "lu", "mk", "ma", "my", "mi", 
						"mv", "ml", "mt", "mo", "mr", "mp", "mx", "fm", "md", "mn", "mg", "mj", "mz", "bm", "wa", "nr", "np", "nu", "ng", "ni", "ne", "nz", 
						"no", "mu", "ug", "uz", "pk", "ps", "pm", "pp", "pa", "pe", "rp", "nl", "pl", "po", "qa", "dr", "ro", "rs", "uk", "rw", "ws", "tp", 
						"sg", "ri", "se", "sl", "sn", "lo", "si", "so", "od", "su", "ce", "st", "sc", "rn", "vc", "sz", "sw", "ns", "wz", "sy", "ti", "tz", 
						"th", "cd", "ez", "tt", "to", "tn", "td", "ts", "tx", "tu", "tv", "up", "uy", "nh", "ve", "vm", "ym", "za", "zi"];


	countryCodes.forEach(scrapeCountryPage)
	res.send("Check outpout.json :)");


})

app.listen('8081')
console.log('To start, access http://localhost:8081/scrape');
exports = module.exports = app; 	




function scrapeCountryPage(countryCode) {
	console.log("processing country " + countryCode);
		request('https://www.cia.gov/library/publications/the-world-factbook/geos/' + countryCode +'.html', function(error, response, html){
			if(!error){
				var $ = cheerio.load(html);
				var entries = {country:"", fields:[]};

				entries.country = $('.region_name1').text();

				$('.category a').filter(function(){
		        	var json = {category:"", data:[]};

		        	var data = $(this);
		        	
		        	json.category = data.text();

		        	var fieldedCategory = data.parent().parent().parent().next('tr').find($('.category')).filter(function() {
		        		
		        		var category = $(this);

		        		var categoryKeyValue = category.text();

						var categoryValueOnly = category.find($('.category_data')).text();

						if(categoryValueOnly === undefined || categoryValueOnly === ''){
							categoryKeyValue += category.parent().find($('.category_data a')).text();
						}

		        		json.data.push(data.text() + " " + categoryKeyValue);
		        	});

		        	var topLevelCategory = data.parent().parent().parent().next('tr').find($('td > .category_data')).filter(function() {
		        		
		        		var category = $(this);

		        		var categoryValue = category.text();

		        		json.data.push(data.text() + " " + categoryValue);
		        	});

		        	entries.fields.push(json);
		        })

			}
			console.log("finished processing "+ countryCode);
				rest.postJson('http://localhost:9200/test/countries/', entries).on('complete', function(data, response) {
			  		console.log('Given to index');
			});
/*			fs.appendFile('output.json', JSON.stringify(entries, null, 4), function(err){
		    	console.log('File successfully written!');
		    })*/
		})
	console.log("Finished a loop ");
}