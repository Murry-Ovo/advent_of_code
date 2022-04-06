import re
from collections import Counter
from string import ascii_lowercase


def parse_input_row(input_row: str) -> tuple:
    """
    - Takes one line from the input and splits it into a tuple of:
        - 'encrypted_letters': A list of all letters in the input string up to the first numerical digit
        - 'sector_id': The numerical value within the input string 
        - 'checksum': The checksum value (the letters within the square brackets)
    """
    name_and_sector, checksum = input_row[:-1].split('[')
    sector_id = int(re.findall('(\d+)', name_and_sector)[0])
    encrypted_letters = re.findall("([a-z])", name_and_sector)
    encrypted_name_with_dash = re.split("(\d+)", name_and_sector)[0][:-1]

    return encrypted_letters, sector_id, checksum, encrypted_name_with_dash


def check_the_checksum(encrypted_letters: list, checksum: str) -> bool:
    """
    - Orders the encrypted_letters alphabetically
    - Makes a counter dictionary of the 5 most common letters
    - Converts the keys to a string to create a 'calculated_checksum'
    - Checks against the input_checksum to see if they match
    """
    encrypted_letters.sort()
    counter_dict = dict(Counter(encrypted_letters).most_common(5))
    calculated_checksum = ''.join([k for k in counter_dict])

    return calculated_checksum == checksum


def sum_valid_sector_ids(puzzle_input: list) -> 'print statement':
    """
    - Iterates through the list of rooms (puzzle input)
    - Checks to see if the checksum matches the calculated checksums
    - Adds to a 'sector_id_sum' if the room is a valid room
    - Prints out the final 'sector_id_sum'
    """
    sector_id_sum = 0
    valid_encryrptions_ = []
    for line in puzzle_input:
        encrypted_letters, sector_id, checksum, encrypted_name_with_dash = parse_input_row(line)
        if check_the_checksum(encrypted_letters, checksum):
            sector_id_sum += sector_id
            valid_encryrptions_.append((encrypted_name_with_dash, sector_id))

    print(f"The sum of the sector_id's from valid rooms is {sector_id_sum}")

    return valid_encryrptions_


def decode_message(input_tuple: tuple) -> 'decoded message':
    """
    - Takes an input tuple (encrypted_name, sector_id) and outputs the decoded message
    - Calculating the number of letters to shift through the alphabet by getting the modulus of the Secotor_ID and 26
    - Adds the new letter to a new 'decoded_string'
    - Returns the decoded string and the sector id 
    """
    alphabet = ascii_lowercase * 2
    encrrypted_message, sector_id = input_tuple
    shift = sector_id % 26
    decoded_string = ''
    for letter in encrrypted_message:
        if letter == '-':
            decoded_string += ' '
        else:
            letter_pos = alphabet.index(letter)
            decoded_string += alphabet[letter_pos + shift]

    return decoded_string, input_tuple[1]


day = '04'
with open(f"inputs/day_{day}.txt", 'r') as f: puz_input = [line.rstrip('\n') for line in f.readlines()]
with open(f'Inputs\\day_{day}_sample.txt') as f: sample_input = [line.rstrip('\n') for line in f.readlines()]

puz_input = puz_input
# puz_input = sample_input    

print("Part One:")
valid_encryrptions = sum_valid_sector_ids(puz_input)

print("\nPart Two:")
decoded_messages = [decode_message(x) for x in valid_encryrptions]
for message in decoded_messages:
    if re.match("northpole|north pole", message[0]) != None: print(f"North Pole objects are stored in {message}")
