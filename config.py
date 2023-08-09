# Logging.
LOGGING_FILENAME = "measurements.log"
LOGGING_FORMAT = "%(message)s"

# IDs of the Decawave anchor modules.
ID_ANCHOR1 = "14A6"
ID_ANCHOR2 = "1539"
ID_ANCHOR3 = "1B95"
ID_ANCHOR4 = "9D84"

# Coordinates of the Decawave anchor modules.
COORDINATES_ANCHOR1 = (0.00, 0.00, 0.77)
COORDINATES_ANCHOR2 = (0.00, 4.12, 0.77)
COORDINATES_ANCHOR3 = (4.17, 4.12, 0.77)
COORDINATES_ANCHOR4 = (4.17, 0.00, 0.77)

# Origin of the indoor positioning system.
ORIGIN_LAT = 62.78910212
ORIGIN_LON = 22.82212920
ORIGIN_HMSL = 45.521

# Angle difference between the vertical axis of the WGS84 reference system
# and Y axis of the indoor positioning system.
DELTA_AZIMUTH = -9.0

# Kalman filter configuration.
TIMESTEP = 0.1
RANGE_STD_DEVIATION = 0.05

# MQTT configurations.
MQTT_CLIENT_ID = "decawave"
MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "seamkiot/decawave"
