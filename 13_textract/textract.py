import os
import sys
import re
from collections import Counter

class texTract:

    def getHelp(self):
        print("Mot available yet.")

    def getFromString(self,input_text):
        if self.Format == 1:
            tokens = [re.sub(r"[^\w\s]","", t) for t in input_text.split(" ") if t != "\n"]
            tokens = [t for t in tokens if len(t) > 0]
            return tokens

    def getFromTxt(self,input_text):
        tokens = []
        with open(input_text, "r") as file:
            for f in file:
                for token in f.split(" "):
                    if "\n" not in token:
                        tokens.append(re.sub(r"[^\w\s]","", token))
        return tokens

    def getFiles(self):
        ind = 0
        print(f"\nThe following file(s) were found:\n")
        for f in os.listdir():
            if f.endswith(".txt"):
                ind+=1
                print(f"\t{[ind]} {f}")

    def getContext(self,text,word,howmany=5):
        i = howmany
        tokens = self.getFromTxt(text)
        indexes = [i for i,w in enumerate(tokens) if w.lower() == word.lower()]
        print(f"\nFound {len(indexes)} instances for the word {word}")
        choice  = input("\nDisplay the context tokens for the word {word} [y/n]?\n")
        if choice.lower() == "y":
            for header,context in enumerate(indexes):
                x = f"Entry {header+1} for the word {word}:"
                y = f"\n\t{' '.join(tokens[context-i:context+i])}"
                if len(y) < 3:
                    print(x,"\n\t(Not enough contextual words)")
                else:
                    print(x,y)

    def getSummary(self,text,word):
        tokens = self.getFromTxt(text)
        total = f"\nCorpus length: {len(tokens)}"
        token = [v for k,v in Counter(tokens).most_common() if k.lower() == word.lower()]
        perc = round(token[0] / len(tokens) * 100,2)
        perc = f"\nRatio: {perc}%"
        token = f"\nNumber of iterations for the word '{word}': {token[0]}"
        token_len = (int(len(token)/2))
        menu = str("\n" + "-" * token_len + " SUMMARY " + "-" * token_len + "\n")
        menu2 = str("\n\n" + "-" * token_len + "TOP WORDS" + "-" * token_len + "\n\n")
        print(menu,total,token,perc,menu2,"\nOther words of interest:\n")
        tokens = [t for t in tokens if len(t) > 4 and t.lower() != word.lower()]
        for k,v in Counter(tokens).most_common(10):
                  print(f"{k:<17} > {v:>5}")

    def getMenu(self):
        main_menu = "\n\t[1] Help\n\t[2] List local text files\n\t[3] Context\n\t[4] Summary\n\t[5] Quit\n\n"
        while True:
            print(self.getLogo())
            choice = int(input(main_menu))
            if choice == 1:
                self.getHelp()
            elif choice == 2:
                self.getFiles()
            elif choice == 3:
                input_text = input("\nPlease enter the name of your .txt file (must be in the same folder):\n")
                input_token = input("\nPlease enter a keyword:\n")
                try:
                    self.getContext(input_text,input_token)
                except:
                    print(f"\nSorry, there doesn't seem to be a file with the name {input_text}")
            elif choice ==4:
                input_text = input("\nPlease enter the name of your .txt file (must be in the same folder):\n")
                input_token = input("\nPlease enter a keyword:\n")
                try:
                    self.getSummary(input_text,input_token)
                except:
                    print(f"\nSorry, there doesn't seem to be a file with the name {input_text}\n")
            elif choice ==5:
                print("\nThe application will now quit, thank you.\n")
                break
            else:
                print("Wrong input")

    def getLogo(self):
        logo = ("""
               ____   ___  _     _   ____   _____   _____   ___   _____
              |_  _| |  _| \ \  / / |_  _| |  _  | |  _  | |  _| |_   _|
                | |  | |_   \ \/ /    | |  | |_| | | |_| | | |     | |
                | |  |  _|   |  |     | |  |    /  |  _  | | |     | |
                | |  | |_   / /\ \    | |  | |\ \  | | | | | |_    | |
                |_|  |___| /_/  \_\   |_|  |_| \_\ |_| |_| |___|   |_|

                """)
        return logo

if __name__ == "__main__":
    textract = texTract()
    textract.getMenu()
