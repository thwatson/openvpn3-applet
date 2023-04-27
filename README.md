# openvpn3-applet
GTK3 Applet for openvpn3 in Python

## Dependencies
* [openvpn3-linux](https://github.com/OpenVPN/openvpn3-linux)
* Notifications require [libnotify](https://gitlab.gnome.org/GNOME/libnotify)
* The killswitch feature uses `sudo`

## Configure
1. Set `OVPN_CONFIG` with path to .ovpn config file.
2. See [Icons](#Icons), if necessary.
3. Install in `$PATH` or just run `$ ./openvpn3-applet`

## Icons
Icons are configured:
```
ICON_PATH = os.path.dirname(os.fspath("/usr/share/icons/hicolor/scalable/apps/"))
CONNECTED_ICON = "/nm-vpn-active-lock-symbolic.svg"
DISCONNECTED_ICON = "/nm-vpn-connecting01-symbolic.svg"
```
This config works for Arch Linux with [network-manager-applet](https://gitlab.gnome.org/GNOME/network-manager-applet) installed. If icons don't work, locate where your distribution installs them, or re-configure to use whatever icons you wish.