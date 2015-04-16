import subprocess

def play_prometheus():
    try:
        subprocess.Popen(["ffplay", "-nodisp", "-autoexit", "-loglevel", "panic", "/home/jeandanielpearson/Downloads/sound/different_turret04.wav"])
    except Exception:
        pass