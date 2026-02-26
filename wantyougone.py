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

class SyncTimer:
    def __init__(self):
        self.start_time = time.time()
        self.offset = 0

    def get_elapsed(self):
        # Use pygame music position if available for better sync with audio clock
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            # get_pos returns milliseconds
            return pygame.mixer.music.get_pos() / 1000.0
        return time.time() - self.start_time

    def sleep_until(self, target_time):
        """Sleeps until the target time, or returns immediately if already past."""
        while True:
            elapsed = self.get_elapsed()
            remaining = target_time - elapsed
            if remaining <= 0:
                break
            # Sleep in small increments to stay responsive
            time.sleep(min(remaining, 0.01))

def type_with_wpm(text, original_wpm, timer, state):
    """
    Types text with synchronization.
    state: a dict containing current 'target_time' and 'wpm'
    """
    words = text.split(" ")
    skip_next = False
    
    for i, word in enumerate(words):
        if skip_next:
            skip_next = False
            continue
            
        # Command processing
        if '/f' in word:
            state['wpm'] *= 2
            word = word.replace('/f', '')
        elif '/s' in word:
            state['wpm'] /= 1.5
            word = word.replace('/s', '')
        elif '/rs' in word:
            state['wpm'] /= 2
            word = word.replace('/rs', '')
        elif '/ns' in word:
            state['wpm'] = original_wpm
            word = word.replace('/ns', '')
        elif '/i' in word:
            state['wpm'] = 1_000_000_000
            word = word.replace('/i', '')
        elif '/nl' in word:
            sys.stdout.write('\n')
            sys.stdout.flush()
            continue
        elif word.startswith('/d'):
            try:
                delay_str = word.split("/d")[1]
                delay = float(delay_str) if delay_str else 0
                state['target_time'] += delay
                timer.sleep_until(state['target_time'])
            except (ValueError, IndexError):
                pass
            skip_next = True
            continue
        
        char_delay = 60 / state['wpm']
        
        for char in word:
            state['target_time'] += char_delay
            timer.sleep_until(state['target_time'])
            sys.stdout.write(char)
            sys.stdout.flush()
        
        # Add space between words
        if i < len(words) - 1:
            state['target_time'] += char_delay
            timer.sleep_until(state['target_time'])
            sys.stdout.write(' ')
            sys.stdout.flush()

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

    timer = SyncTimer()
    state = {'target_time': 0, 'wpm': DEFAULT_WPM}

    try:
        for line in lyrics.split("\n"):
            if '/c' in line:
                os.system('cls' if os.name == 'nt' else 'clear')
                # Optional: slight delay after clear to prevent flicker/lag issues
                state['target_time'] += 0.05 
            elif line.strip() and '/nl' not in line:
                type_with_wpm(line, DEFAULT_WPM, timer, state)
                sys.stdout.write('\n')
                sys.stdout.flush()
            elif line.strip():
                type_with_wpm(line, DEFAULT_WPM, timer, state)
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        pygame.mixer.music.stop()
        pygame.quit()

if __name__ == "__main__":
    main()
