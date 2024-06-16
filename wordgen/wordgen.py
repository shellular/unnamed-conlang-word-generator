import json
import os
import uuid
import random

#Opens the JSON file for langSettings and creates variables for it. Use multiple *args to allow you to import multiple files at once.
def convertJSFileToVariables(*args):
    
    for jsfile in args:
        with open(jsfile) as baseJSFile:
            jsInfo = json.load(baseJSFile)

            #For value in JSON file, make that into a global variable with it's value the same as the JSON file.
            for key, value in jsInfo.items():
                globals()[key] = value


def generatePotentialWords(amount):
    
        if all(options in globals() for options in ['minSyllables', 'maxSyllables', 'mustEndInVowel', 'allowDiphthongs']):
            
            wordList = []
            if all(letters in globals() for letters in ['vowels', 'consonants', 'diphthongs']):
                
                allLetters = vowels + consonants
                
                nonConsonants = vowels
                if allowDiphthongs:
                    nonConsonants += diphthongs
                    allLetters += diphthongs
                
                for i in range(amount):
                    
                    potentialNewCreatedWord = ""
                    syllablesToAppend = random.randint(minSyllables, maxSyllables)
                    previousSyllable = ""
                        
                    for syllables in range(syllablesToAppend):
                        syllable = ""
                        
                        #if syllable has a syllable before it
                        if previousSyllable != "":
                            if previousSyllable[-1] in consonants:
                                syllable += random.choice(nonConsonants)
                            else:
                                syllable += random.choice(consonants)
                                
                            if syllable[-1] in consonants:
                                syllable += random.choice(nonConsonants)
                                
                                #If a coin flip lands heads, and either it doesn't have to end in a vowel or it does but this syllable is before the end of the word, add a consonant to the syllable.
                                if random.randint(1,3) < 3 and (mustEndInVowel == False or (mustEndInVowel == True and syllablesToAppend > syllables)):
                                    syllable += random.choice(consonants)
                            
                            previousSyllable = syllable
                            
                        else:
                            syllable += random.choice(allLetters)
                            #if last letter of syllable is a consonant, add a vowel too
                            if syllable[-1] in consonants:
                                syllable += random.choice(nonConsonants)
                                
                                #If a coin flip lands heads, and either it doesn't have to end in a vowel or it does but this syllable is before the end of the word, add a consonant to the syllable.
                                if random.randint(1,3) < 3 and (mustEndInVowel == False or (mustEndInVowel == True and syllablesToAppend > syllables)):
                                    syllable += random.choice(consonants)
                                    
                            previousSyllable = syllable
                                
                        potentialNewCreatedWord += syllable
                        
                    wordList.append(potentialNewCreatedWord)
                    
                return(wordList)
            
            
            else:
                
                print("One or more letter categories are missing. Potential words were not generated")
                return("error")
                                
        else:
            
            print("One or more option settings are missing. Potential words were not generated.")
            return("error")
    
        



def createPotentialWordFile(word):       
    convertJSFileToVariables("options.json", "langSettings.json")
     
    setManualLength = False
    wordAmount = 0
    
    if "+" in word:
        setManualLength = True
        word = word.replace('+', "")
        
    if "=" in word:
        if 'minSyllables' and 'maxSyllables' in globals():
            global minSyllables
            global maxSyllables
            minSyllables = int(input("Minimum syllable count (number only): "))
            maxSyllables = int(input("Maximum syllable count (number only): "))
        word = word.replace('=', "")
    
    if setManualLength == False:
        if 'defaultWordsGenerated' in globals():
            wordAmount = defaultWordsGenerated
        else:
            print("wordAmount not in options--did you delete it? Automatically setting word count to 15.")
            wordAmount = 15
            
    else:
        hasInput = False
        while not hasInput:
            wordAmountInput = input("How many words do you want? Type only integers (numbers).")
            if wordAmountInput.isdigit():
                wordAmount = wordAmountInput
                hasInput = True
            else:
                print("That wasn't just numbers. Try again.")
        
    if isinstance(wordAmount, int):
            fileContents = generatePotentialWords(wordAmount)
    else:
        
        if wordAmount.isdigit():
            fileContents = generatePotentialWords(int(wordAmount))
        else:
            fileContents = "error"
    
    if fileContents == "error":
        print("Word generation returned an error. File has not been created.")
         
    else:
        isFileNameOpen = False
        #creates the basic potential file name as "[inputted word].txt"
        existingWordFilesOfName = 0
        def findPotentialWordName():
            global potentialFilePath
            global potentialWordName
            
            if existingWordFilesOfName == 0:
                potentialWordName = f"{word}.txt"
                potentialFilePath = f"generatedPotentialWords\\{potentialWordName}"
                
            else:
                potentialWordName = f"{word}-{existingWordFilesOfName}.txt" 
                potentialFilePath = f"generatedPotentialWords\\{potentialWordName}"

        while not isFileNameOpen:
            findPotentialWordName()
            
            if os.path.isfile(potentialFilePath):
                existingWordFilesOfName += 1
                theoreticalName = f"{word}-{existingWordFilesOfName}.txt"
                deleteOrReplace = input(f"File \"{potentialWordName}\" already exists. Delete and replace, or create as {theoreticalName}? Type \"delete\" or a variation thereof to delete, otherwise continue by pressing Enter to make a second file for the same word.\n")
                
                if deleteOrReplace in ["d", "D", "del", "delete", "Delete"]:
                    print(f"deleting {potentialWordName}...")
                    
                    tempName = str(uuid.uuid4())
                    os.remove(potentialFilePath)
                    isFileNameOpen = True
                    
                else:
                    print(f"Continuing creation as {theoreticalName}...")
            else:
                isFileNameOpen = True
        
        with open(potentialFilePath, 'w') as createdWordFile:
            createdWordFile.write(f"Potential words for \"{word}\":\n\n")
            wordCountWritten = 0
            
            for i in range(len(fileContents)):
                if i != (len(fileContents) - 1):
                    createdWordFile.write(f"{fileContents[wordCountWritten]}, ")
                else:
                    createdWordFile.write(f"{fileContents[wordCountWritten]}")
                wordCountWritten += 1
                    
            print(f"File created and written. File can be located in [parent folder]\\wordgen\\generatedPotentialWords\\{word}.txt")
                    
#Loop to let the user use the actual meat of the program.
while True:
    wordInput = input("What word would you like to generate possible words for? (To choose # of generated words manually, add \"+\" to your word, and to choose min/max syllables randomly, add \"=\" to your word.)\n")
    createPotentialWordFile(wordInput)
    goAgain = input("End program, or go again? Press Enter to go again.\n")
    if goAgain != "":
        break
    else:
        print("Going again!")