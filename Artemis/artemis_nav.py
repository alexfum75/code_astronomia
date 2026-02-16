import datetime


class ArtemisObject(object):

    def setTimeStamp(self, timestamp):
        self.artemis_date = timestamp

    def setPos(self, tuple_pos):
        self.pos_x, self.pos_y, self.pos_z = tuple_pos

    def getPos(self):
        return self.pos_x, self.pos_y, self.pos_z

    def getSpeed(self):
        return self.speed_x, self.speed_y, self.speed_z

    def setSpeed(self, tuple_speed):
        self.speed_x, self.speed_y, self.speed_z = tuple_speed

    def setAttitude(self, tuple_attitude):
        self.att_x, self.att_y, self.att_z = tuple_attitude

    def getArtemisDate(self):
        return self.artemis_date

    def __init__(self):
        self.artemis_date = 0

        self.pos_x, self.pos_y, self.pos_z = 0.0, 0.0, 0.0
        self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
        self.att_x, self.att_y, self.att_z = 0.0, 0.0, 0.0

    def printStateVector(self):
        print(f'time: [{self.artemis_date}]'
              f' pos: [{self.pos_x}, {self.pos_y}, {self.pos_z}]'
              f' speed: [{self.speed_x}, {self.speed_y}, {self.speed_z}]'
              f' attitude: [{self.att_x}, {self.att_y}, {self.att_z}]')
