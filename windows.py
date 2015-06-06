
from os.path import join, expanduser, basename
import win32gui, pywintypes, win32con, win32file

from jca.files import my_paths
from jca.qter.qter_test import *
from jca.files.dir_db import DirDb

def all_windows():
  # Make a list of all the windows on the screen.
  windows = []
  def _MyCallback( hwnd, extra ):
    extra.append(hwnd)
  win32gui.EnumWindows(_MyCallback, windows)
  return windows

def bring_to_front(title):
  # Bring the window with the passed title to the foreground.
  for win in all_windows():
    if win32gui.GetWindowText(win) == title:
      try: win32gui.SetForegroundWindow(win)
      except pywintypes.error:  continue
      return True

def stack_widget(widget, tag):
  # Stack windows with the same title in the lower right corner of the screen.
  num_windows = 0
  for win_ in all_windows():
    if win32gui.GetWindowText(win_).startswith(tag):
      num_windows += 1
  screen_width, screen_height = screen_dims()
  widget.move(screen_width - widget.width(),
        screen_height - widget.height() - 60 - 10 * num_windows)

def foreground():
  return win32gui.GetWindowText(win32gui.GetForegroundWindow())

def current_file():
  # Pull current file from the text editor.
  for win in all_windows():
    if win32gui.IsWindowVisible(win):
      title = win32gui.GetWindowText(win)
      for title_str in [' - Notepad++', ' - Sublime Text']:
        if title_str in title:
          path = title.split(title_str)[0]
          if path.startswith(my_paths.goggles):
            db = DirDb(join(expanduser('~'), 'goggles'))
            return db.get(basename(path) + '_dir', 'full_path')
          return path

# Constants
buffer_size = 1024
watch_subtrees = True
to_check = 0
for attr in ["FILE_NAME", "DIR_NAME", "SIZE", "LAST_WRITE"]:
  flag = getattr(win32con, "FILE_NOTIFY_CHANGE_" + attr)
  to_check |= flag
"CREATION too (that flag isn't in win32con for some reason)"
to_check |= 64
action_strings = ["Created", "Deleted", "Updated", "Renamed from",
                  "Renamed to"]
                  
# Monitor a dir.  Fire whenever an action occurs.
def monitor(path_to_watch, on_change):
  hDir = win32file.CreateFile(path_to_watch, 0x0001,
              win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
              None, win32con.OPEN_EXISTING,
              win32con.FILE_FLAG_BACKUP_SEMANTICS, None)
  prev_time = 0  
  
  while 1:
    results = win32file.ReadDirectoryChangesW(
              hDir, buffer_size, watch_subtrees,
              to_check, None, None)
    for action_index, action_path in results:
      action = action_strings[action_index - 1]
      on_change(action, action_path)
          
if __name__ == '__main__':
  # Bring a window to front, stack widget, etc.  Test monitor root.
  start_if_havent()
  bring_to_front(foreground())
  widget = QWidget()
  stack_widget(widget, 'My Lint')
  print 'current_file: ', current_file()
  widget.show()
  launch_if_havent()
  
  def on_change(action, action_path):
    print 'on_change, action:', action, 'action_path:', action_path
  monitor('/', on_change)