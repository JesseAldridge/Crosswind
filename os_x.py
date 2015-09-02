import subprocess, os

import AppKit
from PIL import Image

def get_screen_size():
  return max([(screen.frame().size.width, screen.frame().size.height) 
    for screen in AppKit.NSScreen.screens()])

def take_screenshot():
  ' Return an Image of the screen. '

  cmd_line = 'screencapture -t png -x temp_img.png'
  subprocess.Popen(cmd_line.split()).communicate()
  img = Image.open('temp_img.png')
  os.remove('temp_img.png')
  return img

if __name__ == '__main__':
  print get_screen_size()
  print take_screenshot()