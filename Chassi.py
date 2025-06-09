from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

class Chassi:
    def __init__(self):
        self.hub = PrimeHub()
        self.LEFT_MOTOR = Motor(port=Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
        self.RIGHT_MOTOR = Motor(port=Port.B)
        self.LEFT_COLOR_SENSOR = ColorSensor(port= Port.C)
        self.MIDDLE_COLOR_SENSOR = ColorSensor(port= Port.E)
        self.RIGHT_COLOR_SENSOR = ColorSensor(port= Port.D)
        self.ULTRASSONIC_SENSOR = UltrasonicSensor(port= Port.F)

        self.chassi = DriveBase(
            left_motor= self.LEFT_MOTOR,
            right_motor= self.RIGHT_MOTOR,
            wheel_diameter= 3.04, # Centimetros
            axle_track= 11.1 # Centimetros
        )
        self.chassi.use_gyro(use_gyro= True)
        self.kP = 1

    def getLeftReflection(self):
        return self.LEFT_COLOR_SENSOR.reflection()

    def getMiddleReflection(self):
        return self.MIDDLE_COLOR_SENSOR.reflection()

    def getRightReflection(self):
        return self.RIGHT_COLOR_SENSOR.reflection()
    
    def getColorLeft(self):
        return self.LEFT_COLOR_SENSOR.color(surface= True)
    
    def getColorMiddle(self):
        return self.Middle_COLOR_SENSOR.color(surface= True)

    def getColorRight(self):
        return self.RIGHT_COLOR_SENSOR.color(surface= True)

    def seguirReto(self, distancia): 
        self.chassi.use_gyro(use_gyro= True)
        self.chassi.straight(
            distance= distancia,
            then= Stop.BRAKE
        )

    def stop(self):
        self.chassi.stop()

    def drive(self, speed=200, rate):
        self.chassi.drive(speed=speed, turn_rate=rate)

    def extremeCurve(self):
        if self.getColorLeft() == Color.WHITE:
            while self.getColorMiddle() == Color.WHITE:
                self.drive(rate=200)
        else:
            while self.getColorMiddle() == Color.WHITE:
                self.drive(rate=-200)

    def pidControl(self):
        leftReflection = self.getLeftReflection() 
        rightReflection = self.getRightReflection()
        error = leftReflection - rightReflection
        output = error * self.kP
        self.drive(rate=output)

    def intersection(self):
        if self.getColorLeft() == Color.GREEN or self.getColorRight() == Color.GREEN: # Identifica qual foi o sensor que leu a cor
            whichSensor = ""
            if self.getColorLeft() == Color.GREEN and self.getColorRight() == Color.GREEN: # Dois sensores (left and right)
                whichSensor = "both"
            elif self.getColorLeft() == Color.GREEN:
                whichSensor = "left"
            else:
                whichSensor = "right"
            while (self.getColorLeft() != Color.BLACK or self.getColorRight() != Color.BLACK) or (self.getColorLeft() != Color.WHITE or self.getColorRight() != Color.WHITE):
                self.drive(rate=0)
            self.stop()
            if self.getColorLeft() == Color.BLACK or self.getColorRight() == Color.BLACK: # Realizar curva
                if whichSensor == "both":
                    pass # dar meia volta
                elif whichSensor == "left":
                    pass # virar à esquerda
                else:
                    pass # virar à direita
        else:
            self.pidControl()

    def FollowPath(self):
        if self.getColorMiddle() == Color.WHITE:
            self.extremeCurve()
        else:
            self.intersection()
