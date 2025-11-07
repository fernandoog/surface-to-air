# Surface to Air

A citizen science project for air quality monitoring and visualization, developed for NASA Space Apps Challenge 2019.

## Description

Surface to Air is a comprehensive system that unifies air quality data from NASA and other public, private, and collaborative networks into a single platform (Simple Data Pollution Realtime Network - SRP Network). The project includes IoT sensor prototypes, data processing platforms, and visualization tools.

## Challenge

This project was developed for the [NASA Space Apps Challenge 2019 - Surface Air Quality Mission](https://2019.spaceappschallenge.org/challenges/living-our-world/surface-air-quality-mission/details).

## Components

### CO2nnector

A system designed to make people aware of air pollution problems. It includes:

- **Data Unification**: Combines data from NASA with other public, private, and collaborative networks
- **IoT Sensor Prototypes**: Wearable and stationary sensors for citizens to join the project
- **Real-time Data Sharing**: Platform for sharing sensor data in real-time for use in apps and websites
- **Machine Learning**: Predictive models for air quality (see `prediction/` directory)
- **Web Interface**: Flask-based server for data visualization and management

### aqmap

A data visualization tool for air quality data using Leaflet maps rendered with P5.js and Mappa libraries.

**Features:**
- Interactive map visualization
- Grid-based data representation (width/10 * height/10)
- Real-world coordinate projection (longitude/latitude)
- Dynamic updates based on time and location
- Color-coded visualization: green (0 minutes of life lost per day) to red (20+ minutes)

### srpnetwork

The Simple Data Pollution Realtime Network - a centralized platform for all air quality data.

### wareabledevice

MicroPython-based sensor device prototype software for ESP32.

## Installation

### CO2nnector Server

1. Navigate to `CO2nnector/srpnetwork/`
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python srpserver.py
```

### aqmap

1. Navigate to `aqmap/`
2. Open `index.html` in a web browser
3. Ensure the data server is running and accessible

### Wearable Device

1. Flash MicroPython to your ESP32
2. Upload files from `wareabledevice/` to the device
3. Configure WiFi and sensor connections

## Project Structure

```
surface-to-air/
├── CO2nnector/          # Main project components
│   ├── data/           # Data loading scripts
│   ├── prediction/     # ML models for air quality prediction
│   ├── srpnetwork/    # Flask web server
│   └── wareabledevice/ # ESP32 MicroPython code
├── aqmap/              # Visualization tool
└── Introduction/       # Project documentation
```

## Technologies

- **Backend**: Python, Flask, MicroPython
- **Frontend**: HTML, JavaScript, P5.js, Mappa, Leaflet
- **Machine Learning**: TensorFlow/Keras (H5 models)
- **Hardware**: ESP32, DHT11, MQ2 sensors
- **Data**: NASA APIs, public air quality networks

## Demo

Watch the project demo: [YouTube Video](https://www.youtube.com/watch?v=-5I2oxcQu9o)

## Author

Fernando Ortega Gorrita (@fernandoog)

Developed as part of NASA Space Apps Challenge 2019 - Madrid team.

## License

See LICENSE file for details.
