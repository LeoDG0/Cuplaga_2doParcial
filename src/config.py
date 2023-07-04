#DISPLAY
WIDTH = 1600
HEIGHT = 900
CENTER = (WIDTH // 2, HEIGHT // 2)

SCREEN_SIZE = (WIDTH, HEIGHT)
SCREEN_CENTER = (WIDTH // 2, HEIGHT // 2)
ORIGIN = (0, 0)
FPS = 200

CRONOMETRO = 60

#menu
CENTER_TITULO_RECT = (WIDTH // 2, HEIGHT // 4)
WIDTH_TEXT = WIDTH // 2
HEIGHT_TEXT = HEIGHT // 4

#trampa
SIZE_TRAMP = (100, 100)
SPEED_TRAMP = 5


#BALAS
SIZE_BALAS = (80, 10)
SPEED_BULLETS = 15

#PERSONAJE
START_POS = (WIDTH // 4, HEIGHT // 2)
SIZE_CHAR = (100, 100)
SPEED_CHAR = 6
CANT_VIDAS = 5
SIZE_CORAZONES = (50, 50)

#carnation
SIZE_CARNATION = (700, 750)
SIZE_BOMBA = (40, 40)
VIDAS_DIABLO = 30
SPEED_BOMBA = 3
CANT_BOMBA = 2
BOMB_FRECUENCY = 80
DESPLAZAMIENTO_DERECHA = 300


"""#rey helado
CANT_FIRE = 2
SIZE_REY = (500, 800)
SIZE_FIRE = (40, 40)
SPEED_FIRE = 5
FIRE_FRECUENCY = 30
DESPLAZAMIENTO_DERECHA = 300"""


#COLORES
NEGRO = (0,0,0)
BLANCO = (255,255,255)
GRIS_CLARO = (224, 224, 224)
GRIS = (128,128,128)
GRIS_OSCURO = (64,64,64)
ROJO = (255,0,0)
ROJO_CLARO = (200, 0, 0)
ROSA = (255,96,208)
AZUL = (0,32,255)
AZUL_CLARO = (173, 216, 230)
VERDE = (0,192,0)
VERDE_CLARO = (0, 172, 0)
AMARILLO = (255,224,32)
NARANJA = (255,160,16)
MARRON = (160,128,96)
TRANSPARENTE = (0, 0, 0, 0)


#PATHS

#fuente
TITULO_FONT = "./src/assets/fonts/plaguard.otf" #self.font = pygame.font.Font(FUENTE_PATH)
BOTONES_FONT = "./src/assets/fonts/blomberg.otf"


#fondos
FOND_PATH = "./src/assets/images/fondos/fondoCup.jpg"
FONDO_MENU_PATH = "./src/assets/images/fondos/fondoMenu.jpg"

#trampa
TRAMP_PATH = "./src/assets/images/trampa/sierra.png"
PLATAFORMA_PATH = "./src/assets/images/trampa/plataforma2.png"

#BALAS
BALAS_PATH = "./src/assets/images/balas/balas.png"
SOUND_BALA = "./src/assets/sound/disparo.mp3"

#PERSOANE
CHAR_PATH = "./src/assets/images/personaje/avionNormal.png"
CORAZON_LLENO = "./src/assets/images/personaje/vidas/corazon lleno.png"
CORAZON_VACIO = "./src/assets/images/personaje/vidas/corazon vacio.png"
ITEM_ESPECIAL = "./src/assets/images/personaje/vidas/item vida.png"
SOUND_ITEM = "./src/assets/sound/sonidoMario.mp3"


#JEFE CARNATION
BOMBA_PATH = "./src/assets/images/bomba/bomba.png"
SOUND_BOMB = "./src/assets/sound/explosion.mp3"
SOUND_HITB = "./src/assets/sound/golpeBala.mp3"

#JEFE REY
REY_PATH = "./src/assets/images/jefeReyHelado/rey.png"
PELOTA_PATH = "./src/assets/images/pelotas/pelota.png"

#musica de fondo
MUSIC = "./src/assets/sound/musicaFondo.mp3"
SOUND_GO = "./src/assets/sound/gameOver.mp3"
