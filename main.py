import sys
import signal
import asyncio
from threading import Thread, Lock
import time
from datetime import datetime
from config import Config
from thermometer import FT95Thermometer
from google_sheets import GoogleSheetsHandler
from webserver import create_app, socketio

class FT95System:
    def __init__(self):
        self.thermometer = None
        self.google_sheets = None
        self.app = None
        self.running = False
        self.current_reading = None 
        self.system_start_time = datetime.now()
        self.recent_readings = []
        self.max_readings = 50
        self.reading_lock = Lock()
        
    def initialize(self):
        print("=" * 60)
        print("FT95 AUTO-RECONNECT SYSTEM ACTIVE")
        print("=" * 60)
        self.thermometer = FT95Thermometer(
            mac_address=Config.THERMOMETER_MAC_ADDRESS,
            device_name=Config.DEVICE_NAME,
            update_interval=Config.UPDATE_INTERVAL
        )
        if Config.GOOGLE_SHEET_ID:
            self.google_sheets = GoogleSheetsHandler()
            self.google_sheets.initialize()
        
        # Web server initialization
        self.app = create_app(self)
        self.app.config['SYSTEM'] = self
        
    # --- YE FUNCTION MISSING THA JIS SE WEB CRASH HO RAHA THA ---
    def get_status(self):
        with self.reading_lock:
            connected = self.thermometer.connected if self.thermometer else False
            return {
                'connected': connected,
                'device': self.thermometer.device_name if self.thermometer else "Disconnected",
                'last_reading': self.current_reading,
                'uptime': str(datetime.now() - self.system_start_time).split('.')[0],
                'status': 'Online' if connected else 'Searching...'
            }

    def get_recent_readings(self, count=10):
        with self.reading_lock:
            return self.recent_readings[:count]

    def _google_sheets_sync_worker(self):
        """Force Overwrite Logic for Row 2 & Web Sync"""
        while self.running:
            try:
                time.sleep(5) 
                if self.google_sheets and self.current_reading:
                    with self.reading_lock:
                        reading = self.current_reading.copy()
                    
                    # Overwrite Row 2
                    self.google_sheets.save_reading(reading)
                    print(f"   📊 Sheet Row 2 Updated: {reading['temperature_c']}°C")
                    
                    # WEB KO BHI UPDATE BHEJOIN (Just in case)
                    socketio.emit('new_reading', reading)
                    socketio.emit('system_status', self.get_status())
            except Exception as e:
                print(f"   ⚠️ Sync Error: {e}")

    def _run_async_worker(self):
        """Aggressive Auto-Reconnect Loop"""
        while self.running:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                # Direct call to thermometer loop
                loop.run_until_complete(self.thermometer.continuous_real_read(self.handle_real_reading))
            except Exception as e:
                pass
            finally:
                loop.close()
            time.sleep(1)

    def handle_real_reading(self, reading):
        if not reading: return
        with self.reading_lock:
            self.current_reading = reading
            self.recent_readings.insert(0, reading)
            if len(self.recent_readings) > self.max_readings:
                self.recent_readings.pop()
        
        # Dashboard ko foran naya data bhejien
        socketio.emit('new_reading', reading)
        socketio.emit('system_status', self.get_status())

    def start(self):
        self.running = True
        # Bluetooth Thread
        Thread(target=self._run_async_worker, daemon=True).start()
        # Sheets Sync Thread
        Thread(target=self._google_sheets_sync_worker, daemon=True).start()
        
        print(f"🚀 Dashboard: http://localhost:{Config.PORT}")
        socketio.run(self.app, host=Config.HOST, port=Config.PORT, debug=False, use_reloader=False, allow_unsafe_werkzeug=True)

    def stop(self):
        self.running = False
        sys.exit(0)

if __name__ == "__main__":
    system = FT95System()
    system.initialize()
    system.start()





































# #!/usr/bin/env python3
# """
# FT95 Thermometer System - FINAL STABLE FIX
# """

# import sys
# import signal
# import asyncio
# from threading import Thread, Lock
# import time
# from datetime import datetime
# from config import Config

# # Import modules
# from thermometer import FT95Thermometer
# from google_sheets import GoogleSheetsHandler
# from webserver import create_app, socketio

# class FT95System:
#     def __init__(self):
#         self.thermometer = None
#         self.google_sheets = None
#         self.app = None
#         self.running = False
#         self.current_reading = None 
#         self.system_start_time = datetime.now()
#         self.recent_readings = []
#         self.max_readings = 50
#         self.reading_lock = Lock()
        
#     def initialize(self):
#         print("=" * 60)
#         print("FT95 REAL-TIME THERMOMETER SYSTEM")
#         print("=" * 60)
        
