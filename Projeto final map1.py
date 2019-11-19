# -*- coding: utf-8 -*-

# Importando as bibliotecas necessárias.
import pygame, time
from os import path
#from pygame_functions import *

# Estabelece a pasta que contem as figuras.
img_dir = path.join(path.dirname(__file__), 'imagens_rep')
snd_dir = path.join(path.dirname(__file__), 'sons_rep')


# Dados gerais do jogo.
WIDTH = 1300 # Largura da tela
HEIGHT = 700 # Altura da tela
TILE_SIZE = 40 # Tamanho de cada tile (cada tile é um quadrado)
PLAYER_WIDTH = TILE_SIZE
PLAYER_HEIGHT = int(TILE_SIZE * 1.5)
FPS = 60 # Frames por segundo

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define a aceleração da gravidade
GRAVITY = 1.5
# Define a velocidade inicial no pulo
JUMP_SIZE = 25
# Define a altura do chão
GROUND = HEIGHT * 5 // 6

# Define ações do player
IDLE = 0
RIGHT = 1
LEFT = 2
JUMP = 3
FALL = 4
JUMP_LEFT = 5
FALL_LEFT = 6
IDLE_LEFT = 7
ICED = 8 
ICED_LEFT = 9
POS = [IDLE, RIGHT, JUMP, FALL,ICED]
NEG = [LEFT, JUMP_LEFT, FALL_LEFT, IDLE_LEFT,ICED_LEFT]

# Define ações do mob
ATTACK = 8
DEAD = 9

# Define os tipos de tiles
BLOCK = 0
EMPTY = -1

# Define o mapa com os tipos de tiles
MAP1 = [
    
    [],    
    [],
    [],
    [],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY, EMPTY, EMPTY, EMPTY, BLOCK, BLOCK, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY, EMPTY, EMPTY, EMPTY, BLOCK,BLOCK, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [],
    [],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BLOCK, EMPTY, EMPTY, EMPTY, EMPTY],    
    [BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY, EMPTY, EMPTY, EMPTY],
    [],    
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK],
    [],    
    [BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY, EMPTY, EMPTY, EMPTY],
    [],    
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK],    
    [],
    [BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, EMPTY, EMPTY, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, EMPTY,EMPTY, BLOCK, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK]
    ]




# Class que representa os blocos do cenário
class Tile(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, row, column):

        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        tile_img = pygame.image.load(path.join(img_dir, "ground2.png")).convert()

        # Aumenta o tamanho do tile.
        tile_img = pygame.transform.scale(tile_img, (TILE_SIZE, TILE_SIZE))

        # Define a imagem do tile.
        self.image = tile_img
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        # Posiciona o tile
        self.rect.x = TILE_SIZE * column
        self.rect.y = TILE_SIZE * row

