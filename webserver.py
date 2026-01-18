"""
Flask Web Server - Fixed for Socket.IO connection
"""

from flask import Flask, render_template, jsonify, request, current_app
from flask_socketio import SocketIO, emit
from config import Config
from datetime import datetime

socketio = SocketIO(cors_allowed_origins="*", async_mode='threading')

def create_app(system_instance):
    """Create Flask application"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    socketio.init_app(app)
    
    @app.route('/')
    def index():
        """Main dashboard page"""
        return render_template(
            'index.html',
            config={
                'device_name': Config.DEVICE_NAME,
                'update_interval': Config.UPDATE_INTERVAL,
                'port': Config.PORT,
                'mac_address': Config.THERMOMETER_MAC_ADDRESS
            }
        )
    
    @app.route('/api/status')
    def get_status_api():
        """API endpoint for system status"""
        return jsonify(system_instance.get_status())
    
    @app.route('/api/readings')
    def get_readings():
        """API endpoint for recent readings"""
        count = request.args.get('count', default=10, type=int)
        return jsonify(system_instance.get_recent_readings(count))

    @socketio.on('connect')
    def handle_connect(auth=None):
        """FIXED: Handles connection and sends initial status"""
        print(f"🌐 New client connected")
        
        # Send current status using the fixed get_status method
        emit('system_status', system_instance.get_status())
        
        # Send current reading if available
        if system_instance.current_reading:
            emit('new_reading', system_instance.current_reading)
        
        # Send recent readings
        recent = system_instance.get_recent_readings(10)
        if recent:
            emit('recent_readings', recent)
    
    @socketio.on('disconnect')
    def handle_disconnect():
        print(f"🌐 Client disconnected")
    
    @socketio.on('request_status')
    def handle_status_request():
        emit('status_update', system_instance.get_status())
    
    @socketio.on('request_readings')
    def handle_readings_request(data):
        count = data.get('count', 10)
        emit('readings_update', system_instance.get_recent_readings(count))
    
    return app




































# """
# Flask Web Server - Enhanced for Single Row Google Sheets
# """

# from flask import Flask, render_template, jsonify, request
# from flask_socketio import SocketIO, emit
# from config import Config
# from datetime import datetime

# socketio = SocketIO(cors_allowed_origins="*", async_mode='threading')

# def create_app(system_instance):
#     """Create Flask application"""
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = Config.SECRET_KEY
#     socketio.init_app(app)
    
#     @app.route('/')
#     def index():
#         """Main dashboard page"""
#         return render_template(
#             'index.html',
#             config={
#                 'device_name': Config.DEVICE_NAME,
#                 'update_interval': Config.UPDATE_INTERVAL,
#                 'port': Config.PORT,
#                 'mac_address': Config.THERMOMETER_MAC_ADDRESS
#             }
#         )
    
#     @app.route('/api/status')
#     def get_status():
#         """API endpoint for system status"""
#         return jsonify(system_instance.get_status())
    
#     @app.route('/api/readings')
#     def get_readings():
#         """API endpoint for recent readings"""
#         count = request.args.get('count', default=10, type=int)
#         return jsonify(system_instance.get_recent_readings(count))
    
#     @app.route('/api/device/info')
#     def device_info():
#         """API endpoint for device information"""
#         return jsonify({
#             'mac_address': Config.THERMOMETER_MAC_ADDRESS,
#             'device_name': Config.DEVICE_NAME,
#             'update_interval': Config.UPDATE_INTERVAL,
#             'google_sheets': system_instance.google_sheets is not None,
#             'mode': 'SINGLE_ROW_UPDATE'
#         })
    
#     @app.route('/api/google-sheets/last')
#     def get_last_sheets_reading():
#         """Get last reading from Google Sheets"""
#         if system_instance.google_sheets:
#             last_reading = system_instance.google_sheets.get_last_reading()
#             if last_reading:
#                 return jsonify(last_reading)
#         return jsonify({'error': 'No Google Sheets connection'})
    
#     @socketio.on('connect')
#     def handle_connect():
#         """Handle new WebSocket connection"""
#         print(f"🌐 New client connected: {request.sid}")
        
#         # Send current status
#         emit('system_status', system_instance.get_status())
        
#         # Send current reading if available
#         if system_instance.current_reading:
#             emit('new_reading', system_instance.current_reading)
        
#         # Send recent readings
#         recent = system_instance.get_recent_readings(10)
#         if recent:
#             emit('recent_readings', recent)
    
