# Socket_Server
SmartCar Socket Server created for Casper as well as Video Server.

# Usage

- Run

   `python twistedSocketSeverSerial.py <port_number>`
   `python twistedSocketSeverVideo.py <port_number>`


- e.g `python twistedSocketServerSerial.py 9999`
- e.g `python twistedSocketServerVideo.py 9998`

will start a socket Server listening on port 9999, some port ranges will require SUDO.
will start a Video Server listening on port 9998, some port ranges will require SUDO.


# Protocols

### drive protocol

- syntax : `[token],[operation_flag],[direction_flag],[angle_flag],[speed],[angle],[CR],[LF]`

- Use unsinged 8-bit integers
- Operation flag: `for drive : 'D' hex: 0x44`
- Direction-flag: `Either 'F' hex: 0x46  for forward, or 'B' hex: 0x42 for backward`
- Angle-flag    :  `Either 'R' hex : 0x52    for Right, or 'L' hex : 0x4c for Left`
- speed         :  `0 - 255`
- Angle         :  `0-90`
- CR            :  `0x0d`
- LF            :  `0x0a`

### video stream protocol

- syntax : `[token], [video_flag], [packet amount]`

- Use unsinged 8-bit integers

Recieve the first packet and get the amount of packets.
Store all following packets until all packets have been recieved and concatenate them into one byte array.
You now have the completed image and can display it.