# Classe Jogador que representa Jack
class Player(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, row, column, blocks):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        #Cria spritesheet
        spritesheet =    [pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_000.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_001.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_002.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_003.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_004.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_005.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_006.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_007.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_008.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_009.png")).convert(),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_000.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_001.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_002.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_003.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_004.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_005.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_006.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_007.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_008.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_009.png")).convert(), True, False),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Jump_000.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_000.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_001.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_002.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_003.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_004.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_005.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_006.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_007.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_008.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_009.png")).convert(),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Jump_000.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_000.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_001.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_002.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_003.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_004.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_005.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_006.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_007.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_008.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_009.png")).convert(), True, False),        
                          pygame.image.load(path.join(img_dir, "rapazinhoAzul.png")).convert(),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "rapazinhoAzul.png")).convert(), True,False)] 
                          
        i = 0
        while i < len(spritesheet):
            spritesheet[i] = pygame.transform.scale(spritesheet[i],(40,38))
            self.image = spritesheet[i]
            self.image.set_colorkey(BLACK)
            i += 1
        
        # Carregando a imagem de fundo.
        self.animations = {IDLE:spritesheet[0:10], 
                           LEFT:spritesheet[10:20], 
                           JUMP:spritesheet[20:21], 
                           FALL:spritesheet[20:21], 
                           RIGHT:spritesheet[21:31],
                           JUMP_LEFT:spritesheet[31:32],
                           FALL_LEFT:spritesheet[31:32],
                           IDLE_LEFT:spritesheet[32:42],
                           ICED:spritesheet[42:43],
                           ICED_LEFT:spritesheet[43:44]} 
        
        
        # Define estado atual (que define qual animação deve ser mostrada)
        self.state = IDLE
        # Define animação atual
        self.animation = self.animations[self.state]
        # Inicializa o primeiro quadro da animação
        self.frame = 0
        self.image = self.animation[self.frame]
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Guarda o grupo de blocos para tratar as colisões
        self.blocks = blocks
        
        # Define posição inicial.
        self.rect.x = row * TILE_SIZE - 600
        self.rect.bottom = column * TILE_SIZE
        
        
        # Velocidade K_UP de Jack
        self.speedx = 0
        self.speedy = 0
        
        # Guarda o tick da primeira imagem
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 100
        self.freeze_ticks = 1500
        self.startfreeze_ticks = 0
    def freeze(self): 
        self.prevstate = self.state 
        if self.state in POS:
            self.state = ICED 
        elif self.state in NEG:
            self.state = ICED_LEFT
        self.frame = 0 
        self.animation = self.animations[self.state]
        self.image = self.animation[self.frame]
        self.startfreeze_ticks = pygame.time.get_ticks()
        
    # Metodo que atualiza a posição de Jack
    def update(self):
        # Vamos tratar os movimentos de maneira independente.
        # Primeiro tentamos andar no eixo y e depois no x.
         # Verifica o tick atual.
        now = pygame.time.get_ticks()
        if self.state == ICED or self.state == ICED_LEFT: 
            
            elapsed_ticks = now - self.startfreeze_ticks
            if elapsed_ticks > self.freeze_ticks: 
                self.state = self.prevstate
            else: 
                return 
                
            
            
        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:

            # Marca o tick da nova imagem.
            self.last_update = now
            
            # Avança um quadro.
            self.frame += 1
        
            # Atualiza animação atual
            self.animation = self.animations[self.state]
            # Reinicia a animação caso o índice da imagem atual seja inválido
            if self.frame >= len(self.animation):
                self.frame = 0
            
            # Armazena a posição do centro da imagem
            center = self.rect.center
            # Atualiza imagem atual
            self.image = self.animation[self.frame]
            # Atualiza os detalhes de posicionamento
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
        # Tenta andar em y
        # Atualiza a velocidade aplicando a aceleração da gravidade
        self.speedy += GRAVITY
        # Atualiza a posição y
        self.rect.y += self.speedy

        
        # Se colidiu com algum bloco, volta para o ponto antes da colisão
        collisions = pygame.sprite.spritecollide(self, self.blocks, False)
        # Atualiza o estado para caindo
        if self.speedy > 0 and self.state == JUMP:
            self.state = FALL
        elif self.speedy > 0 and self.state == JUMP_LEFT:
            self.state = FALL_LEFT

        # Corrige a posição do personagem para antes da colisão
        for collision in collisions:
            # Estava indo para baixo
            if self.speedy > 0:
                self.rect.bottom = collision.rect.top
                # Atualiza o estado para parado
                if self.state == FALL:
                    self.state = IDLE
                elif self.state == FALL_LEFT:
                    self.state = IDLE_LEFT
                # Se colidiu com algo, para de cair
                self.speedy = 0
                
            # Estava indo para cima
            elif self.speedy < 0:
                self.rect.top = collision.rect.bottom
                # Atualiza o estado para parado
                if self.state == FALL:
                    self.state = IDLE
                elif self.state == FALL_LEFT:
                    self.state = IDLE_LEFT
                # Se colidiu com algo, para de cair
                self.speedy = 0
                
               
        if self.state == IDLE or self.state == IDLE_LEFT:
            # Define variável para caminhar
            keys = pygame.key.get_pressed()    
            # Verifica se está segurando alguma tela
            if keys[pygame.K_RIGHT] == True and keys[pygame.K_LEFT] == False:
                self.state = RIGHT
            elif keys[pygame.K_LEFT] == True and keys[pygame.K_RIGHT] == False:
                self.state = LEFT
                

        # Tenta andar em x
        self.rect.x += self.speedx
        # Corrige a posição caso tenha passado do tamanho da janela
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH - 1
        # Se colidiu com algum bloco, volta para o ponto antes da colisão
        collisions = pygame.sprite.spritecollide(self, self.blocks, False)
        # Corrige a posição do personagem para antes da colisão
        for collision in collisions:
            # Estava indo para a direita
            if self.speedx > 0:
                self.rect.right = collision.rect.left
            # Estava indo para a esquerda
            elif self.speedx < 0:
                self.rect.left = collision.rect.right

    # Método que faz o personagem pular
    def jump(self):               
        # Só pode pular se ainda não estiver pulando ou caindo
        if self.speedy != 0:
            self.state = JUMP            
        elif self.state == IDLE or self.state == RIGHT:
            self.speedy -= JUMP_SIZE
            self.state = JUMP
        elif self.state == IDLE_LEFT or self.state == LEFT:
            self.speedy -= JUMP_SIZE
            self.state = JUMP_LEFT
    
