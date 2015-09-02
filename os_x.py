import subprocess, os, time, re

from PIL import Image

class g:
  cached_size = None

def get_screen_size():
  if not g.cached_size:
    proc = subprocess.Popen(['system_profiler', 'SPDisplaysDataType'], stdout=subprocess.PIPE)
    result = proc.communicate()[0]
    dims = re.search('Resolution.*', result).group().split(':')[-1].split('x')
    g.cached_size = [int(x) for x in dims]
  return g.cached_size

def take_screenshot():
  ' Return an Image of the screen. '

  cmd_line = 'screencapture -t png -x temp_img.png'
  subprocess.Popen(cmd_line.split()).communicate()
  img = Image.open('temp_img.png')
  os.remove('temp_img.png')
  return img

if __name__ == '__main__':
  for i in range(10):
    print get_screen_size()
  for i in range(2):
    print take_screenshot()
    time.sleep(1)
