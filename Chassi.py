from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch


# Preto -> Color(h=180, s=15, v=17)
# Branco -> Color(h=180, s=5, v=89)


class Chassi:
    def __init__(self):
        self.hub = PrimeHub()
        self.LEFT_MOTOR = Motor(port=Port.C)
        self.RIGHT_MOTOR = Motor(port=Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
        self.LEFT_COLOR_SENSOR = ColorSensor(port= Port.B)
        self.MIDDLE_COLOR_SENSOR = ColorSensor(port= Port.F)
        self.RIGHT_COLOR_SENSOR = ColorSensor(port= Port.D)
        # self.ULTRASSONIC_SENSOR = UltrasonicSensor(port= Port.F)

        self.chassi = DriveBase(
            left_motor= self.LEFT_MOTOR,
            right_motor= self.RIGHT_MOTOR,
            wheel_diameter= 3.6, # Centimetros
            axle_track= 14.0 # Centimetros
        )
        self.kP = 1

        self.chassi.settings(straight_acceleration=500, turn_acceleration=500)

        Color.WHITE = Color(h=180, s=5, v=89)
        Color.BLACK = Color(h=180, s=15, v=17)
        my_colors = [Color.WHITE, Color.BLACK, Color.NONE]

        self.LEFT_COLOR_SENSOR.detectable_colors(my_colors)
        self.MIDDLE_COLOR_SENSOR.detectable_colors(my_colors)
        self.RIGHT_COLOR_SENSOR.detectable_colors(my_colors)



    def getMiddleHSV(self):
        return self.MIDDLE_COLOR_SENSOR.hsv()

    def getLeftReflection(self):
        return self.LEFT_COLOR_SENSOR.reflection()

    def getMiddleReflection(self):
        return self.MIDDLE_COLOR_SENSOR.reflection()

    def getRightReflection(self):
        return self.RIGHT_COLOR_SENSOR.reflection()
    
    def getColorLeft(self):
        return self.LEFT_COLOR_SENSOR.color(surface= True)
    
    def getColorMiddle(self):
        return self.MIDDLE_COLOR_SENSOR.color(surface= True)

    def getColorRight(self):
        return self.RIGHT_COLOR_SENSOR.color(surface= True)

    def seguirReto(self, distancia):
        self.chassi.straight(
            distance= distancia,
            then= Stop.BRAKE
        )

    def stop(self):
        self.chassi.stop()

    def drive(self, rate, speed=10):
        self.chassi.drive(speed=speed, turn_rate=rate)

    def extremeCurve(self):
        if self.getColorLeft() == Color.WHITE:
            while self.getColorMiddle() == Color.WHITE:
                self.LEFT_MOTOR.run(200)
                self.RIGHT_MOTOR.run(-600)
            
        else:
            while self.getColorMiddle() == Color.WHITE:
                self.LEFT_MOTOR.run(-600)
                self.RIGHT_MOTOR.run(200)
                # self.drive(rate=-40, speed=-10)
                # wait(100)

        self.stop()

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
        if (self.getColorMiddle() == Color.WHITE and self.getColorLeft() == Color.BLACK) or (self.getColorMiddle() == Color.WHITE and self.getColorRight() == Color.BLACK):
            self.extremeCurve()
        else:
            self.intersection()
