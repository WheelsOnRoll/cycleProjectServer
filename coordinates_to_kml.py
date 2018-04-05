import sys

if len(sys.argv) != 3:
    print("Usage: coordinates_to_kml.py <input_file> <output_file>")
    exit()

input_file = open(sys.argv[1], "r")
output_file = open(sys.argv[2], "w")

coordinates = ""
last_coordinate = ""

for line in input_file:
    last_coordinate = line.replace('\n', '') + ",0\n"
    coordinates = coordinates + last_coordinate

output_file.write("""
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Path</name>
    <Style id="yellowLineGreenPoly">
      <LineStyle>
        <color>7f00ffff</color>
        <width>4</width>
      </LineStyle>
      <PolyStyle>
        <color>7f00ff00</color>
      </PolyStyle>
    </Style>
    <Placemark>
      <name>File: {0}</name>
      <styleUrl>#yellowLineGreenPoly</styleUrl>
      <LineString>
        <extrude>1</extrude>
        <tessellate>1</tessellate>
        <altitudeMode>absolute</altitudeMode>
        <coordinates>
{1}
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Current Location</name>
      <Point>
        <coordinates>
          {2}
        </coordinates>
      </Point>
    </Placemark>
  </Document>
</kml>
""".format(sys.argv[1], coordinates, last_coordinate))
