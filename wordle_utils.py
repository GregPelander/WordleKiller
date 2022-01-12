def find_max_freq(freq_dict, excluded):
    max_count = 0
    max_letter = None
    for letter in freq_dict:
        if freq_dict[letter] > max_count and letter not in excluded:
            max_count = freq_dict[letter]
            max_letter = letter
    return max_letter
