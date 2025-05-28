import pygame

def tocar_musica_fundo():
    """Toca a música de fundo padrão em loop."""
    pygame.mixer.music.load("assetsBruno/videoplayback (online-audio-converter.com).wav")
    pygame.mixer.music.set_volume(0.5)  # Volume entre 0 (mudo) e 1 (máximo)
    pygame.mixer.music.play(-1)  # -1 faz a música rodar em loop infinito

def parar_musica():
    """Para qualquer música que estiver tocando."""
    pygame.mixer.music.stop()
