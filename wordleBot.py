import json

words = []
letters = {}

with open("words.json", 'r') as f:
    words = json.loads(f.read())

def calcLetters():

    for w in words['La']:
        for i in range(len(w)):
            c = w[i]
            if not c in letters:
                letters[c] = {
                    "appearances" : 0, "position" : [0, 0, 0, 0, 0]
                }
            letters[c]["appearances"] += 1
            letters[c]["position"][i] += 1

    with open("letterData.json", 'w') as f:
        f.write(json.dumps(letters, indent=4))

def find_best_word(wordlist):
    best_score = 0
    best_word = ""

    for w in wordlist:
        score = 0
        currentChars = []
        for i in range(len(w)):
            c = w[i]
            if not c in currentChars:
                score += letters[c]["appearances"] * 2
                currentChars.append(c)
            score += letters[c]["position"][i]
        
        if score > best_score:
            best_score = score
            best_word = w
    
    return best_word

def filter_words(wordlist, static, illegal, anywhere, anywhere_pos = []):
    filtered_list = []
    for w in wordlist:
        legal = True
        for i in range(len(w)):
            c = w[i]
            if not (static[i] == '-' or static[i] == c):
                legal = False
            if c in illegal:
                legal = False
            for j in range(len(anywhere)):
                p = anywhere[j]
                if c == p and i in anywhere_pos[j]:
                    legal = False
        for c in anywhere:
            if c not in w:
                legal = False
        if legal:
            filtered_list.append(w)
    
    return filtered_list

def guess_word(wordList, word = "n", doPrint = True):
    lastWord = find_best_word(wordList)
    tries = 1
    if doPrint:
        print(F"recommended word: {lastWord}")

    static = "-----"
    illegal = ""
    anywhere = ""
    anywhere_pos = []

    while True:
        res = ""
        if word == 'n':
            res = input("result? [-/+/=]   ")
        else:
            for i in range(len(lastWord)):
                c = lastWord[i]
                if word[i] == c:
                    res += '='
                elif c in word:
                    res += '+'
                else:
                    res += '-'
            

        if len(res) != 5:
            if doPrint:
                print("error: unexpected input")
            continue
            
        if res == "=====":
            if doPrint:
                print("cool!")
            return tries
        
        for i in range(5):
            c = lastWord[i]
            r = res[i]

            if r == '-':
                illegal += c
            elif r == '+':
                if c in anywhere:
                    anywhere_pos[anywhere.index(c)].append(i)
                else:
                    anywhere += c
                    anywhere_pos.append([i])
            elif r == '=':
                static = static[:i] + c + static[i+1:]
            else:
                print("error: unexpected input")
                continue
            
        score = 0
        
        for i in static:
            if not i == '-':
                score += 2
        score += len(anywhere)
        
        lastWord = find_best_word(filter_words(wordList, static, illegal, anywhere, anywhere_pos))

        if doPrint:
            print("================================")

        if doPrint:
            print(F"recommended word: {lastWord}")
        tries += 1

guess_word(words["La"], "n", True)
