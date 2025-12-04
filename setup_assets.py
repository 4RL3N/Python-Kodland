import os
import pygame
import wave
import math
import struct

# Inicializa pygame (necessário para salvar imagens)
pygame.init()

# Define nomes e cores para os Placeholders
assets_img = {
    "p1_idle": (0, 255, 0),      # Verde
    "p1_idle2": (0, 200, 0),     # Verde Escuro
    "p1_walk1": (50, 255, 50),   
    "p1_walk2": (100, 255, 100), 
    "p1_walk3": (50, 255, 50),
    "enemy_idle1": (255, 0, 0),  # Vermelho
    "enemy_idle2": (200, 0, 0),
    "enemy_walk1": (255, 50, 50),
    "enemy_walk2": (255, 100, 100),
    "boss_idle1" : (0, 0, 255),     # Azul
    "boss_idle2" : (0, 0, 250),
    "boss_idle3" : (0, 0, 250),
    "boss_walk1" : (50, 50, 255),
    "boss_walk2" : (100, 100, 255)
}

# Cria pastas
if not os.path.exists("images"):
    os.makedirs("images")
if not os.path.exists("sounds"):
    os.makedirs("sounds")

# --- Gerar Imagens ---
print("Gerando imagens...")
for name, color in assets_img.items():
    # Cria uma superfície (quadrado 40x40)
    surf = pygame.Surface((40, 60) if "p1" in name else (40, 40))
    surf.fill(color)
    
    # Desenha um "olho" para sabermos a direção
    pygame.draw.rect(surf, (255, 255, 255), (25, 5, 10, 10))
    
    # Salva na pasta images
    pygame.image.save(surf, f"images/{name}.png")

# --- Gerar Sons (WAV simples) ---
print("Gerando sons...")

def create_beep(filename, frequency=440, duration=0.2):
    sample_rate = 44100
    n_frames = int(sample_rate * duration)
    data = []
    for x in range(n_frames):
        value = int(32767.0 * 0.5 * math.sin(2.0 * math.pi * frequency * x / sample_rate))
        data.append(struct.pack('<h', value))
    
    with wave.open(f"sounds/{filename}.wav", 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(b''.join(data))

# Gera sons básicos
create_beep("jump", 400, 0.1)
create_beep("lose", 150, 0.5)

# Nota: O PgZero toca .mp3 ou .wav, mas gerar mp3 via código puro é complexo.
# Vamos criar um wav e pedir para você renomear a chamada no código se precisar, 
# mas o código original aceita carregar "bg_music" sem extensão se o arquivo estiver lá.
# Para musica, vamos fazer um beep longo e grave repetitivo.
create_beep("bg_music", 100, 3.0) 

print("Concluído! Agora rode o 'main.py'.")