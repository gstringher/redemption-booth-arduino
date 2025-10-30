import pygame

# Initialize mixer
pygame.mixer.init()

# Load and play MP3
pygame.mixer.music.load("audio-domande/intro.wav")

pygame.mixer.music.play()

# Keep the program running until the music finishes
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)