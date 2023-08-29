# openvpn3-applet
GTK3 Applet for openvpn3 in Python

## Dependencies
* [openvpn3-linux](https://github.com/OpenVPN/openvpn3-linux)
* Notifications require [libnotify](https://gitlab.gnome.org/GNOME/libnotify)
* The killswitch feature uses `sudo`

## Configure
1. Set `OVPN_CONFIG` in your env with path to .ovpn config file or hardcode it in the script like `OVPN_CONFIG = "/path/config.ovpn"`
2. Icons used are from [openvpn-gui](https://github.com/OpenVPN/openvpn-gui). If you want to move them or use different ones, see [Icons](#Icons).
3. [openvpn3-applet.sh](./openvpn3-applet.sh) is an example wrapper script. Copy it to your $PATH and configure this repository directory, so it knows where to find the icons.

## Icons
Icons are configured:
```
CONNECTED_ICON = os.path.abspath("icons/connected.ico")
DISCONNECTED_ICON = os.path.abspath("icons/disconnected.ico")
```

Here is the previous icon config that worked for Arch Linux with [network-manager-applet](https://gitlab.gnome.org/GNOME/network-manager-applet) installed:
```
ICON_PATH = os.path.dirname(os.fspath("/usr/share/icons/hicolor/scalable/apps/"))
CONNECTED_ICON = "/nm-vpn-active-lock-symbolic.svg"
DISCONNECTED_ICON = "/nm-vpn-connecting01-symbolic.svg"
```
You can use the `os.path.dirname(os.fspath())` method to use icons from a directory of your choice, and set the icon filenames as shown here.