import pygame
import sys
import time

from config import *
from character import Character
from carnation import Carnation
from sprites import *

import random
import pygame.mixer
import pygame.mixer_music

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("CupLaga")
        self.reloj = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.fondo = pygame.image.load(FOND_PATH).convert()
        self.fondo = pygame.transform.scale(self.fondo, SCREEN_SIZE)
        
        #sonido
        pygame.mixer.init()
        pygame.mixer_music.load(MUSIC)
        self.sonido_explosion = pygame.mixer.Sound(SOUND_BOMB)
        self.sonido_item = pygame.mixer.Sound(SOUND_ITEM)
        self.sonido_game_over = pygame.mixer.Sound(SOUND_GO)
        self.sonido_hit_jefe = pygame.mixer.Sound(SOUND_HITB)

        #personajes
        self.carnation = Carnation(get_animations_jefe(), SIZE_CARNATION, BOMBA_PATH, SIZE_BOMBA, SPEED_BOMBA, BOMB_FRECUENCY)
        self.avion = Character(CHAR_PATH, SIZE_CHAR, START_POS)
        
        #sprites
        self.sprites = pygame.sprite.Group()
        self.balas = pygame.sprite.Group()
        self.bombas = pygame.sprite.Group()
        self.sprites.add(self.avion) 
        self.sprites.add(self.carnation)
        
        # Trampa
        self.sierra = pygame.image.load(TRAMP_PATH).convert_alpha()
        self.sierra = pygame.transform.scale(self.sierra, (70, 70))
        self.fall = True
        self.colision_ocurrida = False
        self.sierra_rect = self.sierra.get_rect()
        self.sierra_rect.center = CENTER
        

        #vidas nivel 1
        self.vidas_personaje = CANT_VIDAS
        self.vidas_jefe = VIDAS_DIABLO

        #score
        self.score_cant = 0
        
        #item vida
        self.item_rect = None
        self.item_spawn_time = None

        self.item_image = pygame.image.load(ITEM_ESPECIAL)
        self.item_image = pygame.transform.scale(self.item_image, (50, 50))

        #cronometro
        self.start_time = time.time()
        self.font = pygame.font.SysFont(None, 36)
        self.is_timer_visible = True

        #flags generales
        self.is_on = True
        self.is_playing = False
        self.is_game_over = False
        self.is_pause = False


        #flags nivel 1
        self.is_level_1 = False
        self.nivel_1_completado = False


    def play(self):
        while True:
            
            pygame.mixer_music.play(-1, 5.5)

            if self.is_on and self.is_playing == False:
                self.reloj.tick(FPS)
                self.menu_inicio()
                print("Entro menu")
            
            elif self.is_on and self.is_playing:
                if self.is_level_1:
                    
                    self.play_level_1()



#verifica con la bandera si el cronometro es visible, calcula con time.time el tiempo en segundos, se le resta
#el tiempo transcurrido y se lo resta a CRONOMETRO y se le pasa max(0, ) para que no de numeros negativos, con divmod
#se divide el tiempo en minutos y segundos, devuelve una tupla con con los valores en minutos y segundos.

    def cronometro(self):
        if self.is_timer_visible:
            elapsed_time = max(0, int(CRONOMETRO - (time.time() - self.start_time)))
            minutes, seconds = divmod(elapsed_time, 60)  #Obtengo minutos y segundos utilizando divmod()
            timer_text = self.font.render(f"{minutes:02d}:{seconds:02d}", True, BLANCO)

            timer_rect_width = 100  #Ancho del rectangulo del cronometro
            timer_rect_height = 40  #Alto del rectangulo del cronometro
            timer_rect_x = WIDTH // 2  #Posición X del rectángulo del cronometro
            timer_rect_y = 10  #Posicion Y del rectangulo del cronometro

            pygame.draw.rect(self.screen, AZUL, (timer_rect_x, timer_rect_y, timer_rect_width, timer_rect_height))
            self.screen.blit(timer_text, (timer_rect_x + 10, timer_rect_y + 10))  #Dibuja el texto del cronometro

            return elapsed_time

        return None


