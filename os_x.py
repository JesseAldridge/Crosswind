
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