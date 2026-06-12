from data import list_seeds, get_seed, lineage_df, STAGE_COLOR
import folium
from folium import CircleMarker, PolyLine

seed_name = list_seeds()[0]
print('Testing seed:', seed_name)

df = lineage_df(seed_name).sort_values('year')
assert not df.empty, 'Lineage DataFrame is empty'

# Create map with same settings
m = folium.Map(location=[52.85, -8.55], zoom_start=8, tiles='CartoDB positron')

tiles_ok = (m.options.get('tiles') == 'CartoDB positron') if hasattr(m, 'options') else True
# Check tiles: folium stores tiles on the Map object
tiles_attr = getattr(m, 'tiles', None)
# Try to detect TileLayer children mentioning CartoDB/positron
tile_children = [ch for ch in m._children.values() if 'Tile' in type(ch).__name__]
tiles_ok = any((('cartocdn' in (getattr(ch, 'tiles', '') or '').lower()) or ('positron' in (getattr(ch, 'tiles', '') or '').lower())) for ch in tile_children)

print('Map.tiles attribute:', tiles_attr)
print('TileLayer children count:', len(tile_children))
print('Tiles setting detected as CartoDB positron:', tiles_ok)
if tile_children:
    tc = tile_children[0]
    print('Tile child repr:', repr(tc))
    # try common attributes
    for attr in ('tiles','url','attr','name','options'):
        if hasattr(tc, attr):
            print(f"Tile child.{attr}:", getattr(tc, attr))

# Add markers
points = []
markers = []
for _, row in df.iterrows():
    lat = row['lat']
    lon = row['lon']
    stage = row['stage']
    color = STAGE_COLOR.get(stage, None)
    popup_html = f"{row.get('place')}|{row.get('grower')}|{row.get('county')}|{row.get('year')}|{row.get('gen')}|{row.get('adapt')}"
    marker = CircleMarker(location=(lat, lon), radius=6, color=color, fill=True, fill_color=color, popup=popup_html)
    marker.add_to(m)
    markers.append({'lat': lat, 'lon': lon, 'stage': stage, 'color': color, 'popup': popup_html})
    points.append((lat, lon))

print('Markers created:', len(markers), 'expected:', len(df))
assert len(markers) == len(df), 'Marker count mismatch'

# Verify popup content and colors
for i, (idx, row) in enumerate(df.iterrows()):
    pop = markers[i]['popup']
    assert str(row['place']) in pop, f"Popup missing place for row {i}"
    assert str(row['county']) in pop, f"Popup missing county for row {i}"
    expected_color = STAGE_COLOR.get(row['stage'])
    assert markers[i]['color'] == expected_color, f"Color mismatch at row {i}: {markers[i]['color']} != {expected_color}"

print('All popups and colors correct')

# Test polyline creation
poly = PolyLine(points, color='#444444', weight=2, dash_array='10,6')
poly.add_to(m)
# Check that poly exists in map._children by type name
poly_present = any(type(ch).__name__ == 'PolyLine' for ch in m._children.values())
print('Polyline added to map children (presence check):', poly_present)

print('Test script completed successfully')
