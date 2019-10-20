def read_sensor():
    global temp, hum
    temp = hum = 0
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        if (isinstance(temp, float) and isinstance(hum, float)) or (isinstance(temp, int) and isinstance(hum, int)):
            msg = (b'{0:3.1f},{1:3.1f}'.format(temp, hum))
            hum = round(hum, 2)
            return (msg)
        else:
            return ('Invalid sensor readings.')
    except OSError as e:
        return ('Failed to read sensor.')


def web_page():
    html = """<!DOCTYPE HTML><html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
      html {
       font-family: Arial;
       display: inline-block;
       margin: 0px auto;
       text-align: center;
      }
      h2 { font-size: 3.0rem; }
      p { font-size: 3.0rem; }
      .units { font-size: 1.2rem; }
      .dht-labels{
        font-size: 1.5rem;
        vertical-align:middle;
        padding-bottom: 15px;
      }
    </style>
  </head>
  <body>
    <p>
      <img src="https://raw.githubusercontent.com/fernandoog/surface-to-air/master/CO2nnector/images/Logo.jpeg"> 
    </p>
    <p>
      <i class="fas fa-thermometer-half" style="color:#0101DF;"></i> 
      <span class="dht-labels">Temperature</span> 
      <span>""" + str(temp) + """</span>
      <sup class="units">&deg;C</sup>
    </p>
    <p>
      <i class="fas fa-tint" style="color:#00add6;"></i> 
      <span class="dht-labels">Humidity</span>
      <span>""" + str(hum) + """</span>
      <sup class="units">%</sup>
    </p>
    <p>
      <i class="fas fa-sad-tear"  style="color:#FF0000;"></i>
      <span class="dht-labels">Air Quality</span>
    </p>
  </body>
  </html>"""
    return html


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    print('Content = %s' % str(request))
    sensor_readings = read_sensor()
    print(sensor_readings)
    response = urequests.post("http://10.236.2.197:8888/sensor", data=sensor_readings)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
