from datetime import datetime

# https://register.geonorge.no/data/documents/sosi-standard-del-1-generell-del_Realisering%20i%20SOSI-format%20og%20GML_v1_del1-2-realiseringsosigml-4_0_.pdf
# De følgende parameterene må kunne settes utenifra
dataeier = 'NORSAR' 
dataprodusent = 'NORSAR'   
oppdateringsdato = '20240815'
objtype = 'Kabelgrøft'
objektkatalog = ''
datauttaksdato = datetime.now().strftime("%Y%m%d%H%M%S")
sosiversjon = '4'
layer = qgis.utils.iface.activeLayer()
crsid = layer.crs().authid()
name = layer.name()
extent = layer.extent()
filename = f"{name}.sos"
unit = 0.01
objectid = 0
sosiversjon = '4.5'

crscodes = {
'EPSG:25831': 21,
'EPSG:25832': 22,
'EPSG:25833': 23,
'EPSG:25834': 24,
'EPSG:25835': 25,
'EPSG:25836': 26,
'EPSG:32631': 21,
'EPSG:32632': 22,
'EPSG:32633': 23,
'EPSG:32634': 24,
'EPSG:32635': 25,
'EPSG:32636': 26,
'EPSG:4326':84,
'EPSG:4231':87}
# Several others to add...
try:
    crscode = crscodes[crsid]
except:
    crscode = 99
    print('TRANSSYS not implemented yet')

with open (filename,'w') as outfile:
    hode=f""".HODE
..TEGNSETT UTF-8
..TRANSPAR
...KOORDSYS {crscode}
...ORIGO-NØ 0 0
...ENHET {unit}
..OMRÅDE
...MIN-NØ {round(extent.yMinimum()/unit)*unit} {round(extent.xMinimum()/unit)*unit}
...MAX-NØ {round(extent.yMaximum()/unit)*unit} {round(extent.xMaximum()/unit)*unit}
..SOSI-NIVÅ 4
..EIER {dataeier}
..OBJEKTKATALOG {objektkatalog}
..PRODUSENT {dataprodusent}
..SOSI-VERSJON {sosiversjon}"""
    print(hode)
    outfile.write(hode)
    objtype = layer.name()
    if layer.geometryType().name == 'Line':
        for feature in layer.getFeatures():
            objectid += 1
            #name=feature['id']
            objhode=f"""
.KURVE {objectid}:
..OBJTYPE {objtype}
..OPPDATERINGSDATO {oppdateringsdato}
..DATAUTTAKSDATO {datauttaksdato}
..NØ"""
            print(objhode)
            outfile.write(objhode)
            for point in feature.geometry().asPolyline():
                # name=feature['name']
                x=round(point.x()/unit)
                y=round(point.y()/unit)
                outfile.write(f"\n{y} {x}")
    else:
        print(f"{layer.geometryType().name} not implemented yet")
    outfile.write('\n.SLUTT')
print(f"\n{filename} written")