import json
import gpxpy
import gpxpy.gpx
import polyline
import csv
import sys

def inAnyOfRegions(vertexTuple, regionsArray):
    vertexLat, vertexLon = vertexTuple
    for region in regionsArray : 
        if ((vertexLat > region["south"]) and 
            (vertexLat < region["north"]) and
            (vertexLon > region["west"]) and
            (vertexLon < region["east"])) : 
            return True    
    return False

ConfigFilename = 'ausnet_to_gpx.json'
with open(ConfigFilename, newline='') as jsonFile:
    jsonStr = jsonFile.read()
    jsonDic = json.loads(jsonStr)
    regionsArrayCfg = jsonDic["include_regions"]
    inputFilename = jsonDic["input_filename"]

gpx = gpxpy.gpx.GPX()
gpxTrack = gpxpy.gpx.GPXTrack()
gpx.tracks.append(gpxTrack)

with open(inputFilename, newline='') as csvfile:
    ausnetReader = csv.reader(csvfile)
    for row in ausnetReader:
        gpxSegment = gpxpy.gpx.GPXTrackSegment()

        polylineEnc = row[1] 
        polylineDec = polyline.decode(polylineEnc)
        for vertexTuple in polylineDec:
            if inAnyOfRegions(vertexTuple, regionsArrayCfg) :
                vertexLat, vertexLon = vertexTuple
                gpxSegment.points.append(gpxpy.gpx.GPXTrackPoint(vertexLat, vertexLon, elevation=0))

        if len(gpxSegment.points) > 0:
            gpxTrack.segments.append(gpxSegment)    

sys.stdout.write(gpx.to_xml())
