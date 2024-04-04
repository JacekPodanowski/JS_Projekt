import Render
import MapGen

# Tworzenie mapy
mapa = MapGen.Map(25, 16)

# renderownie mapy
renderer = Render.MapRenderer(mapa, 40, padding=2)
renderer.run()