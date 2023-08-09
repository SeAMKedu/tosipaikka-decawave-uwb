import config


class Measurements:
    """Range measurement class."""

    def __init__(self) -> None:
        # Measured ranges.
        self.r1 = 0
        self.r2 = 0
        self.r3 = 0
        self.r4 = 0
        # Estimated position.
        self.px = 0
        self.py = 0
        self.pz = 0
        # Quality factor.
        self.qf = 0


def read_measurements(output: str) -> Measurements:
    """
    Read the range measurements and the estimated position of the tag.

    :param str output: Output of the 'les' shell command.
    :return: An instance of the Measurements class.
    :rtype: object

    """
    measurements = Measurements()
    
    for item in output.split(" "):
        if item.startswith("le_us"):
            continue
        
        elif item.startswith("est"):
            position = item.split("[")[1].split("]")[0].split(",")
            measurements.px = float(position[0])
            measurements.py = float(position[1])
            measurements.pz = float(position[2])
            measurements.qf = int(position[3])
        
        else:
            anchor_id = item[0:4]
            measured_range = float(item.split("=")[1])
            if anchor_id == config.ID_ANCHOR1:
                measurements.r1 = measured_range
            elif anchor_id == config.ID_ANCHOR2:
                measurements.r2 = measured_range
            elif anchor_id == config.ID_ANCHOR3:
                measurements.r3 = measured_range
            elif anchor_id == config.ID_ANCHOR4:
                measurements.r4 = measured_range

    return measurements


def validate(output: str) -> bool:
    """
    Validate the output data of the 'les' shell command.

    :param str output: Output data of the 'les' shell command.
    :return: True, if data is valid, False otherwise.
    :rtype: bool

    """
    # The output is expected to contain 4 range measurements, value of
    # the le_us parameter, and the estimated position:
    # <meas1> <meas2> <meas3> <meas4> le_us=<value> est[<px>,<py>,<pz>,<qf>]
    items = output.split(" ")
    if not len(items) == 6:
        return False

    index = output.find("est")
    if index == -1:
        return False
    
    return True
