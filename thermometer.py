import asyncio
from datetime import datetime
from bleak import BleakClient, BleakScanner

TEMP_CHAR_UUID = "00002a1c-0000-1000-8000-00805f9b34fb"

class FT95Thermometer:
    def __init__(self, mac_address, device_name, update_interval):
        self.mac_address = mac_address
        self.device_name = device_name
        self.update_interval = update_interval
        self.connected = False

    def notification_handler(self, characteristic, data):
        """Handle incoming temperature data"""
        try:
            # FT95 typical format (example: [0, 118, 1, 255, 254])
            temp_raw = int.from_bytes(data[1:3], byteorder='little') / 10.0
            reading = {
                'temperature_c': temp_raw,
                'temperature_f': (temp_raw * 9/5) + 32,
                'timestamp': datetime.now().isoformat(),
                'time_display': datetime.now().strftime("%H:%M:%S"),
                'date_display': datetime.now().strftime("%Y-%m-%d"),
                'status': 'Connected',
                'device': self.device_name
            }
            if self.callback:
                self.callback(reading)
        except Exception as e:
            print(f"   ❌ Data Parsing Error: {e}")

    async def continuous_real_read(self, callback, interval=2):
        self.callback = callback
        while True:
            try:
                # 1. Scanner: Har waqt check karega ke thermometer on hua ya nahi
                device = await BleakScanner.find_device_by_address(self.mac_address, timeout=5.0)
                
                if device:
                    print(f"   🔗 FT95 Found! Connecting...")
                    async with BleakClient(device) as client:
                        self.connected = True
                        print(f"   ✅ Connected! Waiting for button press...")
                        
                        # Notifications start karein
                        await client.start_notify(TEMP_CHAR_UUID, self.notification_handler)
                        
                        # Jab tak device signal de rahi hai, yahin rukay raho
                        while client.is_connected:
                            await asyncio.sleep(1)
                            
                else:
                    # Agar device nahi mili (off hai), to 2 sec wait karke dobara scan karein
                    self.connected = False
                    await asyncio.sleep(2)
                    
            except Exception as e:
                self.connected = False
                print(f"   🔍 Searching for FT95...")
                await asyncio.sleep(2)







































# import asyncio
# import time
# from datetime import datetime
# from bleak import BleakClient, BleakScanner

# # FT95 Health Thermometer UUIDs
# TEMP_CHAR_UUID = "00002a1c-0000-1000-8000-00805f9b34fb"
# FT95_TEMP_CHAR_UUID = "0000fff4-0000-1000-8000-00805f9b34fb"

# class FT95Thermometer:
#     def __init__(self, mac_address, device_name, update_interval):
#         self.mac_address = mac_address
#         self.device_name = device_name
#         self.update_interval = update_interval
#         self.client = None
#         self.connected = False
#         self.callback = None
#         self.recent_readings = []
#         self.max_readings = 50

#     def decode_temperature(self, data):
#         """Decode BLE temperature data packet"""
#         try:
#             # FT95 usually sends 5 bytes, temp is in bytes 1-3
#             if len(data) >= 4:
#                 raw_val = int.from_bytes(data[1:3], byteorder='little')
#                 return raw_val / 10.0
#             elif len(data) == 2:
#                 raw_val = int.from_bytes(data, byteorder='little')
#                 return raw_val / 10.0
#         except Exception as e:
#             print(f"   ⚠️ Decode error: {e}")
#         return None

#     def notification_handler(self, characteristic, data):
#         """Handle incoming data from thermometer button press"""
#         temp_c = self.decode_temperature(data)
#         if temp_c and 20 <= temp_c <= 50:
#             reading = self.create_reading_object(temp_c)
#             if self.callback:
#                 self.callback(reading)
#             print(f"   🌡️ NEW READING: {temp_c:.1f}°C")

#     async def connect_and_listen(self):
#         """Connect and setup notifications"""
#         try:
#             print(f"   🔍 Searching for {self.device_name}...")
#             device = await BleakScanner.find_device_by_address(self.mac_address, timeout=10.0)
            
#             if not device:
#                 return False

#             self.client = BleakClient(device)
#             await self.client.connect(timeout=15.0)
            
#             if self.client.is_connected:
#                 self.connected = True
#                 print(f"   🔗 Connected! Waiting for thermometer button press...")
                
#                 # Try to find which UUID works for notifications
#                 target_uuids = [TEMP_CHAR_UUID, FT95_TEMP_CHAR_UUID]
#                 found_char = False
                
#                 for uuid in target_uuids:
#                     try:
#                         await self.client.start_notify(uuid, self.notification_handler)
#                         print(f"   📡 Notifications active on: {uuid}")
#                         found_char = True
#                         break
#                     except:
#                         continue
                
#                 if not found_char:
#                     print("   ❌ Could not find a valid notification characteristic.")
#                     return False
                
#                 return True
#             return False
#         except Exception as e:
#             print(f"   ❌ Connection error: {e}")
#             self.connected = False
#             return False

#     def create_reading_object(self, temp_c):
#         temp_f = (temp_c * 9/5) + 32
#         now = datetime.now()
#         reading = {
#             'temperature_c': temp_c,
#             'temperature_f': temp_f,
#             'temperature_c_display': f"{temp_c:.1f}",
#             'temperature_f_display': f"{temp_f:.1f}",
#             'timestamp': now.isoformat(),
#             'date_display': now.strftime("%Y-%m-%d"),
#             'time_display': now.strftime("%H:%M:%S"),
#             'device': self.device_name,
#             'status': 'Connected',
#             'source': 'REAL'
#         }
#         self.recent_readings.insert(0, reading)
#         return reading

#     async def continuous_real_read(self, callback, interval=2):
#         self.callback = callback
#         while True:
#             try:
#                 if not self.client or not self.client.is_connected:
#                     self.connected = False
#                     success = await self.connect_and_listen()
#                     if not success:
#                         await asyncio.sleep(5)
#                         continue
                
#                 # Just keep the connection alive, notifications handle the rest
#                 await asyncio.sleep(interval)
#             except Exception as e:
#                 print(f"   ⚠️ Worker loop error: {e}")
#                 self.connected = False
#                 await asyncio.sleep(5)

#     def get_recent_readings(self, count=10):
#         return self.recent_readings[:count]







































