# communication_manager.py
#
# Managers that handle the actual network
# communication logic with the vehicles

import fabric

class CommunicationManagerInterface:
    """ Interface manager which all commands to vehicles are passing through """
    def __init__(self):
        pass

    def init_connection(self, host, user, password):
        pass

    def send_speed_order(self, vehicle, speed):
        pass

    def send_angle_order(self, vehicle, angle):
        pass

    def send_stop_order(self, vehicle):
        pass

### End of CommunicationManagerInterface ###


class SSHManager(CommunicationManagerInterface):
    """ Manager of ssh connections to vehicles """
    def __init__(self):
        self.host = 0
        self.user = 0
        self.password = 0
        self.config = 0
        self.connection = 0

    def init_connection(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.config = fabric.Config(overrides={'user': user, 'connect_kwargs': {'password': password}})
        self.connection = fabric.Connection(host, config=self.config)

    def send_speed_order(self, vehicle, speed):
        cmd = "python3 set_speed.py " + str(speed)
        self.connection.run(cmd)

    def send_angle_order(self, vehicle, angle):
        cmd = "python3 set_angle.py " + str(angle)
        self.connection.run(cmd)

    def send_stop_order(self, vehicle):
        self.connection.run("python3 set_angle 0")
        self.connection.run("python3 stop.py")

### End of SSHManager ###


class ITSG5Manager(CommunicationManagerInterface):
    """ Manager of 802.11p connections to vehicles """
    def __init__(self):
        pass

    def init_connection(self, host, user, password):
        pass

    def send_speed_order(self, vehicle, speed):
        pass

    def send_angle_order(self, vehicle, angle):
        pass

    def send_stop_order(self, vehicle):
        pass

### End of ITSG5Manager ###


