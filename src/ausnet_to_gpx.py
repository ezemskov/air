import gpxpy
import gpxpy.gpx
import polyline
import csv

gpx = gpxpy.gpx.GPX()
gpx_track = gpxpy.gpx.GPXTrack()
gpx.tracks.append(gpx_track)

#ausnetFilename = 'data/12kV_Ausnet_Victorian_Transmission_MV_Lines.txt';
ausnetFilename = 'data/22kV_Ausnet_Victorian_Sub-Transmission_MV_Lines.txt';

with open(ausnetFilename, newline='') as csvfile:
    ausnetReader = csv.reader(csvfile)
    for row in ausnetReader:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        polylineEnc = row[1] 
        polylineDec = polyline.decode(polylineEnc)
        for vertex_tuple in polylineDec:
            vertex_lat, vertex_lon = vertex_tuple
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(vertex_lat, vertex_lon, elevation=0))

gpxFile = open("ausnet_res.gpx", "w")
gpxFile.write(gpx.to_xml());
gpxFile.close();
