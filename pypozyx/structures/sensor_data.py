#!/usr/bin/env python
"""pypozyx.structures.sensor_data - Contains container classes for data from the Pozyx's many sensors."""

from pypozyx.structures.byte_structure import ByteStructure
from pypozyx.structures.generic import XYZ

from pypozyx.definitions.constants import *


class Coordinates(XYZ):
    """
    Container for coordinates in x, y, and z (in mm).

    Useful in these functions:
        getCoordinates, setCoordinates
    """
    byte_size = 12
    data_format = 'iii'


class Acceleration(XYZ):
    """
    Container for acceleration in x, y, and z (in mg).

    Useful in these functions:
        getAcceleration_mg
    """
    physical_convert = POZYX_ACCEL_DIV_MG

    byte_size = 6
    data_format = 'hhh'


class Magnetic(XYZ):
    """
    Container for coordinates in x, y, and z (in uT).

    Useful in these functions:
        getMagnetic_uT
    """
    physical_convert = POZYX_MAG_DIV_UT

    byte_size = 6
    data_format = 'hhh'


class AngularVelocity(XYZ):
    """
    Container for angular velocity in x, y, and z (in dps).

    Useful in these functions:
        getAngularVelocity_dps
    """
    physical_convert = POZYX_GYRO_DIV_DPS

    byte_size = 6
    data_format = 'hhh'


class LinearAcceleration(XYZ):
    """
    Container for linear acceleration in x, y, and z (in mg), as floats.

    Useful in these functions:
        getLinearAcceleration_mg
    """
    physical_convert = POZYX_ACCEL_DIV_MG

    byte_size = 6
    data_format = 'hhh'

    def load(self, data, convert=1):
        if convert:
            self.x = float(data[0]) / physical_convert
            self.y = float(data[1]) / physical_convert
            self.z = float(data[2]) / physical_convert
        else:
            self.x = float(data[0])
            self.y = float(data[1])
            self.z = float(data[2])


class PositionError(XYZ):
    """
    Container for position error in x, y, z, xy, xz, and yz (in mm).

    Useful in these functions:
        getPositionError
    """
    physical_convert = 1
    byte_size = 12
    data_format = 'hhhhhh'

    def __init__(self, x=0, y=0, z=0, xy=0, xz=0, yz=0):
        """Initializes the PositionError object."""
        XYZ.__init__(self, x, y, z)
        self.xy = xy
        self.xz = xz
        self.yz = yz
        self.data = [x, y, z, xy, xz, yz]

    def load(self, data):
        XYZ.load(self, data[0:3])
        self.xy = data[3] / physical_convert
        self.xz = data[4] / physical_convert
        self.yz = data[5] / physical_convert

    def update_data(self):
        try:
            if self.data != [self.x, self.y, self.z, self.xy, self.xz, self.yz]:
                self.data = [self.x, self.y, self.z, self.xy, self.xz, self.yz]
        except:
            return

    def __str__(self):
        return 'X: {self.x}, Y: {self.y}, Z: {self.z}, XY: {self.xy}, XZ: {self.xz}, YZ: {self.yz}'.format(self=self)


class Quaternion(XYZ):
    """
    Container for quaternion data in x, y, z and w.

    Useful in these functions:
        getQuaternion
    """
    physical_convert = POZYX_QUAT_DIV

    byte_size = 8
    data_format = 'hhhh'

    def __init__(self, w=0, x=0, y=0, z=0):
        """Initializes the Quaternion object."""
        XYZ.__init__(self, x, y, z)
        self.data = [w, x, y, z]
        self.w = w

    def load(self, data, convert=1):
        for i in range(len(data)):
            data[i] = float(data[i])
        XYZ.load(self, data[1:4], convert)
        self.data = data
        if convert:
            self.w = data[0] / self.physical_convert
        else:
            self.w = data[0]

    def update_data(self):
        try:
            if self.data != [self.w, self.x, self.y, self.z]:
                self.data = [self.w, self.x, self.y, self.z]
        except:
            return

    def __str__(self):
        return 'X: {self.x}, Y: {self.y}, Z: {self.z}, W: {self.w}'.format(self=self)


class EulerAngles(ByteStructure):
    """
    Container for euler angles as heading, roll, and pitch (in degrees).

    Useful in these functions:
        getEulerAngles_deg
    """
    physical_convert = POZYX_EULER_DIV_DEG

    byte_size = 6
    data_format = 'hhh'

    def __init__(self, heading=0, roll=0, pitch=0):
        """Initializes the EulerAngles object."""
        self.data = [heading, roll, pitch]
        self.heading = heading
        self.roll = roll
        self.pitch = pitch

    def load(self, data, convert=1):
        self.data = data
        if convert:
            self.heading = float(data[0]) / self.physical_convert
            self.roll = float(data[1]) / self.physical_convert
            self.pitch = float(data[2]) / self.physical_convert
        else:
            self.heading = float(data[0])
            self.roll = float(data[1])
            self.pitch = float(data[2])

    def update_data(self):
        try:
            if self.data != [self.heading, self.roll, self.pitch]:
                self.data = [self.heading, self.roll, self.pitch]
        except:
            return

    def __str__(self):

        return 'Heading: {self.heading}, Roll: {self.roll}, Pitch: {self.pitch}'.format(
            self=self)


class SensorData(ByteStructure):
    """
    Container for all sensor data.

    This includes, in order, with respective structure:
        - pressure : float
        - acceleration : Acceleration
        - magnetic : Magnetic
        - angular_vel : AngularVelocity
        - euler_angles : EulerAngles
        - quaternion : Quaternion
        - linear_acceleration: LinearAcceleration
        - gravity_vector: LinearAcceleration
        - temperature: UInt8

    Useful in these functions:
        getAllSensorData
    """
    byte_size = 49  # 4 + 6 + 6 + 6 + 6 + 8 + 6 + 6 + 1

    # 'I' + 'h'*3 + 'h'*3 + 'h'*3 + 'h'*3 + 'f'*4 + 'h'*3 + 'h'*3 + 'B'
    data_format = 'fhhhhhhhhhhhhhhhhhhhhhhB'

    def __init__(self, data=[0] * 24):
        """Initializes the SensorData object."""
        self.data = data
        self.pressure = data[0]
        self.acceleration = Acceleration(data[1], data[2], data[3])
        self.magnetic = Magnetic(data[4], data[5], data[6])
        self.angular_vel = AngularVelocity(data[7], data[8], data[9])
        self.euler_angles = EulerAngles(data[10], data[11], data[12])
        self.quaternion = Quaternion(data[13], data[14], data[15], data[16])
        self.linear_acceleration = LinearAcceleration(
            data[17], data[18], data[19])
        self.gravity_vector = LinearAcceleration(data[20], data[21], data[22])
        self.temperature = data[23]

    def load(self, data):
        self.pressure = float(data[0]) / POZYX_PRESS_DIV_PA
        self.acceleration.load(data[1:4])
        self.magnetic.load(data[4:7])
        self.angular_vel.load(data[7:10])
        self.euler_angles.load(data[10:13])
        self.quaternion.load(data[13:17])
        self.linear_acceleration.load(data[17:20])
        self.gravity_vector.load(data[20:23])
        self.temperature = int(data[23] / POZYX_TEMP_DIV_CELSIUS)

    def update_data(self):
        # all the others are datastructures that take care of themselves.
        try:
            if self.data[0] != self.pressure or self.data[23] != self.temperature:
                self.data[0] = self.pressure
                self.data[23] = self.temperature
        except:
            return
