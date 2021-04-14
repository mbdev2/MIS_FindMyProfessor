from flask import Flask, render_template, redirect, request
import asyncio
from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError

app = Flask(__name__)

@app.route("/") # route za osnovno stran
def home():
    return render_template('findmyprofessor.html') #vzame HTML template iz zunanje datoteke

@app.route("/preset", methods=["POST"]) #route klici za presete PTZ 1=tabla1, 2=tabla2, 3=kateder
def nastaviPresetPTZ():
    avtonomijaONOFF = False #ustavi avtonomno upravljanje kamere
    global izbranPreset
    izbranPreset = int(request.form["preset"]) #shranimo vrednost preseta (1-3)
    print("Izbrani preset za PTZ: ", izbranPreset) #izpisemo v terminal ker preset je
    return render_template('findmyprofessor.html', status=izbranPreset)

@app.route("/auto", methods=["POST"]) #route za zagon avtonomnega sistema sledenja
def zagonAvtonomnegaSistema():
    global avtonomijaONOFF
    avtonomijaONOFF = True #globalna spremenljivka, ki bo opravljala naš thread loop
    print("Zagon avtonomnega sistema MLX90640")
    return render_template('findmyprofessor.html', status=4)

app.run(debug = True)
