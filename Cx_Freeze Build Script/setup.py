from cx_Freeze import setup, Executable

setup(name='Tetromino',
	  version='0.1',
	  description='Matthew Zegar',
	  executables = [Executable("main.py", base = "Win32GUI", icon="tetracubeicon.ico")])