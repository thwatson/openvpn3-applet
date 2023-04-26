# openvpn3-applet
GTK3 Applet for openvpn3 in Python

## Dependancies
* Icons require [OpenVPN plugin for NetworkManager](https://gitlab.gnome.org/GNOME/NetworkManager-openvpn)
* [openvpn-applet](openvpn-applet) depends on [vpn-manage](vpn-manage/vpn-manage)

## Configure & Install

### openvpn3-applet
1. Install [vpn-manage](vpn-manage/README.md)
2. Install to `$PATH` or `$ ./openvpn-applet`

### openvpn3-applet-standalone
*I haven't tested this one in a while... it might be half-baked.*

1. Edit `OVPN_CONFIG="/path/to/config.ovpn"`
2. Install to `$PATH` or `$ ./openvpn-applet-standalone`