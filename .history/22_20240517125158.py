import re

text = """
.Sol file Watershed HRU:9 Subbasin:2 HRU:7 Luse:FRST Soil: SHYYLLS Slope: 5-9999 2024/5/10 0:00:00 ArcSWAT 2012.10_7.26
Soil Name: SHYYLLS
Soil Hydrologic Group: A
Maximum rooting depth(mm) : 1000.00
Porosity fraction from which anions are excluded: 0.500
Crack volume potential of soil: 0.500
Texture 1                : SL-L
Depth                [mm]:      300.00     1000.00
Bulk Density Moist [g/cc]:        1.44        1.49
Ave. AW Incl. Rock Frag  :        0.17        0.21
Ksat. (est.)      [mm/hr]:        0.11        0.11
Organic Carbon [weight %]:        1.12        0.82
Clay           [weight %]:       21.00       21.00
Silt           [weight %]:       50.00       45.00
Sand           [weight %]:       29.00       34.00
Rock Fragments   [vol. %]:       10.00       10.00
Soil Albedo (Moist)      :        0.02        0.02
Erosion K                :        0.33        0.33
Salinity (EC, Form 5)    :        0.30        0.30
Soil pH                  :        7.80        7.90
Soil CACO3               :        9.30        9.40
"""

pattern = re.compile(r'([A-Za-z\s]+?)\s*(?:\[\w+[%\.]?\w*\])?:\s*(\d+\.\d+)')
matches = re.findall(pattern, text)

for match in matches:
    print(match)