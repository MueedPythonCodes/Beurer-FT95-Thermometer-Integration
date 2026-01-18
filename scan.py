import asyncio
from bleak import BleakScanner

async def run():
    print("Scanning for Bluetooth devices... (10 seconds)")
    devices = await BleakScanner.discover()
    for d in devices:
        print(f"Name: {d.name}, Address: {d.address}")

asyncio.run(run())