#         self.thermometer = FT95Thermometer(
#             mac_address=Config.THERMOMETER_MAC_ADDRESS,
#             device_name=Config.DEVICE_NAME,
#             update_interval=Config.UPDATE_INTERVAL
#         )
        
#         print(f"\n📊 Initializing Google Sheets...")
#         if Config.GOOGLE_SHEET_ID:
#             self.google_sheets = GoogleSheetsHandler()
#             if self.google_sheets.initialize():
#                 print(f"   ✅ Connected to Google Sheets (Row 2 Mode)")
#             else:
#                 self.google_sheets = None

#         print(f"\n🌐 Initializing Web Dashboard...")
#         self.app = create_app(self)
#         self.app.config['SYSTEM'] = self
        
#     def get_status(self):
#         return {
#             'connected': self.thermometer.connected if self.thermometer else False,
#             'device': self.thermometer.device_name if self.thermometer else "Disconnected",
#             'last_reading': self.current_reading,
#             'uptime': str(datetime.now() - self.system_start_time).split('.')[0],
#             'status': 'Running' if self.running else 'Stopped'
#         }

#     def get_recent_readings(self, count=10):
#         with self.reading_lock:
#             return self.recent_readings[:count]

#     def start(self):
#         if self.running: return
#         self.running = True
        
#         self.thermometer_thread = Thread(target=self._run_async_worker, daemon=True)
#         self.thermometer_thread.start()
        
#         # Google Sheets Sync Thread
#         self.sync_thread = Thread(target=self._google_sheets_sync_worker, daemon=True)
#         self.sync_thread.start()
        
#         print(f"\n🚀 SYSTEM LIVE: http://localhost:{Config.PORT}")
        
#         try:
#             socketio.run(self.app, host=Config.HOST, port=Config.PORT, 
#                          debug=False, use_reloader=False, allow_unsafe_werkzeug=True)
#         except Exception as e:
#             print(f"❌ Server error: {e}")
#             self.stop()

#     def _google_sheets_sync_worker(self):
#         """FORCE SYNC: Ensures Google Sheets stays updated with Web Data"""
#         last_synced_temp = None
#         last_sync_time = 0
        
#         while self.running:
#             try:
#                 time.sleep(3) # Google Sheets quota limit ka khayal rakhte hue
                
#                 if self.google_sheets and self.current_reading:
#                     with self.reading_lock:
#                         reading = self.current_reading.copy()
                    
#                     current_temp = reading.get('temperature_c')
                    
#                     # Fix Logic: Agar temp badal jaye YA 10 seconds guzar jayein (force update)
#                     if current_temp != last_synced_temp or (time.time() - last_sync_time > 10):
#                         success = self.google_sheets.save_reading(reading)
#                         if success:
#                             last_synced_temp = current_temp
#                             last_sync_time = time.time()
#                             print(f"   ✅ Sheets Synced: {current_temp}°C")
#             except Exception as e:
#                 print(f"   ⚠️ Sync Error: {e}")

#     def _run_async_worker(self):
#         """Stable Reconnection Worker"""
#         while self.running:
#             loop = asyncio.new_event_loop()
#             asyncio.set_event_loop(loop)
            
#             async def run_session():
#                 print(f"\n🔍 Searching for FT95... (Waiting for button press)")
#                 try:
#                     self.thermometer.connected = False
#                     await self.thermometer.continuous_real_read(
#                         callback=self.handle_real_reading,
#                         interval=Config.UPDATE_INTERVAL
#                     )
#                 except Exception:
#                     pass
#                 finally:
#                     self.thermometer.connected = False

#             try:
#                 loop.run_until_complete(run_session())
#             except Exception:
#                 pass
#             finally:
#                 loop.close()
            
#             if self.running:
#                 time.sleep(3)

#     def handle_real_reading(self, reading):
#         if not reading: return
#         with self.reading_lock:
#             # Force update timestamp if missing to ensure sync works
#             if 'timestamp' not in reading:
#                 reading['timestamp'] = datetime.now().isoformat()
            
#             self.current_reading = reading
#             self.recent_readings.insert(0, reading)
#             if len(self.recent_readings) > self.max_readings:
#                 self.recent_readings.pop()
        
#         # Dashboard update (This works instantly)
#         socketio.emit('new_reading', reading)

#     def stop(self):
#         print("\n🛑 STOPPING SYSTEM...")
#         self.running = False
#         sys.exit(0)

# def signal_handler(sig, frame):
#     system.stop()

# if __name__ == "__main__":
#     signal.signal(signal.SIGINT, signal_handler)
#     system = FT95System()
#     system.initialize()
#     system.start()























