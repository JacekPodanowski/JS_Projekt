import Render
import MapGen

# Tworzenie mapy
mapa = MapGen.Map(50, 20)

# renderownie mapy
renderer = Render.MapRenderer(mapa, 50,2,2,1280,720, padding=2)

renderer.run()