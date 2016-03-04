datarec = bytearray()
for byte in data:
    datarec.append(ord(byte))
    if hex(ord(byte)) == '0xd':
        tmp = byte
        continue
    if tmp != '':
        if hex(ord(byte)) == '0xa' and hex(ord(tmp)) == '0xd':
            print 'got CLRF'
            break
if datarec[0] != typeFlag.Drive:
     print 'unknown typeFlag...aborting'
     return
else:
    tf = typeFlag.Drive
    print 'this is a driveMsg'

if datarec[1] == directionFlag.forward || datarec[1] == directionFlag.Backward || datarec[1] == directionFlag.Idle:
    if datarec[1] == directionFlag.Forward:
        print 'direction: Forward'
        df = directionFlag.Forward
    if datarec[1] == directionFlag.Backward:
        print 'direction: Right'
        df = directionFlag.Backward
    if datarec[1] == directionFlag.Idle:
        print 'direction: Idle'
        df = directionFlag.Idle

else:
    print 'unknown DirectionFlag..aborting'
    return
if datarec[2] == angleFlag.Right || datarec[1] == angleFlag.Left || datarec[1] == angleFlag.Idle:
    if datarec[2] == angleFlag.Right:
        print 'angle: Right'
        df = angleFlag.Right
    if datarec[2] == angleFlag.Left:
        print 'angle: Left'
        df = angleFlag.Left
    if datarec[2] == angleFlag.Idle:
        print 'angle: Idle'
        df = angleFlag.Idle
else:
    print 'unknown DirectionFlag..aborting'
    return
if datarec[3] < 0 || datarec[3] > 255:
    print 'invalid Speed Value, aborting...'
    return
else:
    if df.name == directionFlag.Forward:
        speed = datarec[3]
    elif df.name == directionFlag.Backward:
        speed = ~datarec[3]+1
    elif df.name == directionFlag.Idle:
        speed = 0

if datarec[4] < 0 || datarec[4] > 90:
    print 'invalid Angle Value, aborting...'
    return
else:
    if af.name == angleFlag.Right:
        angle = datarec[4]
    elif af.name == angleFlag.Left:
        angle = ~datarec[4]+1
    elif af.name == angleFlag.Idle:
        angle = 0