# Classe Bullet que representa os tiros
class Bullet(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, x, y, blocks, mob):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        bullet_img = pygame.image.load(path.join(img_dir, "bala2.png")).convert()
        self.image = pygame.transform.scale(bullet_img,(8,8))
        
        # Arrumando tamanho da imagem
        
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Guarda o grupo de blocos para tratar as colisões
        self.blocks = blocks
        
        # Guarda o grupo de blocos para tratar as colisões
        self.mob = mob
        
        # Coloca no lugar inicial definido em x, y do constutor
        if player.state in POS:
            self.rect.bottom = y+30
            self.rect.centerx = x+10
            self.speedx = 20
        if player.state in NEG:
            self.rect.bottom = y+30
            self.rect.centerx = x-10
            self.speedx = -20

    # Metodo que atualiza a posição da bala
    def update(self):
        self.rect.x += self.speedx
        self.mask = pygame.mask.from_surface(self.image)
        
        # Se o tiro passar do fim da tela, morre.
        if self.rect.x > 1300 or self.rect.x < 0:
            self.kill()
        
        # Se colidiu com algum bloco, morre
        collisions = pygame.sprite.spritecollide(self, self.blocks, False)
        # Corrige a posição do personagem para antes da colisão
        if len(collisions) > 0:
            self.kill()

