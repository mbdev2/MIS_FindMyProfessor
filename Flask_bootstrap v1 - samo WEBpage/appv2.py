from flask import Flask, render_template, redirect, request
import asyncio
from flask_socketio import SocketIO, emit
from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError
from random import random
from time import sleep
from threading import Thread, Event
import functools

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#spremenimo flask app v socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#omogocimo uporabo threada z knjizico
thread = Thread()
thread_stop_event = Event()
notify_uuid = "00002a19-0000-1000-8000-00805f9b34fb".format(0x2A19)
vrednost1=0
vrednost2=0

def callback(sender, data, mac_address):
    dataint = int.from_bytes(data, byteorder='big', signed=False)
    global vrednost1
    global vrednost2
    vrednost1=4
    vrednost2=5
    #dodaj kodo

def run(addresses):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = asyncio.gather(*(connect_to_device(address) for address in addresses))
    loop.run_until_complete(tasks)


async def connect_to_device(address):
    print("starting", address, "loop")
    async with BleakClient(address, timeout=5.0) as client:

        print("connect to", address)
        try:

            #model_number = await client.read_gatt_char(address)
            await client.start_notify(notify_uuid, functools.partial(callback, mac_address=address))
            await asyncio.sleep(1000.0)
            await client.stop_notify(notify_uuid)
        except Exception as e:
            print(e)

    print("disconnect from", address)

def randomNumberGenerator():
    #infinite loop of magical random numbers
    while not thread_stop_event.isSet():
        global vrednost1
        global vrednost2
        number=[vrednost1, vrednost2] #tale array posljemo preko sock emit na spletno stran
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
    run(["96E8409A-F2EB-4029-B3DC-615FADE0C838","D31CB0CA-890E-476B-80D9-80ED8A3AA69A"])
    #ce ni ze zagnan, zazenemo thread z imenom randomNumberGenerator (torej basiclly klicemo funkcijo k se bo izvajala v niti)
    if not thread.isAlive():
        print("Starting Thread")
        thread_stop_event.clear()
        thread = socketio.start_background_task(randomNumberGenerator)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    global thread_stop_event
    thread_stop_event.set()
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)