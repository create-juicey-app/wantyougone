import os
import sys
import time
import pygame

# Function to remove '/d' and the next numbers and write modified content into a new file
def modify_lyrics(content, file_suffix):
    modified_lyrics = []
    for line in content:
        modified_line = line.split('/d')[0]  # Split the line at '/d' and keep only the part before it
        modified_lyrics.append(modified_line.strip() + '\n')  # Add the modified line to the list, stripping any extra whitespace
    with open(f'lyrics{file_suffix}.txt', 'w') as file:
        file.writelines(modified_lyrics)

# Check if 'lyrics.txt' already exists
if os.path.exists('lyrics.txt'):
    file_suffix = 2
    while os.path.exists(f'lyrics{file_suffix}.txt'):
        file_suffix += 1
else:
    file_suffix = 1

# Read the content of "lyrics.txt"
with open('./lyrics.txt', 'r') as file:
    lyrics = file.readlines()

# Modify the lyrics and create a new 'lyrics.txt' file
modify_lyrics(lyrics, file_suffix)

print(f"Modified file 'lyrics{file_suffix}.txt' created successfully!")

# Load lyrics from the newly created file
with open(f'lyrics{file_suffix}.txt', 'r') as file:
    lyrics = file.read()

# Play background music
pygame.init()
pygame.mixer.music.load("wyg.mp3")
pygame.mixer.music.play()

original_wpm = 800  # Adjust the default typing speed as needed
wpm = original_wpm

delays = []  # List to store delays

# Function to type with specified words per minute (WPM)
def typeWithWPM(text, wpm):
    words = text.split(' ')  # Split the text using space as delimiter
    for word in words:
        # Check for special commands within the word
        if '/f' in word:
            wpm *= 2  # Double the WPM speed
            word = word.replace('/f', '')  # Remove the '/f'
        elif '/s' in word:
            wpm /= 1.5  # Half the WPM speed
            word = word.replace('/s', '')  # Remove the '/s'
        elif '/rs' in word:
            wpm /= 2  # Half the WPM speed
            word = word.replace('/rs', '')  # Remove the '/s'
        elif '/ns' in word:
            wpm = original_wpm  # Restore the original WPM speed
            word = word.replace('/ns', '')  # Remove the '/ns'
        elif '/i' in word:
            wpm *= 9999999999  # Restore the original WPM speed
            word = word.replace('/i', '')  # Remove the '/ns'
        elif '/nl' in word:
            print()  # Move to the next line
            continue  # Skip to the next iteration
            
        # Calculate the delay based on the WPM
        delay = 60 / wpm
        
        # Simulate typing each word
        for char in word:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        
        # Add space between words except for the last word
        if word != words[-1]:
            sys.stdout.write(' ')
            sys.stdout.flush()
            time.sleep(delay)  # Pause briefly after each word
    sys.stdout.flush()

for line in lyrics.split("\n"):
    if '/c' in line:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
    elif line.strip() and '/nl' not in line:  # Check if the line is not empty and doesn't contain /nl
        start_time = None  # Initialize start time
        typeWithWPM(line, wpm)
        start_time = time.time()  # Start the timer after the phrase has been fully displayed
        input()  # Wait for user to press Enter without displaying any prompt or newline
        end_time = time.time()  # Record end time
        delay = end_time - start_time
        delays.append(delay)  # Store the delay
        print(f"Time taken: {delay:.2f} seconds")
    elif line.strip():  # Check if the line is not empty (with /nl)
        typeWithWPM(line, wpm)

pygame.mixer.music.stop()


# Function to add '/d[number]' to the end of each line that doesn't contain '/nl'
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
                line = stripped_line + ' /d0.00\n'  # default delay if no more delays in the list
        reversed_lyrics.append(line)
    with open(f'reversed_lyrics{file_suffix}.txt', 'w') as file:
        file.writelines(reversed_lyrics)

# Load lyrics from the modified file
with open(f'lyrics{file_suffix}.txt', 'r') as file:
    lyrics = file.readlines()

# Reverse modify the lyrics and create a new 'reversed_lyrics.txt' file
reverse_modify_lyrics(lyrics, file_suffix, delays)

print(f"Reversed file 'reversed_lyrics{file_suffix}.txt' created successfully!")