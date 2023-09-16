import gi
import os
import signal
import time

gi.require_versions({
    'Gtk': '3.0',
    'Gst': '1.0',
    'AppIndicator3': '0.1',
    'Notify': '0.7',
    'GLib': '2.0'
})

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from gi.repository import GLib

APPINDICATOR_ID = 'openvpn3-applet'
CONNECTED_ICON = os.path.abspath("icons/connected.ico")
DISCONNECTED_ICON = os.path.abspath("icons/disconnected.ico")
OVPN_CONFIG = os.environ.get('OVPN_CONFIG')

class Indicator():
    def __init__(self):
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, \
                DISCONNECTED_ICON, \
                appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        notify.init("sessionInfo")
        self.update_icon()

    def update_icon(self):
        # check if a session is active using `openvpn3 sessions-list`
        session_list = os.popen("openvpn3 sessions-list").read()
        if "Status: Connection, Client connected" in session_list:
            self.indicator.set_icon_full(CONNECTED_ICON, "Connected")
            # schedule the next update in 5 seconds
            GLib.timeout_add_seconds(5, self.update_icon)
        else:
            self.indicator.set_icon_full(DISCONNECTED_ICON, "Disconnected")
        return

    def build_menu(self):
        menu = gtk.Menu()

        command_one = gtk.MenuItem(label='Connect')    
        command_one.connect('activate', self.connect) 
        menu.append(command_one)                 
                                                 
        command_two = gtk.MenuItem(label='Disconnect') 
        command_two.connect('activate', self.disconnect)
        menu.append(command_two)                 
                                                 
        command_three = gtk.MenuItem(label='Kill Switch')
        command_three.connect('activate', self.kill)
        menu.append(command_three)

        command_four = gtk.MenuItem(label='Current Sessions')
        command_four.connect('activate', self.list)
        menu.append(command_four)
        
        exittray = gtk.MenuItem(label='Exit Tray')
        exittray.connect('activate', self.quit)
        menu.append(exittray)

        menu.show_all()
        return menu

    def connect(self, source):
        
        # check if a session is already active and return "connected"
        def check_connect():
            session_list = os.popen("openvpn3 sessions-list").read()
            if "Status: Connection, Client connected" in session_list:
                connected = True
            else:
                connected = False
            return connected
        
        # initiate a new session function
        def connection_start():
            sessionStart = os.popen("openvpn3 session-start --config {0}".format(OVPN_CONFIG)).read()
            notifySessionStart = notify.Notification.new(sessionStart)
            notifySessionStart.set_urgency(1)
            notifySessionStart.show()
            monitor_start()
                
        # monitor the session start function
        def monitor_start():
            time.sleep(3)
            i = 1
            while i < 8:
                connect_check = check_connect()
                if connect_check == True:
                    notifySessionConnected = notify.Notification.new("Connected")
                    notifySessionConnected.set_urgency(1)
                    notifySessionConnected.show()
                    self.update_icon()
                    return
                elif connect_check == False:
                    notifySessionConnecting = notify.Notification.new("Connecting...")
                    notifySessionConnecting.set_urgency(1)
                    notifySessionConnecting.show()
                    time.sleep(3)
                    i += 1

            notifySessionError = notify.Notification.new("Connection failed.")
            notifySessionError.set_urgency(1)
            notifySessionError.show()
            self.update_icon()
            return

        # Run checks and connect
        connect_check = check_connect()

        if connect_check == True:
            notifyActiveSession = notify.Notification.new("A session is already active.")
            notifyActiveSession.set_urgency(1)
            notifyActiveSession.show()
        else:
            connection_start()

    def disconnect(self, source):
        sessionStop = os.popen("openvpn3 session-manage --disconnect --config {0}".format(OVPN_CONFIG)).read()
        notifySessionStop = notify.Notification.new("Disconnecting", sessionStop)
        notifySessionStop.set_urgency(1)
        notifySessionStop.show()
        self.update_icon()
        
    def kill(self, source):
        self.disconnect(None)
        sessionsKill = os.popen("sudo kill -9 $(ps aux | grep openvpn3-service* | awk '{print $2}')")
        notifySessionsKill = notify.Notification.new("All openvpn-service processes killed.")
        notifySessionsKill.set_urgency(1)
        notifySessionsKill.show()
        
    def list(self, source):
        sessionsList = os.popen("openvpn3 sessions-list").read()
        notifySessionsList = notify.Notification.new("Sessions list", sessionsList)
        notifySessionsList.set_urgency(1)             
        notifySessionsList.show()

    def quit(self, source):
        session_list = os.popen("openvpn3 sessions-list").read()
        if "Status: Connection, Client connected" in session_list:
            self.disconnect(None)
            gtk.main_quit()
        else:
            gtk.main_quit()

Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
gtk.main()
