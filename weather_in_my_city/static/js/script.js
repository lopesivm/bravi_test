var server_addr = 'http://localhost:5000';

function getCityWeather() {
    city_name = document.getElementById('city_name').value
    document.getElementById('city_not_found').style.display='none';
    document.getElementById('table_container').style.display='none';
    document.getElementById('loader').style.display='block';
    var xhr = new XMLHttpRequest();
    xhr.open('GET', server_addr + '/api/weather?city_name=' + city_name);
    xhr.onload = function() {
        document.getElementById('loader').style.display='none'
        if (xhr.status === 200) {
            document.getElementById('table_container').innerHTML=JSON.parse(xhr.response).data
            document.getElementById('table_container').style.display='block';
        }else{
            document.getElementById('failure_reason').innerHTML=JSON.parse(xhr.response).data
            document.getElementById('city_not_found').style.display='block';
        }
    };
    xhr.send();
}