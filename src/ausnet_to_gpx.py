import json
import gpxpy
import gpxpy.gpx
import polyline
import csv

def inAnyOfRegions(vertexTuple, regionsArray):
    vertexLat, vertexLon = vertexTuple

    for region in regionsArray : 
        if ((vertexLat > region["south"]) and 
            (vertexLat < region["north"]) and
            (vertexLon > region["west"]) and
            (vertexLon < region["east"])) : 
            return True;
    
    return False;

ConfigFilename = 'ausnet_to_gpx.json';
with open(ConfigFilename, newline='') as jsonFile:
    jsonStr = jsonFile.read();
    jsonDic = json.loads(jsonStr);
    regionsArrayCfg = jsonDic["include_regions"];

gpx = gpxpy.gpx.GPX()
gpxTrack = gpxpy.gpx.GPXTrack()
gpx.tracks.append(gpxTrack)

#AusnetFilename = '../data/12kV_Ausnet_Victorian_Transmission_MV_Lines.txt';
AusnetFilename = '../data/22kV_Ausnet_Victorian_Sub-Transmission_MV_Lines.txt';

with open(AusnetFilename, newline='') as csvfile:
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

gpxFile = open("ausnet_res.gpx", "w")
gpxFile.write(gpx.to_xml());
gpxFile.close();
