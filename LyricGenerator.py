import os
import sys
import time
import pygame

music_file = ""

def modify_lyrics(content, file_suffix):
    modified_lyrics = []
    for line in content:
        modified_line = line.split('/d')[0].strip() + '\n'
        modified_lyrics.append(modified_line)
    with open(f'lyrics{file_suffix}.txt', 'w') as file:
        file.writelines(modified_lyrics)

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

def typeWithWPM(text, wpm):
    words = text.split(' ')
    for word in words:
        command_actions = {'/f': lambda w: wpm * 2,
                           '/s': lambda w: wpm / 1.5,
                           '/rs': lambda w: wpm / 2,
                           '/ns': lambda w: original_wpm,
                           '/i': lambda w: original_wpm * 9999999999}
        for command, action in command_actions.items():
            if command in word:
                wpm = action(wpm)
                word = word.replace(command, '')
                break
        delay = 60 / wpm
        for char in word:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        if word != words[-1]:
            sys.stdout.write(' ')
            sys.stdout.flush()
            time.sleep(delay) 

def main():
    if os.path.exists('lyrics.txt'):
        file_suffix = 2
        while os.path.exists(f'lyrics{file_suffix}.txt'):
            file_suffix += 1
    else:
        file_suffix = 1

    with open('./lyrics.txt', 'r') as file:
        lyrics = file.readlines()

    modify_lyrics(lyrics, file_suffix)

    print(f"Modified 'lyrics{file_suffix}.txt' created successfully!")

    with open(f'lyrics{file_suffix}.txt', 'r') as file:
        lyrics = file.read()

    pygame.init()
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()

    original_wpm = 800
    wpm = original_wpm

    delays = []

    for line in lyrics.split("\n"):
        if '/c' in line:
            os.system('cls' if os.name == 'nt' else 'clear')
        elif line.strip() and '/nl' not in line: 
            start_time = None  
            typeWithWPM(line, wpm)
            start_time = time.time()  
            input()
            end_time = time.time()  
            delay = end_time - start_time
            delays.append(delay)
            print(f"Time taken: {delay:.2f} seconds")
        elif line.strip():
            typeWithWPM(line, wpm)

    pygame.mixer.music.stop()

    reverse_modify_lyrics(lyrics.split("\n"), file_suffix, delays)

    print(f"Reversed 'reversed_lyrics{file_suffix}.txt' created successfully!")

if __name__ == "__main__":
    main()
