import pygame

def tocar_musica_fundo():
    """Toca a música de fundo padrão em loop."""
    pygame.mixer.music.load("assets/snd/videoplayback (online-audio-converter.com).wav")
    pygame.mixer.music.set_volume(0.5)  
    pygame.mixer.music.play(-1)  

def parar_musica():
    """Para qualquer música que estiver tocando."""
    pygame.mixer.music.stop()
