from flask import Flask, render_template, redirect, request
import asyncio
from flask_socketio import SocketIO, emit
from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError
from random import random
from time import sleep
from threading import Thread, Event

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

thread = Thread()
thread_stop_event = Event()
#spremenimo flask app v socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#omogocimo uporabo threada z knjizico
statistikaLeva = 0
statistikaDesna = 0
statistikaNobena = 0

def randomNumberGenerator():
    #infinite loop of magical random numbers
    while not thread_stop_event.isSet():
        global statistikaLeva
        global statistikaDesna
        global statistikaNobena
        number1 = round(random()*100)
        number2 = round(random()*100)
        if (number1 >60 or number2 >60):
            if number1 > number2:
                statistikaLeva+=1
            else:
                statistikaDesna+=1
        else:
            statistikaNobena+=1
        ravnotezen=statistikaLeva+statistikaDesna+statistikaNobena
        leva=statistikaLeva*100/ravnotezen
        desna=statistikaDesna*100/ravnotezen
        number=[number1, number2, leva, desna, (100-leva-desna)] #tale array posljemo preko sock emit na spletno stran
        socketio.emit('newnumber', {'number': number}, namespace='/test')
        socketio.sleep(5) #osvezimo na vsake 5 sec

@app.route("/") # route za osnovno stran
def index():
    return render_template('findmyprofessor.html') #vzame HTML template iz zunanje datoteke

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread #zelimo uporabljati globalni thread
    global thread_stop_event
    print('Client connected')
    if not thread.isAlive():
        print("Starting Thread")
        thread_stop_event.clear()
        thread = socketio.start_background_task(randomNumberGenerator)
    #ce ni ze zagnan, zazenemo thread z imenom randomNumberGenerator (torej basiclly klicemo funkcijo k se bo izvajala v niti)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    global thread_stop_event
    thread_stop_event.set()
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)
