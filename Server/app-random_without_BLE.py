#code without BLE connections just to test out the front-end
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
#we transfrom our FLask app into a SocketIO app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#our global variables for statistics
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
        leva=int(statistikaLeva*100/ravnotezen)
        desna=int(statistikaDesna*100/ravnotezen)
        number=[number1, number2, leva, desna, (100-leva-desna)] #we transmitt this array over SocketIO
        socketio.emit('newnumber', {'number': number}, namespace='/test')
        socketio.sleep(5) #we limit the reresh to 0.2Hz

@app.route("/") # base webpage route
def index():
    return render_template('findmyprofessor.html') #uses an external HTMl file

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread #we tell the app to use the global threaed
    global thread_stop_event
    print('Client connected')
    if not thread.isAlive():
        print("Starting Thread")
        thread_stop_event.clear()
        thread = socketio.start_background_task(randomNumberGenerator)
    #if the thread is not yet started, we basically create a new one to "multitask" number generator while still listening for requests in our main app

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    global thread_stop_event
    thread_stop_event.set()
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)
