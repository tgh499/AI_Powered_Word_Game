# AUTHOR: @Toru

#########################################
# PLEASE USE PYTHON3 to run the program #
#########################################

# Once two words are given, this program creates a chain between the two words.
# Chain implies when there is only one letter difference between the current
# word and previous word
# For example: flea -> flee is a chain

# import packages
# if an error shows up, use "pip3 install <packageName>" to install the package
import heapq
import collections
import numpy as np
import random


# read from textfiles, that are essentially dictionaries
# input: length of the word; integer;
# output: list; combined list from multiple files containing only unique words,
#           and "\n" stripped
def readFiles(n):
    fileList_4 = ['./resources/four_lc.txt', './resources/four_alpha.txt', './resources/old_four.txt']
    fileList_3 = ['./resources/three_lc.txt','./resources/three_alpha.txt']
    fileList_5 = ['./resources/five_lc.txt', './resources/five_alpha.txt']

    if n == 3:
        fileList = fileList_3
    elif n == 5:
        fileList = fileList_5
    else:
        fileList = fileList_4


    wordList = []
    for i in fileList:
        with open(i) as f:
            lines = f.readlines()
            wordList.extend(x for x in lines if x not in wordList)

    for i,j in enumerate(wordList):
        wordList[i] = j.rstrip('\n')

    return(wordList)

# implement a Queue class
# Please refer to, https://www.redblobgames.com/pathfinding/a-star/
# implementation.html. I used the site as my reference.
class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()


# implement a SimpleGraph class
# Please refer to, https://www.redblobgames.com/pathfinding/a-star/
# implementation.html. I used the site as my reference.
class SimpleGraph:
    def __init__(self):
        self.edges = {}

    def neighbors(self, id):
        return self.edges[id]

# calculates distance between two words
# Only returns 1, if there is 1 letter difference
# Otherwise, returns 0
# input: two words of same length
# output: 1 or 0
def heuristic(a, b):
    truthTable = []
    for i in range(len(a)):
        temp = (a[i] == b[i])
        truthTable.append(temp)
    if (np.count_nonzero(truthTable) == (len(a) -1)):
        return 1
    else:
        return 0

# a breadth_first_search function
# Please refer to, https://www.redblobgames.com/pathfinding/a-star/
# implementation.html. I used the site as my reference.
# Performs breadth first search, and also returns the path between
# start word, and final word.
# input: a graph containing neibors that matches the heuristic described above
#        (the graph has the type of a python dictionary); start word; finalWord;
# output: path between startWord, and finalWord
def breadth_first_search(graph, start, goal):
    frontier = Queue()
    frontier.put(start)
    came_from = {}
    came_from[start] = None

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current

    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return(path)

# Creates a graph that containes a word as a key, and its neighbors as values;
# Matches the condition of the heuristic described above
# input: length of word; Here the length can only be 3 or 4 or 5
# output: a dictionary
def wordGraph(n):
    if n == 3:
        currentList = readFiles(3)
    elif n == 5:
        currentList = readFiles(5)
    else:
        currentList = readFiles(4)

    wordG = {}

    for i,j in enumerate(currentList):
        temp = []
        for k,l in enumerate(currentList):
            heurValue = heuristic(j,l)
            if heurValue != 0 :
                temp.append(l)
        wordG[j] = temp
    return(wordG)

# Given a word, creaes a list of words that that has length 1 less than the
# given word. The actual sequence of letters is maintained.
# All shrunk words exist in the given files for that length of words.
# input: a word
# output: a list of words with length 1 less than the given word
def generateShrunkWordLists(word):
    a = [i for i in range(len(word))]
    random.shuffle(a)
    newWords = []
    words = readFiles(len(word) -1)
    for i in a:
        temp = word
        temp = temp.replace(temp[i], "")
        if temp in words:
            newSourceWord = temp
            newWords.append(temp)

    return newWords

# Given a word, creates a list of words that has length 1 more than the
# given word. The sequence is maintained. Random letters are inserted in
# different positions. If they exist in the given files, they are added in a
# list. The list is returned.
# input: a word
# output: a list of words with length 1 more than the given word
def generateExpandedWordLists(word):
    a = [i for i in range(len(word) + 1)]
    alphabet = [chr(i) for i in range(ord('a'), ord('z')+1)]
    newWords = []
    Words = readFiles(len(word) + 1)

    for k in alphabet:
        for i in a:
            hashList = list(word)
            hashList.insert(i, k)
            temp = (''.join(hashList))
            if temp in Words:
                newWords.append(temp)
    return newWords