# Classe Mob que representa os meteoros
class Mob(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, x, y, blocks, fire):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        spritesheetmob = [pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (2).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (3).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (4).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (5).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (6).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (7).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (8).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (9).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (10).png")).convert(),
                          pygame.image.load(path.join(img_dir, "dead (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "dead (2).png")).convert(),
                          pygame.image.load(path.join(img_dir, "dead (3).png")).convert(),
                          pygame.image.load(path.join(img_dir, "dead (4).png")).convert(),
                          pygame.image.load(path.join(img_dir, "dead (5).png")).convert(),
                          pygame.image.load(path.join(img_dir, "dead (6).png")).convert()
                          ]

        
        
        i = 0
        while i < len(spritesheetmob):
            spritesheetmob[i] = pygame.transform.scale(spritesheetmob[i],(50,73))
            self.image = spritesheetmob[i]
            self.image.set_colorkey(BLACK)
            i += 1
        
        # Carregando a imagem de fundo.
        self.animations = {ATTACK:spritesheetmob[0:25],
                           DEAD:spritesheetmob[26:31]}
        
        self.morre = False
        self.state = ATTACK 
        # Define estado atual (que define qual animação deve ser mostrada)
        if self.state == ATTACK:
            
        # Define animação atual
            self.animation = self.animations[self.state]
            # Inicializa o primeiro quadro da animação
            self.frame = 0
            self.image = self.animation[self.frame]
            
            # Detalhes sobre o posicionamento.
            self.rect = self.image.get_rect()
            
        if self.state == DEAD:
            
        # Define animação atual
            self.animation = self.animations[self.state]
            # Inicializa o primeiro quadro da animação
            self.frame = 0
            self.image = self.animation[self.frame]
            
            
            # Detalhes sobre o posicionamento.
            self.rect = self.image.get_rect()
    
        # Guarda o grupo de blocos para tratar as colisões
        self.blocks = blocks
        self.fire = fire
        
        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.bottom = y + 300
        self.rect.centerx = x + 1200
        self.speedx = 0
        self.speedy = 0
        
        # Guarda o tick da primeira imagem
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 100
        
    # Metodo que atualiza a posição de mob
    def update(self):
        # Vamos tratar os movimentos de maneira independente.
        # Primeiro tentamos andar no eixo y e depois no x.
        
        # Verifica o tick atual.
        now = pygame.time.get_ticks()

        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        if self.state == DEAD and self.frame == 4:
            self.morre = True


        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:
            if self.frame == 24:
                self.fire = True
            else:
                self.fire = False

            # Marca o tick da nova imagem.
            self.last_update = now
            
            # Avança um quadro.
            self.frame += 1
        
            # Atualiza animação atual
            self.animation = self.animations[self.state]
            # Reinicia a animação caso o índice da imagem atual seja inválido
            if self.frame >= len(self.animation):
                self.frame = 0
            
            # Armazena a posição do centro da imagem
            center = self.rect.center
            # Atualiza imagem atual
            self.image = self.animation[self.frame]
            self.mask = pygame.mask.from_surface(self.image)
            # Atualiza os detalhes de posicionamento
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
            
        # Tenta andar em y
        # Atualiza a velocidade aplicando a aceleração da gravidade
        self.speedy += GRAVITY
        # Atualiza a posição y
        self.rect.y += self.speedy
        
        # Se colidiu com algum bloco, volta para o ponto antes da colisão
        collisions = pygame.sprite.spritecollide(self, self.blocks, False)

        # Corrige a posição do personagem para antes da colisão
        for collision in collisions:
            # Estava indo para baixo
            if self.speedy > 0:
                self.rect.bottom = collision.rect.top
                self.speedy = 0
                
            # Estava indo para cima
            elif self.speedy < 0:
                self.rect.top = collision.rect.bottom
                self.speedy = 0 

# Classe Arrow que representa flechas
class Arrow(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, x, y, speedx, speedy):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        arrow_img = pygame.image.load(path.join(img_dir, "arrow.png")).convert()
        self.image = pygame.transform.scale(arrow_img,(30,5))
        
        # Arrumando tamanho da imagem
        
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.centery = y
        self.rect.centerx = x
        self.cx = x
        self.cy = y
        self.speedx = speedx
        self.speedy = speedy

    # Metodo que atualiza a posição da bala
    def update(self):
        self.cx += self.speedx
        self.cy += self.speedy
        self.rect.x = int(self.cx)
        self.rect.y = int(self.cy)
        self.mask = pygame.mask.from_surface(self.image)
        # Se o tiro passar do fim da tela, morre.
        if self.rect.x > 1300 or self.rect.x < 0:
            self.kill()

#Classe que representa os Magos 
class Magician(pygame.sprite.Sprite):
    #Construtor da Classe 
    def __init__(self, x, y, blocks, fire):
        # Construtor da classe Final (sprite) 
        pygame.sprite.Sprite.__init__(self)
        
        spritesheetmag =  [
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_000.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_000.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_002.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_003.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_004.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_005.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_006.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_007.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_008.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_009.png" )).convert(),True, False),
                           ]
        i = 0
        while i < len(spritesheetmag):
            spritesheetmag[i] = pygame.transform.scale(spritesheetmag[i],(50,44))
            self.image = spritesheetmag[i]
            self.image.set_colorkey(BLACK)
            i += 1
         # Carregando a imagem de fundo.
        self.animations = {ATTACK:spritesheetmag[0:22]}
        
        
        # Define estado atual (que define qual animação deve ser mostrada)
        self.state = ATTACK
        # Define animação atual
        self.animation = self.animations[self.state]
        # Inicializa o primeiro quadro da animação
        self.frame = 0
        self.image = self.animation[self.frame]
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Guarda o grupo de blocos para tratar as colisões
        self.blocks = blocks
        self.fire = fire
        
        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 0
        self.speedy = 0
        
        # Guarda o tick da primeira imagem
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 100
        
    # Metodo que atualiza a posição dos Magos 
    def update(self):
        # Vamos tratar os movimentos de maneira independente.
        # Primeiro tentamos andar no eixo y e depois no x.
        
        # Verifica o tick atual.
        now = pygame.time.get_ticks()

        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:
            if self.frame == 21:
                self.fire = True
            else:
                self.fire = False

            # Marca o tick da nova imagem.
            self.last_update = now
            
            # Avança um quadro.
            self.frame += 1
        
            # Atualiza animação atual
            self.animation = self.animations[self.state]
            # Reinicia a animação caso o índice da imagem atual seja inválido
            if self.frame >= len(self.animation):
                self.frame = 0
            
            # Armazena a posição do centro da imagem
            center = self.rect.center
            # Atualiza imagem atual
            self.image = self.animation[self.frame]
            self.mask = pygame.mask.from_surface(self.image)
            # Atualiza os detalhes de posicionamento
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
            
        # Tenta andar em y
        # Atualiza a velocidade aplicando a aceleração da gravidade
        self.speedy += GRAVITY
        # Atualiza a posição y
        self.rect.y += self.speedy
        
        # Se colidiu com algum bloco, volta para o ponto antes da colisão
        collisions = pygame.sprite.spritecollide(self, self.blocks, False)

        # Corrige a posição do personagem para antes da colisão
        for collision in collisions:
            # Estava indo para baixo
            if self.speedy > 0:
                self.rect.bottom = collision.rect.top
                self.speedy = 0
                
            # Estava indo para cima
            elif self.speedy < 0:
                self.rect.top = collision.rect.bottom
                self.speedy = 0 
        

class Ice(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, x, y, speedx, speedy):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        arrow_img = pygame.image.load(path.join(img_dir, "ice spell.png")).convert()
        self.image = pygame.transform.scale(arrow_img,(15,14))
        
        # Arrumando tamanho da imagem
        
        
        # Deixando transparente.
        self.image.set_colorkey(WHITE)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.centery = y
        self.rect.centerx = x
        self.cx = x
        self.cy = y
        self.speedx = speedx
        self.speedy = speedy


    # Metodo que atualiza a posição da bala
    def update(self):
        self.cx += self.speedx
        self.cy += self.speedy
        self.rect.x = int(self.cx)
        self.rect.y = int(self.cy)
        self.mask = pygame.mask.from_surface(self.image)
        # Se o tiro passar do fim da tela, morre.
        if self.rect.x > 1300 or self.rect.x < 0:
            self.kill()



# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()


# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("Jack")

# Variável para o ajuste de velocidade
clock = pygame.time.Clock()


row = len(MAP1)
column = len(MAP1[0])

# Carrega o fundo do jogo
background = pygame.image.load(path.join(img_dir, 'Full Moon - background.png')).convert()
background_rect = background.get_rect()

# Carrega os sons do jogo
pygame.mixer.music.load(path.join(snd_dir, 'blackmist II.mp3'))
pygame.mixer.music.set_volume(0.3)
pew_sound = pygame.mixer.Sound(path.join(snd_dir, 'shot.ogg'))
game_over_sound = pygame.mixer.Sound(path.join(snd_dir, 'game_over_bad_chest.wav'))
arrow_sound = pygame.mixer.Sound(path.join(snd_dir, 'Archers-shooting.ogg'))
die_sound = pygame.mixer.Sound(path.join(snd_dir, 'Hurting The Robot.wav'))
grunt_sound = pygame.mixer.Sound(path.join(snd_dir, 'grunt.wav'))  
victory_sound = pygame.mixer.Sound(path.join(snd_dir, 'victory.ogg'))
ice_sound = pygame.mixer.Sound(path.join(snd_dir, 'ice_sound.ogg'))

# Sprites de block são aqueles que impedem o movimento do jogador
blocks = pygame.sprite.Group()

# Cria Jack. O construtor será chamado automaticamente.
player = Player(row, column, blocks)

# Cria um grupo de sprites e adiciona Jack.
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Cria tiles de acordo com o mapa
for row in range(len(MAP1)):
    for column in range(len(MAP1[row])):
        tile_type = MAP1[row][column]
        if tile_type == BLOCK:
            tile = Tile(row, column)
            all_sprites.add(tile)
            blocks.add(tile)
            
# Cria um grupo só de esqueletos
mob = pygame.sprite.Group()

#Cria um grupo so para magos 
mag = pygame.sprite.Group() 

# Cria i mobs e adiciona no grupo
for i in range(1):
    m = Mob(row, column, blocks, Arrow)
    all_sprites.add(m)
    mob.add(m)
    
# Cria x magos e adiciona o grupo 
for x in range(1):
    mg = Magician(row, column, blocks, Ice)
    all_sprites.add(mg)
    mag.add(mg)

# Cria um grupo para tiros
bullets = pygame.sprite.Group()

# Cria um grupo para flechas
arrows = pygame.sprite.Group()

#Cria um grupo so para icehits
ices = pygame.sprite.Group()     

# Comando para evitar travamentos.
def game_screen(screen):
    
    # Loop principal.
    
    vida = 100
    vida_mob = 10
    running = True
    pygame.mixer.music.play(loops=-1)
    while running:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        #Adiciona as flechas no mapa 
        for m in mob:
            if m.fire:  
                m.fire = False
                dx = player.rect.centerx - m.rect.left
                dy = player.rect.centery - m.rect.centery
                d = (dx**2 + dy**2)**(1/2)
                if dy < 0:
                    Sy = -10*dy/d
                Sx = 10*dx/d
                Sy = 10*dy/d

                arrow = Arrow(m.rect.left, m.rect.centery, Sx, Sy)
                all_sprites.add(arrow)
                arrows.add(arrow)
                arrow_sound.play()
                
        #Adiciona os ices
        for mg in mag:
            if mg.fire:
                mg.fire = False
                
                dx2 = player.rect.centerx - mg.rect.left
                dy2 = player.rect.centery - mg.rect.centery
                d2 = (dx2**2 + dy2**2)**(1/2)
                if dy2 < 0:
                    Sy2 = -10*dy2/d2
                Sx2 = 10*dx2/d2
                Sy2 = 10*dy2/d2                


                
                ice = Ice(mg.rect.right, mg.rect.centery, Sx2, Sy2)
                all_sprites.add(ice)
                ices.add(ice) 
                
                
                
                
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                running = False
                
            
            if player.state != ICED and player.state != ICED_LEFT:  
                # Verifica se pulou
                if event.type == pygame.KEYDOWN:       
                    if event.key == pygame.K_UP and player.state in POS:                    
                        player.jump()
                        player.state = JUMP
                    elif event.key == pygame.K_UP and player.state in NEG:                    
                        player.jump()
                        player.state = JUMP_LEFT
            
                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key == pygame.K_LEFT:
                        player.speedx = -5
                        player.state = LEFT
                    elif event.key == pygame.K_RIGHT:
                        player.speedx = 5
                        player.state = RIGHT
                    if event.key == pygame.K_UP and player.state in POS:                    
                        player.jump()
                        player.state = JUMP
                    elif event.key == pygame.K_UP and player.state in NEG:                    
                        player.jump()
                        player.state = JUMP_LEFT
                    # Se for um espaço atira!
                    if event.key == pygame.K_SPACE:
                        bullet = Bullet(player.rect.centerx, player.rect.top, blocks, mob)
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                        pew_sound.stop() 
                        pew_sound.play()                    
                
                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key == pygame.K_LEFT:
                        player.speedx = 0                    
                        player.state = IDLE_LEFT
                    elif event.key == pygame.K_RIGHT:
                        player.speedx = 0                    
                        player.state = IDLE
                    
        # Depois de processar os eventos.
        # Atualiza a acao de cada sprite.
        all_sprites.update()
        
        # Verifica se houve colisão entre tiro e meteoro
        hits = pygame.sprite.groupcollide(mob, bullets, False, True, pygame.sprite.collide_mask)
        for hit in hits: # Pode haver mais de um
            # O meteoro e destruido e precisa ser recriado
            die_sound.play()
            vida_mob -= 1
            if vida_mob == 0:
                m.state = DEAD
                print(m.frame)
        for m in mob:
            if m.morre == True:
                m.kill()
                
                
        hits = pygame.sprite.spritecollide(player, arrows, True, pygame.sprite.collide_mask)
        for hit in hits: # Pode haver mais de um
            # O meteoro e destruido e precisa ser recriado
            grunt_sound.play()
            vida -= 1
        hits = pygame.sprite.spritecollide(player, ices, True, pygame.sprite.collide_mask) 
        for hit in hits: #Pode haver mais de um 
            ice_sound.play()
            player.freeze()
            
        # Verifica se caiu da tela
        if player.rect.y > 700 or vida == 0:
            pygame.mixer.music.stop()
            game_over = pygame.image.load(path.join(img_dir, "Game-over-2.png")).convert()
            game_over_sound.play()    
            screen.fill(BLACK)
            screen.blit(game_over,[0,0])
            pygame.display.update()
            time.sleep(5)
            
            running = False
        
        elif len(mob) == 0 :
            pygame.mixer.music.stop()
            victory = pygame.image.load(path.join(img_dir, "victory.jpg")).convert()
            screen.fill(BLACK)
            screen.blit(victory,[0,0])
            pygame.display.update()
            victory_sound.play()    
            time.sleep(10)
            
            running = False
            
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
try:
    game_screen(screen)
        
finally:
    pygame.quit()
