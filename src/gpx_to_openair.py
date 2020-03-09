import gpxpy
import gpxpy.gpx
import sys

def degToAbsDms(deg):
    degAbs = abs(deg)
    d = int(degAbs)
    md = abs(degAbs - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [abs(d), m, sd]

def formatDms(dms):
    return '{0:0>2d}:{1:0>2d}:{2:05.2f}'.format(dms[0], dms[1], dms[2])

def latSign(deg):
    return ' ' + ('N' if (deg > 0) else 'S')

def lonSign(deg):
    return ' ' + ('E' if (deg > 0) else 'W') 


if len(sys.argv) < 2:
    sys.stderr.write("Usage : " + sys.argv[0] + " input.gpx > output_openair.txt\n")
    sys.exit()

with open(sys.argv[1], 'r') as gpxFile:
    gpx = gpxpy.parse(gpxFile)

    for gpxTrack in gpx.tracks:
        for gpxSegment in gpxTrack.segments:
            if len(gpxSegment.points) == 0:
                continue
            print('AC Q')
            print('AN Powerline')
            print('AL SFC')
            print('AH 100 ft AGL')
            for gpxPoint in gpxSegment.points:
                lat = gpxPoint.latitude
                lon = gpxPoint.longitude
                latStr = formatDms(degToAbsDms(lat)) + latSign(lat)
                lonStr = formatDms(degToAbsDms(lon)) + lonSign(lon)
                print('DP {0} {1}'.format(latStr, lonStr))
            print('\n')
