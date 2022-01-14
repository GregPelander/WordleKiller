def find_max_freq(freq_dict, excluded):
    max_count = 0
    max_letter = None
    for letter in freq_dict:
        if freq_dict[letter] > max_count and letter not in excluded:
            max_count = freq_dict[letter]
            max_letter = letter
    return max_letter


def find_best_divisor(freq_dict, excluded, total_count):
    target = total_count / 2
    min_diff = None
    best_letter = None
    for letter in freq_dict:
        if letter not in excluded:
            diff = abs(target - freq_dict[letter])
            if min_diff is None or min_diff > diff:
                min_diff = diff
                best_letter = letter
    return best_letter


all_words = []


# get initial word list in singleton pattern
def get_all_words():
    if len(all_words) == 0:
        f = open('word-list.txt')
        for line in f:
            all_words.append(line.strip())
        f.close()
    return all_words