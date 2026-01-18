import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'ft95-secret-key-2024')
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', '0.0.0.0')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Bluetooth configuration
    THERMOMETER_MAC_ADDRESS = os.getenv('THERMOMETER_MAC_ADDRESS', 'FF:00:00:00:01:C8')
    DEVICE_NAME = os.getenv('DEVICE_NAME', 'FT95')
    SCAN_TIMEOUT = int(os.getenv('SCAN_TIMEOUT', 10))
    UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', 2))
    CONNECTION_TIMEOUT = int(os.getenv('CONNECTION_TIMEOUT', 30))
    
    # FT95 Specific UUIDs (Beurer FT95)
    FT95_SERVICE_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"
    FT95_TEMP_CHAR_UUID = "0000fff4-0000-1000-8000-00805f9b34fb"
    FT95_BATTERY_CHAR_UUID = "0000fff1-0000-1000-8000-00805f9b34fb"
    FT95_UNIT_CHAR_UUID = "0000fff2-0000-1000-8000-00805f9b34fb"
    
    # Google Sheets configuration
    GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID', '').strip()
    GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
    WORKSHEET_NAME = os.getenv('WORKSHEET_NAME', 'Temperature_Readings')
    
    # Data storage
    DATA_FILE = 'temperature_data.json'
    CSV_FILE = 'temperature_log.csv'
    
    # Web interface
    AUTO_REFRESH = int(os.getenv('AUTO_REFRESH', 2))
    MAX_READINGS_DISPLAY = int(os.getenv('MAX_READINGS_DISPLAY', 50))
    
    # Fast mode settings
    FAST_MODE = os.getenv('FAST_MODE', 'True').lower() == 'true'
    SINGLE_ROW_UPDATE = os.getenv('SINGLE_ROW_UPDATE', 'True').lower() == 'true'
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        errors = []
        
        if not cls.THERMOMETER_MAC_ADDRESS:
            errors.append("THERMOMETER_MAC_ADDRESS not configured")
        
        if not cls.GOOGLE_SHEET_ID:
            errors.append("GOOGLE_SHEET_ID not configured")
        
        if errors:
            print("\n⚠ Configuration errors:")
            for error in errors:
                print(f"   ❌ {error}")
            return False
        return True