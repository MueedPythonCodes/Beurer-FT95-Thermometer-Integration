"""
Google Sheets Integration - Single Row Update
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from config import Config

class GoogleSheetsHandler:
    """Google Sheets handler with SINGLE ROW update"""
    
    def __init__(self):
        self.client = None
        self.sheet = None
        self.initialized = False
        self.current_row = 2  # Always update row 2
    
    def initialize(self):
        """Initialize Google Sheets connection"""
        try:
            print(f"   📊 Connecting to Google Sheets...")
            
            # Define scope
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]
            
            # Authenticate
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                Config.GOOGLE_CREDENTIALS_FILE, 
                scope
            )
            
            self.client = gspread.authorize(creds)
            
            # Open spreadsheet
            spreadsheet = self.client.open_by_key(Config.GOOGLE_SHEET_ID)
            
            # Get or create worksheet
            try:
                self.sheet = spreadsheet.worksheet(Config.WORKSHEET_NAME)
                print(f"   ✅ Using existing worksheet: {Config.WORKSHEET_NAME}")
            except:
                print(f"   📝 Creating new worksheet: {Config.WORKSHEET_NAME}")
                self.sheet = spreadsheet.add_worksheet(
                    title=Config.WORKSHEET_NAME,
                    rows=100,
                    cols=10
                )
                # Set up single row format
                self._setup_single_row()
            
            self.initialized = True
            print(f"   ✅ Google Sheets ready (Single Row Mode)")
            return True
            
        except Exception as e:
            print(f"   ❌ Google Sheets error: {e}")
            return False
    
    def _setup_single_row(self):
        """Setup single row format with headers"""
        try:
            # Clear everything
            self.sheet.clear()
            
            # Add headers
            headers = [
                '📅 DATE', '⏰ TIME', '🌡️ TEMP (°C)', '🌡️ TEMP (°F)', 
                '📱 DEVICE', '🔗 STATUS', '🕒 TIMESTAMP', '📊 SOURCE'
            ]
            self.sheet.update('A1:H1', [headers])
            
            # Format header row
            try:
                self.sheet.format('A1:H1', {
                    "backgroundColor": {"red": 0.2, "green": 0.6, "blue": 0.8},
                    "horizontalAlignment": "CENTER",
                    "textFormat": {"bold": True, "fontSize": 11}
                })
            except:
                pass
            
            # Add initial data row
            initial_data = [
                'Waiting...', '--:--:--', '--.--', '--.--',
                Config.DEVICE_NAME, 'Connecting...', datetime.now().isoformat(), 'REAL'
            ]
            self.sheet.update('A2:H2', [initial_data])
            
            print("   ✅ Single row setup complete")
            
        except Exception as e:
            print(f"   ⚠ Setup error: {e}")
    
    def save_reading(self, reading):
        """UPDATE SINGLE ROW (Row 2) with new reading"""
        if not self.initialized:
            print("   ⚠ Google Sheets not initialized")
            return False
        
        try:
            # Prepare single row data
            row_data = [
                reading.get('date_display', datetime.now().strftime("%Y-%m-%d")),  # A - Date
                reading.get('time_display', datetime.now().strftime("%H:%M:%S")),  # B - Time
                f"{reading.get('temperature_c', 0):.1f}",  # C - °C (formatted)
                f"{reading.get('temperature_f', 32):.1f}",  # D - °F (formatted)
                reading.get('device', Config.DEVICE_NAME),  # E - Device
                reading.get('status', 'Connected'),        # F - Status
                reading.get('timestamp', datetime.now().isoformat()),  # G - Timestamp
                reading.get('source', 'REAL')              # H - Source
            ]
            
            # UPDATE ONLY ROW 2 (overwrites previous)
            self.sheet.update(f'A{self.current_row}:H{self.current_row}', [row_data])
            
            # Format the temperature cells
            try:
                # Highlight temperature cells
                self.sheet.format(f'C{self.current_row}:D{self.current_row}', {
                    "backgroundColor": {"red": 1.0, "green": 0.9, "blue": 0.9},
                    "horizontalAlignment": "CENTER",
                    "textFormat": {"bold": True, "fontSize": 12}
                })
                
                # Format status based on connection
                if reading.get('status') == 'Connected':
                    status_color = {"red": 0.9, "green": 1.0, "blue": 0.9}  # Green
                else:
                    status_color = {"red": 1.0, "green": 0.9, "blue": 0.9}  # Light red
                
                self.sheet.format(f'F{self.current_row}', {
                    "backgroundColor": status_color,
                    "horizontalAlignment": "CENTER"
                })
            except:
                pass
            
            print(f"   ✅ Updated Google Sheets Row {self.current_row}")
            return True
            
        except Exception as e:
            print(f"   ❌ Google Sheets update error: {e}")
            return False
    
    def get_last_reading(self):
        """Get the last reading from row 2"""
        if not self.initialized:
            return None
        
        try:
            values = self.sheet.row_values(self.current_row)
            if len(values) >= 7:
                return {
                    'date': values[0],
                    'time': values[1],
                    'temp_c': values[2],
                    'temp_f': values[3],
                    'device': values[4],
                    'status': values[5],
                    'timestamp': values[6]
                }
        except Exception as e:
            print(f"   ⚠ Error reading from sheets: {e}")
        
        return None