#carga dos imagenes que se usan para el corazon vacio y el corazon lleno, con el for se recorre la vidas del perosnaje
#y se representan como corazon con el metodo blit, usa el ancho del corazon y se le suma 5 pixeles para dejar margen entre corazones
#el segundo bucle for se itera sobre las vidas y la cantidad de vidas para saber cuantos corazones vacios se deben agregar
    def renderizar_corazones(self, vidas_personaje):
        corazon_lleno = pygame.image.load(CORAZON_LLENO).convert_alpha()
        corazon_vacio = pygame.image.load(CORAZON_VACIO).convert_alpha()
        corazon_lleno = pygame.transform.scale(corazon_lleno, SIZE_CORAZONES)
        corazon_vacio = pygame.transform.scale(corazon_vacio, SIZE_CORAZONES)

        x = 0
        for i in range(vidas_personaje):
            self.screen.blit(corazon_lleno, (x, 0))
            x += corazon_lleno.get_width() + 5

        for i in range(vidas_personaje, CANT_VIDAS):
            self.screen.blit(corazon_vacio, (x, 0))
            x += corazon_lleno.get_width() + 5




    def handler_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    self.is_pause = True
                    self.mostrar_menu_pausa()
                    self.is_pause = False
                
                if event.key == pygame.K_LEFT:
                    self.avion.speed_x = -SPEED_CHAR
                    #self.avion.current_image = 1

                if event.key == pygame.K_RIGHT:
                    self.avion.speed_x = SPEED_CHAR
                    #self.avion.current_image = 1

                if event.key == pygame.K_UP:
                    self.avion.speed_y = -SPEED_CHAR
                    self.avion.current_image = 0

                if event.key == pygame.K_DOWN:
                    self.avion.speed_y = SPEED_CHAR
                    self.avion.current_image = 5

                if event.key == pygame.K_SPACE:
                    self.avion.shoot(self.sprites, self.balas)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.avion.speed_x < 0:
                    self.avion.speed_x = 0
                    self.avion.current_image = 1
                
                if event.key == pygame.K_RIGHT and self.avion.speed_x > 0:
                    self.avion.speed_x = 0
                    self.avion.current_image = 1
                
                if event.key == pygame.K_UP and self.avion.speed_y < 0:
                    self.avion.speed_y = 0
                    self.avion.current_image = 1
                
                if event.key == pygame.K_DOWN and self.avion.speed_y > 0:
                    self.avion.speed_y = 0
                    self.avion.current_image = 1


    def jugar(self):
        self.is_playing = True
        self.is_level_1 = True
        self.restart()
        pygame.mixer_music.play(-1, 5.5)
        self.is_pause = False
        print("Entro")


    def salir(self):
        pygame.quit()
        sys.exit()



#con los parametros recibe le texto, el tamaño de la fuente, x e y son para la ubicacion del texto,
#la fuente que si no se le pasa una se declara como None y el color del texto
#si la fuente fue declara como none se usa SysFont que es una fuente predeterminada del sistema
#si no se le pasa color, se inicializa en blanco
#se crea un objeto mensaje con render() y se devuelve el objeto que se usa para mostrar el texto
    def texto(self, texto, tamaño, x, y, fuente=None, color=None):
        if fuente is None:
            fuente = pygame.font.SysFont(None, tamaño)
        elif isinstance(fuente, str):
            fuente = pygame.font.Font(fuente, tamaño)
        
        if color is None:
            color = BLANCO
        
        mensaje = fuente.render(texto, True, color)
        return mensaje




