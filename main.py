from forwChain import forward_chaining, find_recommendations
from parseKB import read_xml_from_file, parse_knowledge_base
from gui import Questions
import tkinter as tk


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
    app = Questions(root)
    root.mainloop()

    # After the Tkinter main loop, you can access the selected choices
    selected_choices = app.get_selected_choices()

    # Read XML data
    xml_file_path = 'fishKB.xml'
    xml_data = read_xml_from_file(xml_file_path)

    # Parse XML
    knowledge_base = parse_knowledge_base(xml_data, selected_choices)

    print_KB(knowledge_base)
    forward_chaining(knowledge_base)
    find_recommendations(knowledge_base)
    print_KB(knowledge_base)



if __name__ == "__main__":
    main()



