import asyncio
from bleak import BleakClient, BleakScanner

async def auto_pair_forever(address):
    print(f"🚀 Initializing Auto-Pairer for FT95 ({address})...")
    
    while True:
        try:
            print("\r📡 Scanning for device signal...", end="", flush=True)
            # 1. Device ko dhoondna
            device = await BleakScanner.find_device_by_address(address, timeout=5.0)
            
            if device:
                print(f"\n✅ FT95 Found! Attempting Permanent Pairing...")
                async with BleakClient(device) as client:
                    # 2. Hardware Pairing Request
                    # Ye line Windows ko force karti hai ke wo "Pairing Popup" dikhaye ya auto-bond kare
                    paired = await client.pair()
                    
                    if paired:
                        print("🔐 [SUCCESS] Device is now Bonded/Paired with this System.")
                        print("✨ Ab aapka system isay 'Life-Time' yaad rakhega.")
                        break # Pairing ho gayi, ab loop se bahar
                    else:
                        print("⚠️ Pairing failed. Make sure 'blu' is flashing on Thermometer.")
            
            await asyncio.sleep(1)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            await asyncio.sleep(2)

if __name__ == "__main__":
    # Aapki device ki ID jo scan mein aayi thi
    TARGET_MAC = "FF:00:00:00:01:C8"
    asyncio.run(auto_pair_forever(TARGET_MAC))