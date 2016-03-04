# Socket_Server
SmartCar Socket Server created for Casper

# Usage

- Run

   `python twistedSocketSever.py <port_number>`

- e.g `python twistedSocketServer.py 9999`
will start a socket Server listening on port 9999, some port ranges will require SUDO. 

# Protocols

### drive protocol

- syntax : `[operation_flag],[direction_flag],[angle_flag],[speed],[angle],[CR],[LF]` 

- Use unsinged 8-bit integers
- Operation flag: `for drive : 'D' hex: 0x44`
- Direction-flag: `Either 'F' hex: 0x46  for forward, or 'B' hex: 0x42 for backward`
- Angle-flag    :  `Either 'R' hex : 0x52    for Right, or 'L' hex : 0x4c for Left` 
- speed         :  `0 - 255`
- Angle         :  `0-90`
- CR            :  `0x0d`
- LF            :  `0x0a`
