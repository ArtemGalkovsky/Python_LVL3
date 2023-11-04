# Add your Python code here. E.g.
from microbit import *
import audio
import neopixel
Red=(255,0,0)
Orange=(255,165,0)
Yellow=(255,255,0)
Green=(0,255,0)
Blue=(0,0,255)
Dark_Violet=(148,0,211)
White=(255,255,255)
color=(Red,Orange,Yellow,Green,Blue,Dark_Violet,White)
np=neopixel.NeoPixel(pin12, 1)
i=0
while True:
np.clear()
np[0]=color[i]
np.show()
sleep(1000)
i=i+1
if i>6:
    i=0
timer=0
display.show(Image('00000:'
                   '09090:'
                   '00000:'
                   '09990:'
                   '00000'))
audio.play(Sound.HELLO)
while True:
    if pin_logo.is_touched():
        timer=0
        display.show(Image.HAPPY)
        audio.play(Sound.HAPPY)
    elif accelerometer.was_gesture('shake'):
        timer=0
        display.show(Image.SURPRISED)
        audio.play(Sound.GIGGLE)
    else:
        sleep(500)
        timer+=0.5
    if timer==20:
        display.show(Image.SAD)
        audio.play(Sound.SAD)
    elif timer==30:
        display.show(Image.ASLEEP)
        audio.play(Sound.YAWN)
    elif timer==40:
        display.show(Image.SKULL)
        audio.play(Sound.MYSTERIOUS)
        break
    