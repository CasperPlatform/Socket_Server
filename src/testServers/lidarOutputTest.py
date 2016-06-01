import serial
import svgwrite
import time
import math

def svgTest():
    #dwg = svgwrite.Drawing('test.svg', profile='tiny')
    #dwg.add(dwg.line((0, 0), (100, 100), stroke=svgwrite.rgb(10, 10, 16, '%')))
    #dwg.add(dwg.text('Test', insert=(0, 0.2), fill='red'))
    #dwg.save()
    ser = serial.Serial('/dev/cu.wchusbserial410', 115200)
    startSVG()

    time.sleep(2)

    print("test")
    ser.write("LI")

    while True:
        data = ser.readline()
        print repr(data)

        if data[0] =='c':
            break

        values = data.split(',')

    	print repr(values)

    #    values[0] = round(values[0])
    #    values[1] = round(values[1])
        values[0] = float(values[0])
        values[1] = int(values[1])

    #    if not values[0].isdigit():
    #        continue

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
