import cv2
import tensorflow as tf
import platform
import subprocess
import sys
import getpass
from pathlib import Path
import matplotlib.pyplot as plt
import math
import time

sys.path.append("./Rcb4Lib")
sys.path.append("./ledCamera")

from Rcb4BaseLib import Rcb4BaseLib
from led_camera import ledCamera

print(platform.machine())
print(platform.platform())
print(platform.system())

class KXRA5:
    
    am1 = 120
    am2 = 120
    am3 = 200
    am4 = 160
    
    sv_pos = [0,0,0,0,0,0,0,0]
    
    rcb4 = Rcb4BaseLib()
    ledCam = ledCamera()
    crnt_path = Path.cwd()
    model_path = crnt_path / "ledCamera" / "phots-model-light.hdf5"
    
    def __init__(self):
        
        self.ledCam.model_set(str(self.model_path))
        #ledCam.camera_view()
        ret, frame = self.ledCam.cap.read()
        self.rcb4.open('/dev/ttyUSB0',115200,1.3)
        for i in range(1,8):
            print(i,self.get_degree(i))
            
    def __del__(self):
        self.rcb4.close()
        self.ledCam.release()
            
    def get_theta(self,sv_no):
        _,sv = self.rcb4.getSinglePos(sv_no,1)
        self.sv_pos[sv_no] = sv
        rad = (7500 - sv) / 5000 * math.pi
        return rad

    def get_degree(self,sv_no):
        rad = self.get_theta(sv_no)
        degree = 180 * rad / math.pi
        return degree

    def set_theta(self,sv_no,rad,late=200):
        sv = int(7500 - 5000 * rad / math.pi)
        print(sv)
        if(sv < 5000 or 10000< sv):
            return False
        self.rcb4.setSingleServo(sv_no,1,sv,late)
        return sv

    def theta2degree(self,theta):
        return round((180 * theta / math.pi),1)

    def set_lh2theta(self,l,h,late=200):
        op2 = l**2 + h**2
        print(op2)
        op = math.sqrt(op2)
        print(op)
        alpha = math.acos((am2**2 + am3**2 - op2) / (2 * am2 * am3))
        beta = math.acos((op2 + am2**2 - am3**2) / (2 * am2 * am3))
        gamma = math.acos( h / op )
        sv2 = gamma - beta
        sv3 = math.pi - alpha
        sv5 = math.pi - sv2 - sv3

        print(self.theta2degree(sv2),self.theta2degree(sv3),self.theta2degree(sv5))
        print(self.set_theta(2,sv2,late))
        print(self.set_theta(3,sv3,late))
        print(self.set_theta(5,sv5,late))

        return True

    # 3次元で指定
    def set_xyz2theta(self,x,y,z,late=200):
        z0 = z + am4
        sv1 = math.atan(y/x)
        xy = math.sqrt(x**2 + y**2)
        print(self.set_theta(1,sv1))
        self,self.set_lh2theta(xy,z0,late)
        
        return True