#se usa mouse.get_pos() para obtener las coordenadas del mouse mediante una tupla, se verifica con get_pressed()
#si se hace algun clic en el mouse, devuelve una tupla con 3 valores el cual el valor [0] significa que se hizo clic
#en las variables centro se calcula el centro del rectangulo del boton
#en el if verifica si las coordenadas del mouse estan sobre el area del boton y si es true se dibuja un rectangulo sobre el boton con un color mas claro
#si se hace clic se usa la funcion accion que recibio por parametro
#se usa el metodo texto() para crear los botones y con get rect delimita el boton de cad texto
    def dibujarBoton(self, x, y, ancho, alto, colorActivo, colorInactivo, texto, accion=None):
        cursor = pygame.mouse.get_pos()
        clic = pygame.mouse.get_pressed()

        #Calcula las coordenadas del centro medio del rectangulo
        centro_x = x + ancho // 2
        centro_y = y + alto // 2

        if x + ancho > cursor[0] > x and y + alto > cursor[1] > y:
            pygame.draw.rect(self.screen, colorActivo, (x, y, ancho, alto))

            #Si se hace clic en el boton, ejecuta la accion correspondiente
            if clic[0] == 1 and accion is not None:
                accion()
                print("Entro accion")
        else:
            pygame.draw.rect(self.screen, colorInactivo, (x, y, ancho, alto))

        
        mensaje = self.texto(texto, 30, centro_x, centro_y, BOTONES_FONT)
        mensaje_rect = mensaje.get_rect(center=(centro_x, centro_y))
        self.screen.blit(mensaje, mensaje_rect)


    def menu_inicio(self):
        
        while self.is_on and self.is_playing == False:
            #Controla los eventos del teclado y el mouse
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sys.exit()

            #Dibuja el fondo del menu
            fondo_menu = pygame.image.load(FONDO_MENU_PATH).convert()
            fondo_menu = pygame.transform.scale(fondo_menu, SCREEN_SIZE)
            self.screen.blit(fondo_menu, (0, 0))

            #Dibuja el titulo del juego centrado en la pantalla
            texto_titulo = self.texto('CupLaga', 200, WIDTH_TEXT, HEIGHT_TEXT, TITULO_FONT, NARANJA)
            texto_titulo_rect = texto_titulo.get_rect(center = CENTER_TITULO_RECT)
            self.screen.blit(texto_titulo, texto_titulo_rect)

            #Dibuja el boton para jugar
            self.dibujarBoton(WIDTH / 2.5, 400, 300, 50, VERDE, VERDE_CLARO, "Jugar", self.jugar)
            #Dibuja el boton para salir
            self.dibujarBoton(WIDTH / 2.5, 500, 300, 50, ROJO, ROJO_CLARO, "Salir", self.salir)

            #Actualiza la pantalla
            pygame.display.update()


    def musica_on(self):
            pygame.mixer_music.unpause()


    def musica_off(self):
        pygame.mixer_music.pause()


    def mostrar_menu_pausa(self):
        
        self.is_playing = False
        #pygame.mixer_music.stop()
        while self.is_pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_playing = True
                        return
            
            self.avion.speed_x = 0
            self.avion.speed_y = 0

            #Dibujar el menu de pausa en la pantalla
            texto_pausa = self.texto("Pausa", 100, WIDTH / 2, HEIGHT / 3, BOTONES_FONT, ROJO)
            texto_pausa_rect = texto_pausa.get_rect(center=(WIDTH / 2, HEIGHT / 4))
            self.screen.blit(texto_pausa, texto_pausa_rect)

            self.dibujarBoton(WIDTH // 2 - 150, 450, 300, 50, ROJO, ROJO_CLARO, "Menu Principal", self.menu_inicio)
            self.dibujarBoton(WIDTH // 2 - 100, 550, 200, 50, VERDE, VERDE_CLARO, "Reiniciar", self.jugar)
            self.dibujarBoton(WIDTH // 2 - 100, 300, 200, 50, AZUL, AZUL_CLARO, "Musica ON", self.musica_on)
            self.dibujarBoton(WIDTH // 2 - 100, 350, 200, 50, AZUL, AZUL_CLARO, "Musica OFF", self.musica_off)

            self.reloj.tick(60)
            pygame.display.flip()



#level 1

#renderiza los metodos necesarios para el nivel 1 y la pantalla del juego
    def play_level_1(self):
            
            while self.is_on and self.is_playing and not self.nivel_1_completado:
                self.reloj.tick(FPS)
                self.handler_events()
                self.render_level_1()
                pygame.display.flip()


#actualiza todos los prites que se le pasa, la imagen de fondo, los sprites de las bombas y todo lo que se necesita para el nivel 1
    def render_level_1(self):
        self.sprites.update()
        self.carnation.update()
        self.balas.update()
        self.carnation.bombs.update()
        self.screen.blit(self.fondo, ORIGIN)
        self.collide_detection_level_1()
        self.sprites.draw(self.screen)
        self.carnation.bombs.draw(self.screen)
        self.cronometro()
        self.generate_item_vida()
        self.renderizar_corazones(self.vidas_personaje)
        self.mostrar_puntaje(self.screen, self.score_cant, BOTONES_FONT, BLANCO)
        self.sierra_trampa()


#reinicia el movimimiento del personaje, las vidas, la ubicacion, las bombas, el cronometro y el score
    def restart(self):
        self.vidas_personaje = CANT_VIDAS
        self.vidas_jefe = VIDAS_DIABLO
        self.avion.rect.center = START_POS
        self.carnation.reset_bombs()
        self.avion.reset_movement()
        self.score_cant = 0
        self.start_time = time.time()


#menu de game over que frena los elementos, la musica y reproduce la musica de game over, ademas utiliza los metodos de texto y botones para
#crear los botones de reinicio y menu principal y ademas muestra el score obtenido de la partida
    def game_over(self):
        
        self.is_playing = False
        pygame.mixer_music.stop()
        self.sonido_game_over.play()
        self.stop_elements()
        
        # Menú de Game Over
        while self.is_on and self.is_playing == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.fondo, ORIGIN)

            #Dibuja el titulo centrado en la pantalla
            texto_game_over = self.texto("GAME OVER", 80, WIDTH / 2, HEIGHT / 3, TITULO_FONT, ROJO)
            texto_game_over_rect = texto_game_over.get_rect(center=(WIDTH / 2, HEIGHT / 3))
            self.screen.blit(texto_game_over, texto_game_over_rect)

            texto_score = self.texto(f"SCORE: {self.score_cant}", 80, WIDTH / 2, HEIGHT / 3, BOTONES_FONT, ROJO)
            texto_score_rect = texto_score.get_rect(center=(WIDTH / 2, 400))
            self.screen.blit(texto_score, texto_score_rect)

            #Dibuja el boton "Menu Principal"
            self.dibujarBoton(WIDTH / 2.5, 550, 300, 50, ROJO, ROJO_CLARO, "Menu Principal", self.menu_inicio)

            #Dibuja el boton "Reiniciar"
            self.dibujarBoton(WIDTH / 2.5, 650, 300, 50, VERDE, VERDE_CLARO, "Reiniciar", self.jugar)

            pygame.display.update()


#frena todo los sprites con el metood stop() el cual la mayoria setea la velocidad en 0
    def stop_elements(self):
            for sprite in self.sprites:
                sprite.stop()


#detecta las colisiones y setea el game over o la aparicion del item de vida
    def collide_detection_level_1(self):
        

        if self.colision_circulos(self.sierra_rect, self.avion.rect):
            self.colision_ocurrida = True
            self.vidas_personaje -= 1
            """if self.colision_ocurrida:
                self.colision_ocurrida = False"""
            print("choco sierra")

        for bala in self.balas:
            impactos = pygame.sprite.spritecollide(bala, self.carnation.bombs, True)
            if impactos:
                self.sonido_explosion.play()
                bala.kill()
                self.score_cant += 10

        for bala in self.balas:
            if pygame.sprite.collide_mask(bala, self.carnation):
                self.sonido_hit_jefe.play()
                self.vidas_jefe -= 1
                bala.kill()
                self.score_cant += 5

        for bomba in self.carnation.bombs:
            if pygame.sprite.collide_mask(bomba, self.avion):
                self.sonido_explosion.play()
                bomba.kill()
                self.vidas_personaje -= 1
        
        if self.vidas_jefe != 0 and self.vidas_personaje != 0 and self.cronometro() <= 0:
            print("fin del tiempo")
            self.game_over()

        if self.item_rect is not None and self.item_rect.colliderect(self.avion):
            self.sonido_item.play()
            self.vidas_personaje += 1
            self.item_rect = None
            self.item_spawn_time = None

        if self.vidas_personaje == 0:
            self.game_over()
            self.score_cant = 0

        if self.vidas_jefe == 0:
            #self.nivel_1_completado = True
            #if self.score_cant > 100:
            self.game_over()


#verifica que no haya un item presente en el juego, verifica que la vidas del personaje sea menor a la incial
#si se todo es true, se genera un nuevo item aleatoreamente con randint, se verifica si el item aparecio mas de la mitad
#de la pantalla y se vuelve a generar otro item si fuera el caso, para que el item no spawnee sobre el jefe
#se crea un rectangulo con pygame.Rect
    def generate_item_vida(self):
        
        if self.item_rect is None and self.item_spawn_time is None and self.vidas_personaje < CANT_VIDAS:
            x = random.randint(0, WIDTH - 50)
            y = random.randint(0, HEIGHT - 50)

            #ajusta el rango del eje x para que no pase de mitad de pantalla
            if x > WIDTH / 2:
                x = random.randint(0, int(WIDTH / 2 + 100) - 50)

            self.item_rect = pygame.Rect(x, y, 50, 50)
            #self.item_spawn_time = time.time()

        if self.item_rect is not None:
            self.screen.blit(self.item_image, self.item_rect)


    def mostrar_puntaje(self, ventana, puntaje, fuente_path, color):
        
        fuente = pygame.font.Font(fuente_path, 48)
        # Crea el objeto de texto con el puntaje y los parámetros de fuente y color
        texto_puntaje = fuente.render(f"SCORE: {puntaje}", True, color)
        # Obtiene el rectángulo del texto
        rect_puntaje = texto_puntaje.get_rect()
        # Establece la posición del rectángulo en la parte superior derecha de la pantalla
        rect_puntaje.topright = ventana.get_rect().topright
        # Dibuja el texto en la ventana
        ventana.blit(texto_puntaje, rect_puntaje)


    def sierra_trampa(self):
        
        if self.fall:
            if self.sierra_rect.bottom <= HEIGHT:
                self.sierra_rect.y += SPEED_TRAMP
            else:
                self.fall = False
        else:
            if self.sierra_rect.top > 0:
                self.sierra_rect.y -= SPEED_TRAMP
            else: 
                self.fall = True

        self.screen.blit(self.sierra, self.sierra_rect)


    def colision_circulos(self, rect1:pygame.Rect, rect2:pygame.Rect):
        colision = False

        cateto_x = rect1.centerx - rect2.centerx
        cateto_y = rect1.centery - rect2.centery
        
        limite = rect1.width // 2 + rect2.width // 2

        distancia = (cateto_x ** 2 + cateto_y ** 2) ** 0.5

        if distancia <= limite:
            colision = True
        
        return colision