import numpy as np

import config

X1, Y1, Z1 = config.COORDINATES_ANCHOR1
X2, Y2, Z2 = config.COORDINATES_ANCHOR2
X3, Y3, Z3 = config.COORDINATES_ANCHOR3
X4, Y4, Z4 = config.COORDINATES_ANCHOR4


class EKF:
    """
    Extended Kalman Filter (EKF) that uses a constant velocity model.

    :param float dt: Time step between states.
    :param float std_r: Standard deviation of the measured range.

    """
    def __init__(self, dt: float, std_r: float) -> None:
        # State x.
        self.x = np.array([0.1, 0.0, 0.1, 0.0, 0.1, 0.0]).T
        # State transition function F.
        self.F = np.array([
            [1, dt, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, dt, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, dt],
            [0, 0, 0, 0, 0, 1]
        ])
        # Covariance matrix P.
        self.P = np.array([100, 100, 100, 100, 100, 100])
        # Process noise matrix Q.
        self.Q = np.eye(6) * 1e-5
        # Measurement noise matrix R.
        self.R = np.eye(4) * np.power(std_r, 2)
        # Identity matrix I.
        self.I = np.eye(6)


    def HJacobian(self) -> np.ndarray:
        """Compute the partial derivative of the H at x."""

        x, y, z = (self.x[0], self.x[2], self.x[4])

        r1 = np.sqrt((x-X1)**2 + (y-Y1)**2 + (z-Z1)**2)
        r2 = np.sqrt((x-X2)**2 + (y-Y2)**2 + (z-Z2)**2)
        r3 = np.sqrt((x-X3)**2 + (y-Y3)**2 + (z-Z3)**2)
        r4 = np.sqrt((x-X4)**2 + (y-Y4)**2 + (z-Z4)**2)

        return np.array([
            [(x-X1)/r1, 0, (y-Y1)/r1, 0, (z-Z1)/r1, 0],
            [(x-X2)/r2, 0, (y-Y2)/r2, 0, (z-Z2)/r2, 0],
            [(x-X3)/r3, 0, (y-Y3)/r3, 0, (z-Z3)/r3, 0],
            [(x-X4)/r4, 0, (y-Y4)/r4, 0, (z-Z4)/r4, 0]
        ])


    def Hx(self) -> np.ndarray:
        """Compute the H at x."""

        x, y, z = (self.x[0], self.x[2], self.x[4])

        return np.array([
            np.sqrt((x-X1)**2 + (y-Y1)**2 + (z-Z1)**2),
            np.sqrt((x-X2)**2 + (y-Y2)**2 + (z-Z2)**2),
            np.sqrt((x-X3)**2 + (y-Y3)**2 + (z-Z3)**2),
            np.sqrt((x-X4)**2 + (y-Y4)**2 + (z-Z4)**2)
        ])


    def predict(self):
        """Predict the state and covarince matrix."""

        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q


    def update(self, z: np.ndarray):
        """
        Update the state and covarince matrix.

        :param ndarray z: Range measurements.
    
        """
        H = self.HJacobian()
        hx = self.Hx()
        # System uncertainty.
        S = H @ self.P @ H.T + self.R
        # Kalman gain.
        K = self.P @ H.T @ np.linalg.inv(S)
        # Residual.
        y = z - hx
        # State update.
        self.x = self.x + K @ y
        # Covariance matrix update.
        I_KH = self.I - K @ H
        self.P = I_KH @ self.P @ I_KH.T + K @ self.R @ K.T
