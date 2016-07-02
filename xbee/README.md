# Xbee with python
## Dependencies
TBD

## Use
TBD

## Installation
Create *99-xbee.rules* file in /etc/udev/rules.d directory with :
`KERNEL=="ttyUSB*", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", MODE="0666"
(To adapt if needed)`
