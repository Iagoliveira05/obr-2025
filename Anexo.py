from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

class MotorEsquerda:
    def __init__(self):
        self.motorEsquerda = Motor(port= Port.D)
        self.motorEsquerda.control.pid()
        self.motorEsquerda.reset_angle()

    def girarPorGrau(self, velocidade, angulo):
        self.motorEsquerda.run_angle(
            speed= velocidade,
            rotation_angle= angulo,
            then= Stop.BRAKE
        )

class MotorDireita:
    def __init__(self):
        self.motorDireita = Motor(port= Port.E)

    def girarPorGrau(self, velocidade, angulo):
        self.motorDireita.run_angle(
            speed= velocidade,
            rotation_angle= angulo,
            then= Stop.BRAKE
        )


class Anexo:
    def __init__(self):
        self.motorEsquerda = MotorEsquerda()
        self.motorDireita = MotorDireita()

