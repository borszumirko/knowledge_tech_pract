import tkinter as tk
from forwChain import forward_chaining, find_recommendations
from parseKB import read_xml_from_file, parse_knowledge_base
from tkinter import PhotoImage
from PIL import Image, ImageTk



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



class Questions:
    def __init__(self, master):
        self.master = master
        self.master.title("Fishing Method Recommendation System")

        self.questions = [
            {"question": "Are you fishing at running water or standing water?", "choices": ["running water", "standing water"]},
            {"question": "Is the water temperature below or above 10C", "choices": ["below 10C", "above 10C"]},
            {"question": "How did the temperature change in the previous days?", "choices": ["getting warmer", "getting colder", "did not change"]},
            {"question": "Are you trying to fish during day or nighttime", "choices": ["day", "night"]},
        ]

        self.current_question_index = 0
        self.selected_choices = []

        self.images = []  # List to store PhotoImage instances


        # GUI elements
        self.question_label = None
        self.choices_menu = None
        self.next_button = None
        self.listbox_frame = None
        self.listbox = None

        self.create_listbox_frame()
        self.display_question()

    def create_listbox_frame(self):
        # Create a frame to hold the listbox
        self.listbox_frame = tk.Frame(self.master)
        #self.listbox_frame.pack(side="left", padx=10)
        self.listbox_frame.place(x=0,y=0)

        # Display List
        self.listbox = tk.Listbox(self.listbox_frame, font=("Helvetica", 12, "bold"), bg="khaki", fg="black", bd=3)
        self.listbox.pack()


    def next_question(self):
        selected_choice = self.choice_var.get()
        self.selected_choices.append(selected_choice)
        self.listbox.insert(tk.END, '• ' + selected_choice)

        # Move to the next question
        self.current_question_index += 1

        # Update the existing widgets with new content
        self.question_label.config(text="")
        self.choices_menu.destroy()
        self.next_button.destroy()

        # Display the next question
        self.display_question()





    def display_question(self):
        # prevent next question from moving down
        if self.question_label:
            self.question_label.pack_forget()
        if self.choices_menu:
            self.choices_menu.pack_forget()
        if self.next_button:
            self.next_button.pack_forget()


        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]

            # Display Question
            self.question_label = tk.Label(self.master, text=question_data["question"], bg="khaki", font=("Helvetica", 12, "bold"), bd=3)
            self.question_label.pack(pady=10)

            # Display Choices
            self.choice_var = tk.StringVar(value="Choose an option")
            self.choices_menu = tk.OptionMenu(self.master, self.choice_var, *question_data["choices"])
            self.choices_menu.pack(pady=10)

            menu = self.choices_menu.nametowidget(self.choices_menu.menuname)
            menu.configure(font=("Helvetica", 12, "bold"), background="khaki") 

            # Configure individual items in the menu
            for item in menu.winfo_children():
                item.configure(font=("Helvetica", 12, "bold"), background="khaki")

            # Next Question button
            self.next_button = tk.Button(self.master, text="Next Question", font=("Helvetica", 12, "bold"),command=self.next_question, bg="gray", fg="gray", bd=5)
            self.next_button.pack(pady=10)
            self.next_button["state"] = tk.DISABLED

            # Enable the "Next Question" button when a choice is made
            self.choice_var.trace_add('write', lambda *args: self.update_button_color())
        else:
            self.show_summary()





    def update_button_color(self):
        # Change the button color when a choice is made
        self.next_button["bg"] = "green"
        self.next_button["fg"] = "white"
        self.next_button["state"] = tk.NORMAL


    def show_summary(self):
        
        # Update the listbox in the separate frame with the final choices
        #self.listbox.delete(0, tk.END)
        #for choice in self.selected_choices:
        #    self.listbox.insert(tk.END, choice)

        selected_choices = self.get_selected_choices()

        # Read XML data
        xml_file_path = 'fishKB.xml'
        xml_data = read_xml_from_file(xml_file_path)

        # Parse XML
        knowledge_base = parse_knowledge_base(xml_data, selected_choices)

        #print_KB(knowledge_base)
        forward_chaining(knowledge_base)
        find_recommendations(knowledge_base)

        self.display_recommendations(knowledge_base['recommendations'])

    def get_selected_choices(self):
        return self.selected_choices

    def get_filename(self, rec):
        if (rec == "sweet boilie" or rec == "stinky boilie"):
            return "boilie.png"
        else:
            return "images/" + rec + ".png"


    def display_recommendations(self, recommendations):
        # Clear existing widgets
        if self.question_label:
            self.question_label.pack_forget()
        if self.choices_menu:
            self.choices_menu.pack_forget()
        if self.next_button:
            self.next_button.pack_forget()

        # Display recommendations
        recommendations_label = tk.Label(self.master, text="Here are your recommended fishing tecniques and baits:", font=("Helvetica", 18, "bold"), bg="khaki", bd=3)
        recommendations_label.pack(pady=10)

        # Create a text widget to display recommendations
        recommendations_text = tk.Text(self.master, height=5, width=50, font=("Helvetica", 12), bg="khaki", bd=3)
        recommendations_text.pack(pady=10)

        # Insert recommendations into the text widget
        recs = ""
        for recommendation in recommendations:
            for i, r in enumerate(recommendation):
                if (i%2 == 0):
                    recs += r + " - "
                else:
                    recs += r + '\n'

        recommendations_text.insert("1.0",recs)
        
        # Adjust the width and height of the text widget based on the content
        width = max(len(line) for line in recs.split('\n')) + 2
        height = recs.count('\n') + 1  # Number of lines

        recommendations_text.config(width=width, height=height)
        recommendations_text.config(state=tk.DISABLED)

        col = 50
        row = 270
        for recommendation in recommendations:
            for r in recommendation:
                image = PhotoImage(file=self.get_filename(r))
                self.images.append(image)
                label = tk.Label(self.master, image=image,
                                compound=tk.TOP, text=r,
                                font=("Helvetica", 12), bg="khaki", bd=3)

                
                label.place(x=col, y=row)
                if len(self.images) % 2 == 0:
                    col += image.width() + 50
                else:
                    col += image.width()
                if len(self.images)%8 == 0:
                    row += 270
                    col = 50