#     @socketio.on('disconnect')
#     def handle_disconnect():
#         """Handle client disconnect"""
#         print(f"🌐 Client disconnected: {request.sid}")
    
#     @socketio.on('request_status')
#     def handle_status_request():
#         """Handle status request from client"""
#         emit('status_update', system_instance.get_status())
    
#     @socketio.on('request_readings')
#     def handle_readings_request(data):
#         """Handle readings request from client"""
#         count = data.get('count', 10)
#         emit('readings_update', system_instance.get_recent_readings(count))
    
#     @socketio.on('request_sheets_status')
#     def handle_sheets_status():
#         """Handle Google Sheets status request"""
#         sheets_status = {
#             'connected': system_instance.google_sheets is not None,
#             'mode': 'SINGLE_ROW_UPDATE',
#             'current_row': 2,
#             'timestamp': datetime.now().isoformat()
#         }
#         emit('sheets_status', sheets_status)
    
#     return app





































# """
# Flask Web Server - Enhanced for Single Row Google Sheets
# """

# from flask import Flask, render_template, jsonify, request
# from flask_socketio import SocketIO, emit
# from config import Config
# from datetime import datetime

# socketio = SocketIO(cors_allowed_origins="*", async_mode='threading')

# def create_app(system_instance):
#     """Create Flask application"""
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = Config.SECRET_KEY
#     socketio.init_app(app)
    
#     @app.route('/')
#     def index():
#         """Main dashboard page"""
#         return render_template(
#             'index.html',
#             config={
#                 'device_name': Config.DEVICE_NAME,
#                 'update_interval': Config.UPDATE_INTERVAL,
#                 'port': Config.PORT,
#                 'mac_address': Config.THERMOMETER_MAC_ADDRESS
#             }
#         )
    
#     @app.route('/api/status')
#     def get_status():
#         """API endpoint for system status"""
#         return jsonify(system_instance.get_status())
    
#     @app.route('/api/readings')
#     def get_readings():
#         """API endpoint for recent readings"""
#         count = request.args.get('count', default=10, type=int)
#         return jsonify(system_instance.get_recent_readings(count))
    
#     @app.route('/api/device/info')
#     def device_info():
#         """API endpoint for device information"""
#         return jsonify({
#             'mac_address': Config.THERMOMETER_MAC_ADDRESS,
#             'device_name': Config.DEVICE_NAME,
#             'update_interval': Config.UPDATE_INTERVAL,
#             'google_sheets': system_instance.google_sheets is not None,
#             'mode': 'SINGLE_ROW_UPDATE'
#         })
    
#     @app.route('/api/google-sheets/last')
#     def get_last_sheets_reading():
#         """Get last reading from Google Sheets"""
#         if system_instance.google_sheets:
#             last_reading = system_instance.google_sheets.get_last_reading()
#             if last_reading:
#                 return jsonify(last_reading)
#         return jsonify({'error': 'No Google Sheets connection'})
    
#     @socketio.on('connect')
#     def handle_connect():
#         """Handle new WebSocket connection"""
#         print(f"🌐 New client connected: {request.sid}")
        
#         # Send current status
#         emit('system_status', system_instance.get_status())
        
#         # Send current reading if available
#         if system_instance.current_reading:
#             emit('new_reading', system_instance.current_reading)
        
#         # Send recent readings
#         recent = system_instance.get_recent_readings(10)
#         if recent:
#             emit('recent_readings', recent)
    
#     @socketio.on('disconnect')
#     def handle_disconnect():
#         """Handle client disconnect"""
#         print(f"🌐 Client disconnected: {request.sid}")
    
#     @socketio.on('request_status')
#     def handle_status_request():
#         """Handle status request from client"""
#         emit('status_update', system_instance.get_status())
    
#     @socketio.on('request_readings')
#     def handle_readings_request(data):
#         """Handle readings request from client"""
#         count = data.get('count', 10)
#         emit('readings_update', system_instance.get_recent_readings(count))
    
#     @socketio.on('request_sheets_status')
#     def handle_sheets_status():
#         """Handle Google Sheets status request"""
#         sheets_status = {
#             'connected': system_instance.google_sheets is not None,
#             'mode': 'SINGLE_ROW_UPDATE',
#             'current_row': 2,
#             'timestamp': datetime.now().isoformat()
#         }
#         emit('sheets_status', sheets_status)
    
#     return app