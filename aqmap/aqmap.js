const mappa = new Mappa('Leaflet');
var canvas;
var maximum_value;
var minimum_value;
const url = 'http://<SERVER_IP>:8888/data_prediction';
var from = 1502402400.0;
var to = from + 86400;
var positions = [];
var request_body = {
    to: to,
    from: from,
    positions: positions
};
var slider_value = 0;
var air_quality = [];
// Starting day for the slider
var offset = 1546300800
const options = {
    lat: 33.93,
    lng: -118.31,
    zoom: 13,
    style: "http://{s}.tile.osm.org/{z}/{x}/{y}.png"
}
var allowed_to_send = true;
var resend_counter = 0;

function preload() {
    positions = [];
    for (i = 0; i < width / 10; i++) {
        for (j = 0; j < height / 10; j++) {
            point = trainMap.map.containerPointToLatLng([i * 10, j * 10]);
            positions.push(JSON.parse('{"lat":' + point.lat + ', "lng":' + point.lng + '}'));
        }
    }
    request_body = {
        to: to,
        from: from,
        positions: positions
    };
    fetch(url, {
        method: 'POST',
        body: JSON.stringify(request_body),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).catch(error => console.error('Error:', error)).then(response => air_quality = response);
}

function setup() {
    frameRate(1);
    width = 800;
    height = 600;
    var canvas = createCanvas(width, height);
    trainMap = mappa.tileMap(options);
    trainMap.overlay(canvas);
    zoom = trainMap.zoom();
    minimum_value = 0;
    maximum_value = 30;
    // 30 means 91.25 hours of life lost per year here
    // 30 means 20 minutes of life lost per day here
    day = createSlider(1, 31, 1);
    day.position(300, 650);
    grid = Create2DArray(width / 10);
    trainMap.onChange(function() {
        if (allowed_to_send == true) {
            allowed_to_send = false;
            from = offset + (day.value() - 1) * 86400;
            to = from + 86400;
            positions = [];
            for (i = 0; i < width / 10; i++) {
                for (j = 0; j < height / 10; j++) {
                    point = trainMap.map.containerPointToLatLng([i * 10, j * 10]);
                    positions.push(JSON.parse('{"lat":' + point.lat + ', "lng":' + point.lng + '}'));
                }
            }
            request_body = {
                to: to,
                from: from,
                positions: positions
            };
            fetch(url, {
                method: 'POST',
                body: JSON.stringify(request_body),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(res => res.json()).catch(error => console.error('Error:', error)).then(response => air_quality = response);
        }
    });
}

function draw() {
    clear()
    if (slider_value != day.value()) {
        refreshData();
        slider_value = day.value();
    }
    getAirQualityData();
    drawGrid();
    colorMode(RGB);
    fill(0, 0, 0);
    textSize(15);
    if (resend_counter > 10) {
        allowed_to_send = true;
        resend_counter = 0;
    }
    resend_counter++;
}

function getAirQualityData() {
    var latitude = 0;
    var longitude = 0;
    var point_value = 0;
    for (let element of air_quality) {
        latitude = element[1];
        longitude = element[2];
        point_value = element[3];
        //Remove not valid positions
        if (isNaN(latitude) || isNaN(longitude)) {
            continue;
        }
        if (point_value > maximum_value) {
            var point_value = maximum_value;
        }
        pos = trainMap.latLngToPixel(latitude, longitude);
        //Out of the canvas
        if (pos.x < 0 || pos.y < 0 || pos.x >= width || pos.y >= height) {
            continue;
        }
        i = Math.floor(pos.x / 10);
        j = Math.floor(pos.y / 10);
        grid[i][j] = map(point_value, minimum_value, maximum_value, 90, 0);
    }
}

function refreshData() {
    if (allowed_to_send == true) {
        allowed_to_send = false;
        from = offset + (day.value() - 1) * 86400;
        to = from + 86400;
        positions = [];
        for (i = 0; i < width / 10; i++) {
            for (j = 0; j < height / 10; j++) {
                point = trainMap.map.containerPointToLatLng([i * 10, j * 10]);
                positions.push(JSON.parse('{"lat":' + point.lat + ', "lng":' + point.lng + '}'));
            }
        }
        request_body = {
            to: to,
            from: from,
            positions: positions
        };
        fetch(url, {
            method: 'POST',
            body: JSON.stringify(request_body),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).catch(error => console.error('Error:', error)).then(response => air_quality = response);
    }
}

function drawGrid() {
    colorMode(HSL);
    alpha = 0.3;
    noStroke();
    for (i = 0; i < width / 10; i++) {
        for (j = 0; j < height / 10; j++) {
            if (grid[i][j] !== undefined && grid[i][j] !== null) {
                selected_color = color(Math.round(grid[i][j]), 100, 50, alpha);
                grid[i][j] = null;
            } else {
                selected_color = color(90, 0, 50, alpha);
            }
            fill(selected_color);
            rect(i * 10, j * 10, 10, 10);
        }
    }
}

function Create2DArray(rows) {
    var arr = [];
    for (var i = 0; i < rows; i++) {
        arr[i] = [];
    }
    return arr;
}

function toFixed(value, precision) {
    var power = Math.pow(10, precision || 0);
    return String(Math.round(value * power) / power);
}