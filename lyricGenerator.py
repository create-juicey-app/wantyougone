import os
import sys
import time
import pygame

music_file = "wyg.mp3"

def modify_lyrics(content, file_suffix):
    modified_lyrics = []
    for line in content:
        modified_line = line.split('/d')[0]
        modified_lyrics.append(modified_line.strip() + '\n')
    with open(f'lyrics{file_suffix}.txt', 'w') as file:
        file.writelines(modified_lyrics)

if os.path.exists('lyrics.txt'):
    file_suffix = 2
    while os.path.exists(f'lyrics{file_suffix}.txt'):
        file_suffix += 1
else:
    file_suffix = 1

with open('./lyrics.txt', 'r') as file:
    lyrics = file.readlines()

modify_lyrics(lyrics, file_suffix)

print(f"Modified file 'lyrics{file_suffix}.txt' created successfully!")

with open(f'lyrics{file_suffix}.txt', 'r') as file:
    lyrics = file.read()

pygame.init()
pygame.mixer.music.load(music_file)
pygame.mixer.music.play()

original_wpm = 800
wpm = original_wpm

delays = []

def type_with_wpm(text, wpm):
    words = text.split(' ')
    for word in words:
        if '/f' in word:
            wpm *= 2
            word = word.replace('/f', '')
        elif '/s' in word:
            wpm /= 1.5
            word = word.replace('/s', '')
        elif '/rs' in word:
            wpm /= 2
            word = word.replace('/rs', '')
        elif '/ns' in word:
            wpm = original_wpm
            word = word.replace('/ns', '')
        elif '/i' in word:
            wpm *= 9999999999
            word = word.replace('/i', '')
        elif '/nl' in word:
            print()
            continue
        delay = 60 / wpm
        for char in word:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        if word != words[-1]:
            sys.stdout.write(' ')
            sys.stdout.flush()
            time.sleep(delay)
    sys.stdout.flush()

for line in lyrics.split("\n"):
    if '/c' in line:
        os.system('cls' if os.name == 'nt' else 'clear')
    elif line.strip() and '/nl' not in line:
        start_time = None
        type_with_wpm(line, wpm)
        start_time = time.time()
        input()
        end_time = time.time()
        delay = end_time - start_time
        delays.append(delay)
        print(f"Time taken: {delay:.2f} seconds")
    elif line.strip():
        type_with_wpm(line, wpm)

pygame.mixer.music.stop()

def reverse_modify_lyrics(content, file_suffix, delays):
    reversed_lyrics = []
    delay_index = 0
    for line in content:
        stripped_line = line.strip()
        if stripped_line and not stripped_line.endswith('/nl') and not stripped_line == '/c':
            if delay_index < len(delays):
                line = stripped_line + f' /d{delays[delay_index]:.2f}\n'
                delay_index += 1
            else:
                line = stripped_line + ' /d0.00\n'
        reversed_lyrics.append(line)
    with open(f'reversed_lyrics{file_suffix}.txt', 'w') as file:
        file.writelines(reversed_lyrics)

with open(f'lyrics{file_suffix}.txt', 'r') as file:
    lyrics = file.readlines()

reverse_modify_lyrics(lyrics, file_suffix, delays)

print(f"Reversed file 'reversed_lyrics{file_suffix}.txt' created successfully!")
