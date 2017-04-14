import cx_Freeze

executables = [cx_Freeze.Executable("your-script-name.py")]

cx_Freeze.setup(
    name = "My First Game!",

    options = {"build_exe": {"packages": ["pygame"], "include_files": []}},
    
    executables = executables
    )
