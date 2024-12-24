import re  # 导入正则表达式库

text = """
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

# Split the text into lines
lines = text.strip().split('\n')

# Extract variable names and remove any brackets and their contents
variable_names = [re.sub(r"\s*\[.*?\]", "", line.split(':')[0]).strip() for line in lines]
variable_names = [re.sub(r"\s*\(.*?\)", "", name).strip() for name in variable_names]

print(variable_names)