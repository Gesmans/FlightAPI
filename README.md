# Raspberry Pi Flight Tracker

A Raspberry Pi project that pulls live aircraft data from the [OpenSky Network API](https://openskynetwork.github.io/opensky-api/) and displays overhead flight details — callsign and altitude — on a 16x2 I2C LCD.

## How it works

1. Query the OpenSky `states/all` endpoint with a geographic bounding box.
2. Parse the returned state vectors to extract callsign, latitude, longitude, and altitude.
3. Display the nearest/first matched aircraft's details on the LCD.

## Hardware

- Raspberry Pi 5 (with GPIO header)
- 16x2 LCD with PCF8574 I2C backpack
- Breadboard + jumper wires

## Wiring

| LCD Pin | Raspberry Pi Pin        |
|---------|--------------------------|
| GND     | GND (physical pin 6)    |
| VCC     | 5V (physical pin 2/4)   |
| SDA     | GPIO2 (physical pin 3)  |
| SCL     | GPIO3 (physical pin 5)  |

## Setup

### 1. Enable I2C

```bash
sudo raspi-config
# Interface Options → I2C → Enable, then reboot
```

### 2. Confirm the LCD is detected

```bash
sudo apt install -y i2c-tools
i2cdetect -y 1
```

You should see a hex address (e.g. `0x27`) appear in the grid — this is your LCD's I2C address.

### 3. Install dependencies

```bash
sudo apt install -y python3-pip
pip3 install RPLCD smbus2 requests --break-system-packages
```

## Configuration

Set your bounding box coordinates in the script (`lamin`, `lomin`, `lamax`, `lomax`) to cover the area you want to monitor. Example — a box covering Basingstoke, Reading, Farnham, and Tadley:

```python
params = {
    "lamin": 51.19, "lomin": -1.17,
    "lamax": 51.48, "lomax": -0.77
}
```

Update the LCD address in the script to match what `i2cdetect` reported (default assumed: `0x27`).

## Usage

```bash
python3 flight_tracker.py
```

The script polls the OpenSky API, extracts details for a matched aircraft, and writes the callsign (line 1) and altitude (line 2) to the LCD.

## Data source

Live aircraft state vectors are provided by [OpenSky Network](https://opensky-network.org/), a non-profit crowdsourced ADS-B receiver network. See the [state vector field reference](https://openskynetwork.github.io/opensky-api/rest.html#response) for what each value in a returned array represents.

## Notes

- Anonymous API access is rate-limited; consider registering an OpenSky client for higher limits.
- Callsigns may contain trailing whitespace or be empty/`null` — handle both cases before display.
- A 16x2 display only holds so much — this project shows first-match details, not every aircraft in the box.

## License

MIT
