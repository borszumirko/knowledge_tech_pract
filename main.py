from gui import Questions
import tkinter as tk
from tkinter import font



def prtDict(dict):
    print('---')
    for rule in dict:
        for key, value in rule.items():
            print(f"{key}: {value}")
        print('---')

def print_KB(knowledge_base):
    print('Rules:')
    prtDict(knowledge_base['rules'])
    print('Recommendation rules:')
    prtDict(knowledge_base['recRules'])
    print('Facts:')
    print(knowledge_base['facts'])
    print('---')
    print('Recommendations:')
    print(knowledge_base['recommendations'])



def main():
    root = tk.Tk()
    questions = Questions(root)
    root.mainloop()





if __name__ == "__main__":
    main()



