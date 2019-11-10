#!/usr/bin/python
import sys
import time
import yaml
from pynput import mouse, keyboard
from pynput.keyboard import Key
from pynput.mouse import Button
import struct

kb_controller = keyboard.Controller()
m_controller = mouse.Controller()

exit = False
paused = False

delay_between_press_release = 0.025
delay_between_keys = 0.01

def on_release(key):
    global exit
    global paused
    global delay_between_press_release
    global delay_between_keys

    try:
        KEY = key.char
    except:
        KEY = key

    if paused and KEY not in [Key.f1,Key.f4]:
        return
    elif KEY == Key.f4:
        print 'EXIT'
        exit = True
    elif KEY == Key.f1:
        if paused:
            print 'UNPAUSED'
            paused = False
        else:
            paused = True
            print 'PAUSED'
    elif KEY == 'e':
        print 'E'
        kb_controller.press('o')
        kb_controller.press('p')
        time.sleep(delay_between_press_release)
        kb_controller.release('o')
        kb_controller.release('p')
    elif KEY == 'q':
        print 'Q'
        kb_controller.press('9')
        kb_controller.press('0')
        time.sleep(delay_between_press_release)
        kb_controller.release('9')
        kb_controller.release('0')


kb_listener = keyboard.Listener(on_release=on_release)
kb_listener.start()


mb_left = 0
mb_right = 0

file = open( "/dev/input/mice", "rb" )
while not exit:
    p_mb_left = mb_left
    p_mb_right = mb_right

    buf = file.read(3)
    button = ord( buf[0] )
    mb_left = button & 0x1
    mb_right = ( button & 0x2 ) > 0

    if paused:
        continue

    if mb_left != p_mb_left:
        if mb_left == 1:
            print '1 PRESSED'
            kb_controller.press('1');
        else:
            print '1 RELEASED'
            kb_controller.release('1');

    if mb_right != p_mb_right:
        if mb_right == 1:
            print '2 PRESSED'
            kb_controller.press('2');
        else:
            print '2 RELEASED'
            kb_controller.release('2');

    time.sleep(0.01)

kb_listener.stop()
file.close()