# Executes when a shrunk chain is sought from main
# Tries its best to find a chain from the startWord to finalWord.
# If no chain exists, it starts to find a chain to the immediate previous word
# in its four-word chain.
# input: startWord, finalWord, length of either of those words
# output: printing the path between startWord, finalWord
def shrink(sourceWord, destWord, n):
    newSourceWords = generateShrunkWordLists(sourceWord)

    newGraph4 = SimpleGraph()
    newGraph4.edges = wordGraph(len(sourceWord))
    fourPath = breadth_first_search(newGraph4, sourceWord, destWord)

    count = 1

    newGraph = SimpleGraph()
    newGraph.edges = wordGraph(n-1)

    currentDestWords = []
    middlePath = []
    if len(fourPath) == 0:
        print("")
    else:
        for i in range(len(fourPath)-1):
            destWord = fourPath[-count]
            count = count + 1
            currentDestWords.append(destWord)

            newDestWords = generateShrunkWordLists(destWord)

            for i in newSourceWords:
                for j in newDestWords:
                    middlePath = breadth_first_search(newGraph, i, j)
                    if middlePath != []:
                        break
                if middlePath != []:
                    break;
            if middlePath != []:
                break;

    startPath = [sourceWord]
    currentDestWords.reverse()
    if middlePath == []:
        print("No chain exists! \n")
        return None
    else:
        path = startPath + middlePath + currentDestWords

    print("\n The word-chain from " +str(sourceWord) +" to "+str(destWord) +":")
    printWordChain(path)
    print("Chain length is: " + str(len(path)-1) + "\n")


# Executes when a expanded chain is sought from main
# Tries its best to find a chain from the startWord to finalWord.
# If no chain exists, it starts to find a chain to the immediate previous word
# in its four-word chain.
# input: startWord, finalWord, length of either of those words
# output: printing the path between startWord, finalWord
def expand(sourceWord, destWord, n):
    newSourceWords = generateExpandedWordLists(sourceWord)

    newGraph4 = SimpleGraph()
    newGraph4.edges = wordGraph(len(sourceWord))
    fourPath = breadth_first_search(newGraph4, sourceWord, destWord)

    count = 1

    newGraph = SimpleGraph()
    newGraph.edges = wordGraph(n+1)

    currentDestWords = []
    middlePath = []
    if len(fourPath) == 0:
        print("")
    else:
        for i in range(len(fourPath)-1):
            destWord = fourPath[-count]
            count = count + 1
            currentDestWords.append(destWord)

            newDestWords = generateExpandedWordLists(destWord)

            for i in newSourceWords:
                for j in newDestWords:
                    middlePath = breadth_first_search(newGraph, i, j)
                    if middlePath != []:
                        break
                if middlePath != []:
                    break;
            if middlePath != []:
                break;

    startPath = [sourceWord]
    currentDestWords.reverse()
    if middlePath == []:
        print("No path exists! \n")
        return None
    else:
        path = startPath + middlePath + currentDestWords

    print("\n The word-chain from " +str(sourceWord) +" to "+str(destWord) +":")
    printWordChain(path)
    print("Chain length is: " + str(len(path)-1) + "\n")

# finds the path between sourceWord, finalWord, when no shrinking or expanding
# is chosen.
# input: startWord, finalWord
# output: printing the path between startWord, finalWord
def wordChainSameLength(sourceWord, destWord):
    newGraph = SimpleGraph()
    newGraph.edges = wordGraph(len(sourceWord))
    middlePath = []
    middlePath = breadth_first_search(newGraph, sourceWord, destWord)
    if middlePath == []:
        print("No path exists! \n")
        return None
    else:
        path = middlePath

    print("\n The word-chain from " +str(sourceWord) +" to "+str(destWord) +":")
    printWordChain(path)
    print("Chain length is: " + str(len(path)-1) + "\n")

