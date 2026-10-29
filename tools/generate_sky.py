#!/usr/bin/env python3
"""Genera una proyección del cielo desde un archivo de configuración privado.

Uso: python3 tools/generate_sky.py /ruta/fuera-del-repositorio/sky-config.json
Dependencias de diseño: tools/requirements-sky.txt. No se usan en la web.
No publica fecha, hora, lugar ni coordenadas del observador. Solo guarda puntos
proyectados y posición solar normalizada; informe completo junto al config.
"""
import json,math,re,sys
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import numpy as np
import astropy.units as u
from astropy.coordinates import EarthLocation,AltAz,SkyCoord,get_sun
from astropy.time import Time
from astropy.utils import iers
from xml.sax.saxutils import escape

iers.conf.auto_download=False
ROOT=Path(__file__).resolve().parents[1]
CENTER=(600.,200.)
RADIUS=720.

def project(az,alt):
    # Azimuthal equidistant. Rotate the whole chart -90° for this composition.
    # This is a viewport crop of the sky above the geometric horizon.
    r=RADIUS*(90-np.asarray(alt))/90
    a=np.deg2rad(az)
    x=-r*np.sin(a); y=-r*np.cos(a)
    return CENTER[0]+y,CENTER[1]-x

def main(config_path):
    config_path=Path(config_path).resolve()
    if config_path.is_relative_to(ROOT):raise SystemExit('La configuración natal debe quedar fuera del checkout público.')
    config=json.loads(config_path.read_text())
    dt=datetime.fromisoformat(config['date']+'T'+config['local_time']).replace(tzinfo=ZoneInfo(config['timezone']))
    time=Time(dt)
    location=EarthLocation(lat=config['latitude']*u.deg,lon=config['longitude']*u.deg,height=config.get('elevation_m',0)*u.m)
    frame=AltAz(obstime=time,location=location,pressure=0*u.hPa)
    source=json.loads((ROOT/'tools/data/bright-stars-virgo.json').read_text())
    stars=source['stars']
    positions=SkyCoord(ra=[s[1] for s in stars]*u.deg,dec=[s[2] for s in stars]*u.deg,frame='icrs').transform_to(frame)
    circles=[];visible=[]
    for star,az,alt in zip(stars,positions.az.deg,positions.alt.deg):
        if alt<0:continue
        x,y=project(az,alt);mag=star[3]
        radius=max(.65,min(2.35,1.95-mag*.27))
        alpha=max(.38,min(.95,.9-mag*.1))
        circles.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius:.2f}" opacity="{alpha:.2f}"/>')
        visible.append({'hip':star[0],'azimuth':float(az),'altitude':float(alt)})
    paths=[];nodes={};coordinates=[]
    for line in source['virgo']:
        q=SkyCoord(ra=[s[0] for s in line]*u.deg,dec=[s[1] for s in line]*u.deg,frame='icrs').transform_to(frame)
        run=[]
        for az,alt in zip(q.az.deg,q.alt.deg):
            if alt<0:
                if len(run)>1:paths.append(run)
                run=[];continue
            x,y=project(az,alt);point=(round(float(x),2),round(float(y),2))
            run.append(point);nodes[point]=True;coordinates.append((float(az),float(alt)))
        if len(run)>1:paths.append(run)
    sun=get_sun(time).transform_to(frame);sx,sy=project(sun.az.deg,sun.alt.deg)
    license_text=(ROOT/'assets/sky/LICENSE-d3-celestial.txt').read_text()
    markup=['<div class="celestial-stage" aria-hidden="true">',f'<svg class="celestial-map" id="celestial-map" viewBox="0 0 1200 1000" preserveAspectRatio="xMidYMin slice" data-sun-x="{sx:.4f}" data-sun-y="{sy:.4f}" xmlns="http://www.w3.org/2000/svg">',
      '<metadata>'+escape('Star coordinates: XHIP via ofrohn/d3-celestial, J2000. Western Virgo line pattern adapted from that dataset. '+license_text)+'</metadata>',
      '<g class="sky-stars" fill="currentColor">'+''.join(circles)+'</g>', '<g class="virgo-lines" fill="none" stroke="currentColor">']
    for path in paths:
        d='M'+' L'.join(f'{x:.2f},{y:.2f}' for x,y in path)
        markup.append(f'<path d="{d}" pathLength="1"/>')
    markup.extend(['</g>','<g class="virgo-stars" fill="currentColor">'+''.join(f'<circle cx="{x}" cy="{y}" r="2.35"/>' for x,y in nodes)+'</g>','</svg></div>'])
    fragment='\n'.join(markup)
    (ROOT/'assets/sky/sky-fragment.html').write_text(fragment)
    css=f':root {{ --solar-x:{float(sx)/12:.4f}%; --solar-y:{float(sy)/10:.4f}%; }}\n'
    (ROOT/'assets/sky/solar.css').write_text(css)
    index=(ROOT/'index.html').read_text()
    region='<!-- sky:begin -->\n'+fragment+'\n<!-- sky:end -->'
    if '<!-- sky:begin -->' in index:index=re.sub(r'<!-- sky:begin -->.*?<!-- sky:end -->',lambda _:region,index,flags=re.S)
    else:index=index.replace('<div class="spot" aria-hidden="true"></div>',region+'\n  <div class="spot" aria-hidden="true"></div>',1)
    (ROOT/'index.html').write_text(index)
    private_report={'utc':time.utc.isot,'utc_offset_hours':dt.utcoffset().total_seconds()/3600,'sun_azimuth_deg':float(sun.az.deg),'sun_altitude_deg':float(sun.alt.deg),'visible_star_count':len(circles),'virgo_nodes_visible':len(nodes),'virgo_altitude_range': [min(a for _,a in coordinates),max(a for _,a in coordinates)],'location_accuracy':config.get('location_accuracy'),'refraction':False,'proper_motion':'catalogue fixed ICRS positions; no individual proper motions applied','projection':'azimuthal equidistant, rotated -90 degrees; cropped to viewport'}
    config_path.with_name('sky-report.json').write_text(json.dumps(private_report,indent=2))
    print(f'{len(circles)} stars above horizon; {len(nodes)} Virgo vertices. Sun altitude {sun.alt.deg:.2f}°, azimuth {sun.az.deg:.2f}°. Private input not copied.')

if __name__=='__main__':main(sys.argv[1])
