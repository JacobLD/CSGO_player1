# direct inputs
# source to this solution and code:
# http://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
# http://www.gamespp.com/directx/directInputKeyboardScanCodes.html

import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

# http://terpconnect.umd.edu/~nsw/enpm808c/scancode.htm
# Scan codes at url
W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
L_SHIFT = 0x2A
ONE = 0x02
TWO = 0x03
THREE = 0x04
FOUR = 0x05
FIVE = 0x06
ALT = 0x38
CTRL = 0x1D
B = 0x30
F1 = 0x3B
E = 0x12
Q = 0x10
R = 0x13

# needs to be implemented
# SPACE = 0x39

# Is in proper order
KEYS = [W, A, S, D, L_SHIFT, ONE, TWO, THREE, FOUR, FIVE, ALT, CTRL, B, F1, E, Q, R]


NP_2 = 0x50
NP_4 = 0x4B
NP_6 = 0x4D
NP_8 = 0x48

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actual Functions

#does not release
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

if __name__ == '__main__':
    PressKey(0x11)
    time.sleep(1)
    ReleaseKey(0x11)
    time.sleep(1)