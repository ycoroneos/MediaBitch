from subprocess import call

def setVolume(vol):
    call(["amixer", "set", "Master", str(vol)+"%"])
