#!/usr/bin/env python3
import os
import sys
import time
import pygame

# Function to remove '/d' and the next numbers and write modified content into a new file
def strip_delays(content):
    modified_lyrics = []
    for line in content:
        # Split the line at '/d' and keep only the part before it
        modified_line = line.split('/d')[0]
        modified_lyrics.append(modified_line.strip() + '\n')
    return modified_lyrics

def get_next_available_filename(base_name, extension):
    if not os.path.exists(f"{base_name}.{extension}"):
        return f"{base_name}.{extension}"
    
    suffix = 2
    while os.path.exists(f"{base_name}{suffix}.{extension}"):
        suffix += 1
    return f"{base_name}{suffix}.{extension}"

def type_with_wpm(text, wpm, original_wpm):
    words = text.split(' ')
    for i, word in enumerate(words):
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
            wpm = 1_000_000_000
            word = word.replace('/i', '')
        elif '/nl' in word:
            print()
            continue
            
        delay = 60 / wpm
        for char in word:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        
        if i < len(words) - 1:
            sys.stdout.write(' ')
            sys.stdout.flush()
            time.sleep(delay)
    sys.stdout.flush()

def main():
    lyrics_file = 'lyrics.txt'
    audio_file = 'wyg.mp3'

    if not os.path.exists(lyrics_file):
        print(f"Error: {lyrics_file} not found.")
        sys.exit(1)

    with open(lyrics_file, 'r', encoding='utf-8') as f:
        original_lines = f.readlines()

    stripped_lines = strip_delays(original_lines)
    temp_lyrics_file = get_next_available_filename('lyrics_temp', 'txt')
    
    with open(temp_lyrics_file, 'w', encoding='utf-8') as f:
        f.writelines(stripped_lines)

    print(f"Temporary file '{temp_lyrics_file}' created.")

    # Play background music
    pygame.init()
    if os.path.exists(audio_file) and os.path.getsize(audio_file) > 0:
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
    else:
        print("Note: Audio file missing or empty. Syncing without music.")

    original_wpm = 800
    wpm = original_wpm
    delays = []

    print("\nStarting sync process. Press ENTER after each line appears to record the delay.")
    
    for line in stripped_lines:
        line_content = line.strip()
        if '/c' in line_content:
            os.system('cls' if os.name == 'nt' else 'clear')
        elif line_content and '/nl' not in line_content:
            type_with_wpm(line_content, wpm, original_wpm)
            start_time = time.time()
            input() # Wait for user input to sync
            end_time = time.time()
            delay = end_time - start_time
            delays.append(delay)
            print(f"Recorded delay: {delay:.2f}s")
        elif line_content:
            type_with_wpm(line_content, wpm, original_wpm)

    pygame.mixer.music.stop()
    pygame.quit()

    # Create the final reversed lyrics file with recorded delays
    final_lyrics_file = get_next_available_filename('lyrics_synced', 'txt')
    delay_index = 0
    synced_lines = []
    
    for line in stripped_lines:
        stripped_line = line.strip()
        if stripped_line and not '/nl' in stripped_line and not stripped_line == '/c':
            if delay_index < len(delays):
                synced_lines.append(f"{stripped_line} /d{delays[delay_index]:.2f}\n")
                delay_index += 1
            else:
                synced_lines.append(f"{stripped_line} /d0.00\n")
        else:
            synced_lines.append(line)

    with open(final_lyrics_file, 'w', encoding='utf-8') as f:
        f.writelines(synced_lines)

    print(f"\nSynced lyrics saved to '{final_lyrics_file}'.")

if __name__ == "__main__":
    main()