# Prompts the user for inputs
# Calls the inputWords function repeatedly to make sure that inputs are of
# correct format.
# input: nothing. called from main.
# output: returns a word chain that matches the correct format, and exists
#    in the files provided
def prompt():
    wordsToBeChained = []
    prompt = 'y'
    while (prompt == 'y' or prompt == 'Y'):
        wordsToBeChained += inputWords()
        prompt = input("Do you want to insert another set of words?" +\
                            " Type 'y' for yes, any character otherwise.")

    print("\n")
    return wordsToBeChained

# Takes inputs from users, and make sure they are of correct format and esist
# in the files provided
# input: nothing. called from prompt()
# output: returns a pair of words; ['startWord', 'finalWord']
def inputWords():
    sourceWord = input("Enter the start word:")
    destWord = input("Enter the final word:")
    fourWordList = readFiles(4)
    temp = []
    if len(sourceWord)!=4 or len(destWord) != 4:
        print("Both start and goal words should be of length 4.\n")
    elif sourceWord == destWord:
        print("Start word and final word are same. Chain length is 0.")
    elif sourceWord not in fourWordList or destWord not in fourWordList:
        print("Sorry, those are not valid words to create wordchain.")
    else:
        temp.append(sourceWord)
        temp.append(destWord)

    return temp

# given a word list, prints the words in with an arrow in between
# input: a word list
# output: prints the words with arrow in between
def printWordChain(chain):
    text = ""
    for i in chain:
        if i != chain[-1]:
            text += (str(i) + "-> ")
        else:
            text += (str(i))
    print(text)

# the main function
# calls the functions as necessary to create the word chain
# asks the user to choose between shrink, expanding, and same-word-length
def main():
    option = input("Do you want a word chain of same word-length or do" +\
                " you want to shrink or expand?\nType 3 to " +\
                "shrink, type 5 to expand; default is 4 which creates " +\
                "a chain of 4 letters.\n")
    if option == '3':
        toBeChained = prompt()
        count = 0
        if len(toBeChained) == 0:
            print("No words to be chained.")
        elif len(toBeChained) == 2:
            startWord = toBeChained[0]
            finalWord = toBeChained[1]
            print("Files used: three_lc.txt,three_alpha.txt," +\
                            "\n\tfour_lc.txt, four_alpha.txt, old_four.txt")
            shrink(startWord, finalWord, len(startWord))
        else:
            for i in range(len(toBeChained)-2):
                startWord = toBeChained[count]
                finalWord = toBeChained[count+1]
                print("Files used: three_lc.txt,three_alpha.txt," +\
                                "\n\tfour_lc.txt, four_alpha.txt, old_four.txt")
                shrink(startWord, finalWord, len(startWord))
                count  = count + 2
    elif option == '5':
        toBeChained = prompt()
        count = 0
        if len(toBeChained) == 0:
            print("No words to be chained.")
        elif len(toBeChained) == 2:
            startWord = toBeChained[0]
            finalWord = toBeChained[1]
            print("Files used: five_lc.txt, five_alpha.txt" +\
                    "\n\tfour_lc.txt, four_alpha.txt, old_four.txt")
            expand(startWord, finalWord, len(startWord))

        else:
            for i in range(len(toBeChained)-2):
                startWord = toBeChained[count]
                finalWord = toBeChained[count+1]
                print("Files used: five_lc.txt, five_alpha.txt" +\
                        "\n\tfour_lc.txt, four_alpha.txt, old_four.txt")
                expand(startWord, finalWord, len(startWord))
                count  = count + 2
    else:
        toBeChained = prompt()
        count = 0
        if len(toBeChained) == 0:
            print("No words to be chained.")
        elif len(toBeChained) == 2:
            startWord = toBeChained[0]
            finalWord = toBeChained[1]
            print("Files used: four_lc.txt, four_alpha.txt, old_four.txt")
            wordChainSameLength(startWord, finalWord)
        else:
            for i in range(len(toBeChained)-2):
                startWord = toBeChained[count]
                finalWord = toBeChained[count+1]
                print("Files used: four_lc.txt, four_alpha.txt, old_four.txt")
                wordChainSameLength(startWord, finalWord)
                count  = count + 2
    print("Thanks for using the program!")

main()
