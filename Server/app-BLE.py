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
import platform

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#MAC or UUID (based on whether you use Mac or Windows) for our Bleak connection over BLE to Arduinos
notify_uuid = "00002a19-0000-1000-8000-00805f9b34fb".format(0x2A19)

naprava1 = ( #device1
    "C2:97:1D:BD:47:1B"
    if platform.system() != "Darwin"
    else "96E8409A-F2EB-4029-B3DC-615FADE0C838"
)

naprava2 = ( #device2
    "F4:FB:70:D5:CF:55"
    if platform.system() != "Darwin"
    else "D31CB0CA-890E-476B-80D9-80ED8A3AA69A"
)

#our global data variables for statistics
number1 = 0
number2 = 0
statistikaLeva = 0
statistikaDesna = 0
statistikaNobena = 0

connectedEvent = asyncio.Event()

#we transfrom our FLask app into a SocketIO app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#we enable the use of threads using the thread library
thread = None
thread_stop_event = Event()

def callback(sender, data, mac_address):
    global number1
    global number2
    global statistikaLeva
    global statistikaDesna
    global statistikaNobena
    dataint = int.from_bytes(data, byteorder='little', signed=True)
    if(mac_address == naprava1):
        number1 = dataint
    else:
        number2 = dataint
    #our logical to decide which blackboard is being written on
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
    number=[number1, number2, leva, desna, (100-leva-desna)] #we transmit this array over SocketIO
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
            while connectedEvent.is_set():
                await asyncio.sleep(0.1)
            await client.stop_notify(notify_uuid)
        except Exception as e:
            print(e)
    print("disconnect from", address)


@app.route("/") # homepage route
def index():
    connectedEvent.set()
    print("Web client connected")
    return render_template('findmyprofessor.html') #external HTML use

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    global naprava1
    global naprava2
    global thread_stop_event
    print('Client connected')
    connectedEvent.set()


    #if the thread is not yet started, we basically create a new one to "multitask" BLE connections while still listening for requests in our main app
    if not thread or not thread.is_alive():
        print("Starting Thread from ",threading.current_thread().ident,threading.current_thread().name)
        thread_stop_event.clear()
        thread = Thread(target=functools.partial(run,[naprava1,naprava2]),name="BLEthread")
        thread.start()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    global thread_stop_event
    thread_stop_event.set()
    connectedEvent.clear()
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)
