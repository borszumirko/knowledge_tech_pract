from forwChain import forward_chaining, find_recommendations
from parseKB import read_xml_from_file, parse_knowledge_base
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

    
    #canvas = tk.Canvas(root, bg="lightblue")
    #canvas.pack(fill=tk.BOTH, expand=True)
    image_path = "waves.png"  # Replace with the actual path to your image file
    custom_image = tk.PhotoImage(file=image_path)
    image_width = custom_image.width()
    image_height = custom_image.height()

    # Set the size of the Tkinter window to match the image dimensions
    root.geometry(f"{image_width}x{image_height}")


    # Create a label with the image
    image_label = tk.Label(root, image=custom_image)
    image_label.place(relwidth=1, relheight=1)
    questions = Questions(root)
    root.mainloop()





if __name__ == "__main__":
    main()



