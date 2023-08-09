import argparse
import json
import logging

import numpy as np
import paho.mqtt.client as mqtt

import config
from decawave import DecawaveModule
import geotools
import helpers
from kalman import EKF


def on_output(
        data: bytes, 
        client: mqtt.Client,
        logger: logging.Logger, 
        ekf: EKF = None
    ):
    """
    Called on the output of the 'les' shell command.

    :param bytes data: Output data of the 'les' shell command.
    :param object client: An instance of the MQTT client class.
    :param Logger logger: Logger object.
    :param object ekf: An instance of the Kalman filter class.

    """
    # Parse and validate the output data.
    output = data.decode().replace("\r\n", "")
    isvalid = helpers.validate(output)
    if isvalid is False:
        return
    
    meas = helpers.read_measurements(output)

    # Position calculated by the Decawave system.
    px = meas.px
    py = meas.py
    pz = meas.pz
    
    # Use extended Kalman filter to compute the position.
    if ekf:
        z = np.array([meas.r1, meas.r2, meas.r3, meas.r4]).T
        ekf.predict()
        ekf.update(z)
        px = ekf.x[0]
        py = ekf.x[2]
        pz = ekf.x[4]

    logger.info(json.dumps({"px": px, "py": py, "pz": pz, "meas": output}))
    
    # Send the position to the MQTT broker.
    lat, lon = geotools.compute_lat_lon(px, py)
    position = {"name": "decawave", "lat": lat, "lon": lon}
    client.publish(config.MQTT_TOPIC, json.dumps(position))


def main():
    # Parse the command line arguments.
    parser = argparse.ArgumentParser("Decawave reader")
    parser.add_argument("-kf", action="store_true", help="use Kalman filter")
    args = parser.parse_args()

    # Logging.
    logging.basicConfig(
        filename=config.LOGGING_FILENAME,
        format=config.LOGGING_FORMAT,
        level=logging.INFO
    )
    logger = logging.getLogger()

    # MQTT client.
    client = mqtt.Client(config.MQTT_CLIENT_ID)
    client.connect(host=config.MQTT_HOST, port=config.MQTT_PORT)

    # Extended Kalman Filter (EKF).
    ekf = None
    if args.kf:
        ekf = EKF(config.TIMESTEP, config.RANGE_STD_DEVIATION)

    # Read data from the Decawave module over the serial port.
    dwm = DecawaveModule()
    dwm.open()
    dwm.les(datahandler=on_output, client=client, logger=logger, ekf=ekf)
    dwm.les()
    dwm.close()

    client.disconnect()


if __name__ == "__main__":
    main()
