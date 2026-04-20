import csv, math

def merc(x, y):
    lon = x / 20037508.34 * 180
    lat = math.degrees(math.atan(math.exp(y / 20037508.34 * math.pi))) * 2 - 90
    return round(lat, 4), round(lon, 4)

rows = list(csv.DictReader(open('AIS_BASE_STATIONS.csv')))
nais = [r for r in rows if r['stationtype'] == 'NAIS']
loma = [r for r in rows if r['stationtype'] == 'LOMA']
print(f"NAIS: {len(nais)}   LOMA: {len(loma)}")

coords = [(merc(float(r['X']), float(r['Y'])), r['stationname']) for r in nais]
lats = [c[0][0] for c in coords]
lons = [c[0][1] for c in coords]
print(f"NAIS lat range: [{min(lats):.2f}, {max(lats):.2f}]")
print(f"NAIS lon range: [{min(lons):.2f}, {max(lons):.2f}]")
print()
print("Sample NAIS stations:")
for (lat, lon), name in coords[:10]:
    print(f"  {name:25s}  {lat:8.4f}  {lon:9.4f}")
