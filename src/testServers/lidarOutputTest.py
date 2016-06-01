import serial
import svgwrite


def svgTest():
    #dwg = svgwrite.Drawing('test.svg', profile='tiny')
    #dwg.add(dwg.line((0, 0), (100, 100), stroke=svgwrite.rgb(10, 10, 16, '%')))
    #dwg.add(dwg.text('Test', insert=(0, 0.2), fill='red'))
    #dwg.save()
    ser = serial.Serial('/dev/cu.wchusbserial1410', 115200)
    startSVG()

    time.sleep(2)

    print("test")
    ser.writeline("LI")

    while True:
        data = ser.readline()

        if data[0] == 0x04:
            break

        values = data.split(',')

        if not values[0].isdigit():
            continue

        addPoint(int(values[0]), int(values[1]))

    finishSVG()
    
def startSVG():
    global dwg
    dwg = svgwrite.Drawing('test.svg', profile='tiny')

def finishSVG():
    global dwg
    dwg.save()

def addPoint(angle, distance):
    global dwg
    global lastPoint

    x = 500
    y = 250

    firstPoint = False

    if angle == 0 or angle == 360:
        x += 0
        y -= distance
        firstPoint = True
        lastPoint = (x, y)
    elif angle < 90:
        radian = math.radians(angle)

        x += math.sin(radian)*distance
        y -= math.cos(radian)*distance
    elif angle == 90:
        x += distance
    elif angle < 180:
        radian = math.radians(angle-90)

        x += math.cos(radian)*distance
        y += math.sin(radian)*distance
    elif angle == 180:
        y += distance
    elif angle < 270:
        radian = math.radians(angle-180)

        x -= math.sin(radian)*distance
        y += math.cos(radian)*distance
    elif angle == 270:
        x -= distance
    elif angle < 360:
        radian = math.radians(angle-270)

        x -= math.cos(radian)*distance
        y -= math.sin(radian)*distance

    if not firstPoint:
        #dwg.line(start=(2*cm, (2+y)*cm), end=(18*cm, (2+y)*cm))
        dwg.add(dwg.line(lastPoint, (x, y), stroke=svgwrite.rgb(10, 10, 16, '%')))
        lastPoint = (x, y)
        
if __name__ == '__main__':
    svgTest()
