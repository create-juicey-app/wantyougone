#!/usr/bin/env python3
import os
import sys
import time
import pygame

# Hide pygame support prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

DEFAULT_WPM = 800
LYRICS_FILE = 'lyrics.txt'
AUDIO_FILE = 'wyg.mp3'

def type_with_wpm(text, original_wpm, state):
    """
    Types text with synchronization.
    state: a dict containing current 'wpm'
    """
    words = text.split(" ")
    
    for i, word in enumerate(words):
        # Handle /d (delay) command - usually a standalone word
        if '/d' in word:
            try:
                # Find the part that starts with /d
                parts = word.split("/d")
                # We assume /d is at the end or standalone for timing
                delay_str = ""
                for char in parts[1]:
                    if char.isdigit() or char == '.':
                        delay_str += char
                    else:
                        break
                delay = float(delay_str) if delay_str else 0
                time.sleep(delay)
                # Remove the command from the word for printing
                word = parts[0] + parts[1][len(delay_str):]
            except (ValueError, IndexError):
                pass
            if not word: continue

        # Handle formatting/speed commands
        # Check longer commands first (e.g., /rs before /s)
        commands = [
            ('/rs', lambda: state.__setitem__('wpm', state['wpm'] / 2)),
            ('/ns', lambda: state.__setitem__('wpm', original_wpm)),
            ('/f',  lambda: state.__setitem__('wpm', state['wpm'] * 2)),
            ('/s',  lambda: state.__setitem__('wpm', state['wpm'] / 1.5)),
            ('/i',  lambda: state.__setitem__('wpm', 1_000_000_000)),
            ('/nl', lambda: sys.stdout.write('\n')),
            ('/c',  lambda: os.system('cls' if os.name == 'nt' else 'clear')),
        ]

        changed = True
        while changed:
            changed = False
            for cmd, action in commands:
                if cmd in word:
                    action()
                    word = word.replace(cmd, '', 1)
                    changed = True
                    break
        
        if not word:
            if i < len(words) - 1:
                # If it was a command-only word, we still might need to handle trailing spaces
                # but usually command-only words don't trigger the space delay.
                pass
            continue

        char_delay = 60 / state['wpm']
        
        for char in word:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(char_delay)
        
        # Add space between words if the next word is not a command
        if i < len(words) - 1:
            next_word = words[i+1]
            # If the current word wasn't just a command and next isn't just a command
            if not (next_word.startswith('/d') or next_word == '/nl' or next_word == '/c'):
                sys.stdout.write(' ')
                sys.stdout.flush()
                time.sleep(char_delay)



def main():
    if not os.path.exists(LYRICS_FILE):
        print(f"Error: {LYRICS_FILE} not found.")
        sys.exit(1)

    with open(LYRICS_FILE, 'r', encoding='utf-8') as f:
        lyrics = f.read()

    pygame.init()
    audio_exists = os.path.exists(AUDIO_FILE) and os.path.getsize(AUDIO_FILE) > 0
    
    if audio_exists:
        try:
            pygame.mixer.music.load(AUDIO_FILE)
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"Warning: Could not play audio. {e}")
    else:
        print("Note: Audio file missing or empty. Playing without music.")

    state = {'wpm': DEFAULT_WPM}
    
    try:
        for line in lyrics.split("\n"):
            state['wpm'] = DEFAULT_WPM # Reset WPM for each line
            if '/c' in line:
                os.system('cls' if os.name == 'nt' else 'clear')
            elif line.strip() and '/nl' not in line:
                type_with_wpm(line, DEFAULT_WPM, state)
                sys.stdout.write('\n')
                sys.stdout.flush()
            elif line.strip():
                type_with_wpm(line, DEFAULT_WPM, state)
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        pygame.mixer.music.stop()
        pygame.quit()

if __name__ == "__main__":
    main()
