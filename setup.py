import cx_Freeze

executables = [cx_Freeze.Executable("platform_sol.py")]

cx_Freeze.setup(
    name = "My First Game!",
    options = {"build_exe": {"packages": ["pygame"], "include_files": [("./assets/background.png", "./assets/background.png"), ("./assets/dirt_32x32.png", "./assets/dirt_32x32.png"), ("./assets/grass_32x32.png", "./assets/grass_32x32.png"), ("./assets/jump.wav", "./assets/jump.wav"), ("./assets/player.png", "./assets/player.png")]}},
    executables = executables
    )
