import threading

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

#podatki za Bleak
notify_uuid = "00002a19-0000-1000-8000-00805f9b34fb".format(0x2A19)

naprava1 = "96E8409A-F2EB-4029-B3DC-615FADE0C838"
naprava2 = "D31CB0CA-890E-476B-80D9-80ED8A3AA69A"

number1 = 0
number2 = 0

disconnectEvent = asyncio.Event()

#spremenimo flask app v socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#omogocimo uporabo threada z knjizico
thread = None
#thread2 = Thread()
thread_stop_event = Event()

def callback(sender, data, mac_address):
    global number1
    global number2
    dataint = int.from_bytes(data, byteorder='little', signed=True)
    if(mac_address == naprava1):
        number1 = dataint
    else: number2 = dataint
    number=[number1, number2] #tale array posljemo preko sock emit na spletno stran
    socketio.emit('newnumber', {'number': number}, namespace='/test')


def run(addresses):
    print("Starting Thread in run from ",threading.current_thread().ident,threading.current_thread().name)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    tasks = asyncio.gather(*(connect_to_device(address) for address in addresses))
    loop.run_until_complete(tasks)


async def connect_to_device(address):
    global notify_uuid
    print("starting", address, "loop")
    async with BleakClient(address, timeout=10.0) as client:

        print("connect to", address)
        try:
            #model_number = await client.read_gatt_char(address)
            await client.start_notify(notify_uuid, functools.partial(callback, mac_address=address))
            while not disconnectEvent.is_set():
                await asyncio.sleep(0.1)
            await client.stop_notify(notify_uuid)
        except Exception as e:
            print(e)
    print("disconnect from", address)


@app.route("/") # route za osnovno stran
def index():
    return render_template('findmyprofessor.html') #vzame HTML template iz zunanje datoteke

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    global naprava1
    global naprava2 #zelimo uporabljati globalni thread
    global thread_stop_event
    print('Client connected')


    #ce ni ze zagnan, zazenemo thread z imenom randomNumberGenerator (torej basiclly klicemo funkcijo k se bo izvajala v niti)
    if not thread or not thread.is_alive():
        print("Starting Thread from ",threading.current_thread().ident,threading.current_thread().name)
        thread_stop_event.clear()
        #thread = socketio.start_background_task(run([naprava1,naprava2]))
        thread = Thread(target=functools.partial(run,[naprava1,naprava2]),name="BLEthread")
        thread.start()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    global thread_stop_event
    thread_stop_event.set()
    #disconnectEvent.set()
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)
