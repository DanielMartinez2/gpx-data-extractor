import xml.etree.ElementTree as ET
import os
import re
import sys
from pathlib import Path

def main():
    diretorio_principal = './'
    arquivos = os.listdir(diretorio_principal)

    for arquivo in arquivos:
        if re.findall(r'\.gpx$', arquivo):
            nome_txt = 'arquivo' + arquivo.removeprefix('linha').removesuffix('.gpx') + '.txt'
            analisa_xml_escreve_txt(arquivo, nome_txt)


def analisa_xml_escreve_txt(arquivo, nome_txt):
    mytree = ET.parse(arquivo)
    myroot = mytree.getroot()
    lat = []
    long = []
    elev = []
    names = []
    description = []
    distance = []
    angles = []
    for wpt in myroot.findall("{http://www.topografix.com/GPX/1/1}wpt"):
        lat_long = wpt.attrib
        elevation = wpt.findtext("{http://www.topografix.com/GPX/1/1}ele", default='')
        desc = wpt.findtext("{http://www.topografix.com/GPX/1/1}desc", default='')
        name = wpt.findtext("{http://www.topografix.com/GPX/1/1}name", default='')
        lat.append(lat_long['lat'])
        long.append(lat_long['lon'])
        elev.append(elevation)
        names.append(name)
        description.append(desc)
        dist = desc.removeprefix('<table cellspacing="0" cellpadding="2" border="1" style="border-collapse:collapse"><tr><td><b>distance</b></td><td>').removesuffix('</td></tr></table>').rsplit('<td>')[0].removesuffix('</td></tr><tr>')
        angle = desc.removeprefix('<table cellspacing="0" cellpadding="2" border="1" style="border-collapse:collapse"><tr><td><b>distance</b></td><td>').removesuffix('</td></tr></table>').rsplit('<td>')[-1]
        angles.append(angle)
        distance.append(dist)
        


    header = 'type	latitude	longitude	altitude (m)	distance (km)	name	desc	angle \n'
    distance[0] = 0

    with open(nome_txt, 'w', encoding='utf-8') as f:
        f.write(header)
        for i in range(0, len(lat)):
            linha_1 = 'W\t{}\t{}\t{}\t{}\t{}\t{}\t{} \n'.format(lat[i],long[i], elev[i],distance[i],names[i], description[i], angles[i])
            f.write(linha_1)    
    f.close

    
if __name__ == '__main__':
    main()
