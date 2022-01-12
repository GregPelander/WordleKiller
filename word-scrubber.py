outputfile = open('sample.txt', 'a')
with open('word-large.txt') as f:
    for line in f:
        word = line.strip()
        if len(word) == 5:
            outputfile.write(word + '\n')
            print(word)
outputfile.close()
