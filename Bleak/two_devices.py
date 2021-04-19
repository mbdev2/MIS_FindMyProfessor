from bleak import BleakClient
import asyncio
import functools

notify_uuid = "00002a19-0000-1000-8000-00805f9b34fb".format(0x2A19)


def callback(sender, data, mac_address):
    print(mac_address, data)

def run(addresses):
    loop = asyncio.get_event_loop()

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


if __name__ == "__main__":
    run(
        ["96E8409A-F2EB-4029-B3DC-615FADE0C838","D31CB0CA-890E-476B-80D9-80ED8A3AA69A"]
    )
