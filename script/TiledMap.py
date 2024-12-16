from pytmx import load_pygame,TiledTileLayer

class TiledMap:
    def __init__(self,file):
        self.tmx_data = load_pygame(file)
        self.map_width = self.tmx_data.width * self.tmx_data.tilewidth
        self.map_height = self.tmx_data.height * self.tmx_data.tileheight
    def draw_map(self,surface):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, TiledTileLayer):  # Vérifie que c'est un calque de tuiles
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))