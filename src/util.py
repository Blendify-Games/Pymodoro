import pygame

def tiledsurf_slice(surf: pygame.Surface, 
                     tilewh: tuple) -> 'SurfList':
    surfs = []
    w, h = surf.get_size()
    rect = pygame.Rect(0, 0, tilewh[0], tilewh[1])
    for i in range(0, h//tilewh[1]):
        for j in range(0, w//tilewh[0]):
            rect.topleft = j*tilewh[0], i*tilewh[1]
            surfs.append(surf.subsurface(rect))
    return surfs

def tiledsurf_slice_from_path(path: str,
                               tilewh: tuple,
                               scale: 'tuple|int' = (1, 1)) -> 'SurfList':
    '''scale can be either a tuple or int'''
    surf = pygame.image.load(path)
    surf.convert_alpha()
    scale = (scale, scale) if type(scale) == int else scale
    if scale[0] > 1 or scale[1] > 1:
        tilewh = (
            tilewh[0] * scale[0],
            tilewh[1] * scale[1]
        )
        surf = pygame.transform.scale_by(surf, scale)
    return tiledsurf_slice(surf, tilewh)
