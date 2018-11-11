//first example using ajax
$(function (){
	var $cities = $('#cities');
	var $city = $('#city');

	function addCity(city_data) {
		$cities.append(`<tr><td><img src="http://openweathermap.org/img/w/${city_data.icon}.png" alt="Image"></td> <td><b>${city_data.city}</b><br/> ${city_data.temperature}°C <br />${city_data.description}</td></tr>`);
	}

	$.ajax({
		type: 'GET',
		url: 'https://uisnrbk429.execute-api.eu-west-1.amazonaws.com/dev/weather',
		success: function (weather_data){
			$.each(weather_data, function(id, city_data){
				addCity(city_data);
			});
		},
		error: function (){
			alert('error loading weather');
		}
	});

	$('#add-city').on('click', function(){
		var addcity = {
			city: $city.val(),
		};
		$.ajax({
			type: 'POST',
			contentType: "application/json",
			url: 'https://uisnrbk429.execute-api.eu-west-1.amazonaws.com/dev/weather',
			data: JSON.stringify(addcity),
			success: function (city_data){
				if(city_data){
					addCity(city_data);
				}
			},
			error: function (){
				alert('error saving new city, check if it already exists');
			}
		});
	});
});

// Another way using fetch
// const api = 'https://uisnrbk429.execute-api.eu-west-1.amazonaws.com/dev';
// var $cities = $('#cities') 
//   $(document).ready(function () {
//     fetch(api + '/weather')
//       .then(res => res.json())
//       .then((result) => {
//         console.log(result)
//         result.weather.map(wcity => $cities.append(`<tr><td><img src="http://openweathermap.org/img/w/${wcity.icon}.png" alt="Image"></td> <td><b>${wcity.city}</b><br/> ${wcity.temperature} F <br />${wcity.description}</td></tr>`))
//       });
//   })