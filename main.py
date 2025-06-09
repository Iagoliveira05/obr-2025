from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, run_task

from Chassi import Chassi
from Anexo import Anexo

def main():
    chassi.seguirReto(20)


chassi = Chassi()

hub = PrimeHub()
run_task(main())