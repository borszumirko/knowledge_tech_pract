import tkinter as tk
from forwChain import forward_chaining, find_recommendations
from parseKB import read_xml_from_file, parse_knowledge_base
from tkinter import PhotoImage



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

helvFont = ("Helvetica", 12)
helvFontBold = ("Helvetica", 12, "bold")

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
        self.setup()

    def setup(self):
        image_path = "images/waves2.png"
        waves_image = tk.PhotoImage(file=image_path)
        image_width = waves_image.width()
        image_height = waves_image.height()

        self.master.geometry(f"{image_width}x{image_height}")

        # Create a label with the image
        image_label = tk.Label(self.master, image=waves_image)
        image_label.place(relwidth=1, relheight=1)

        # Keep a reference to prevent garbage collection
        image_label.image = waves_image

        self.current_question_index = 0
        self.selected_choices = []
        self.images = []  # List to store images

        # GUI elements
        self.question_label = None
        self.choices_menu = None
        self.next_button = None
        self.listbox_frame = None
        self.listbox = None

        self.create_listbox_frame()
        self.display_question()
        self.display_reset_button()

    def display_reset_button(self):
            self.restart_button = tk.Button(self.master, text="Restart Quiz", font=helvFontBold,command=self.reset_quiz, bg="khaki", fg="black", bd=5)
            self.restart_button.place(x=1700, y=50)

    # Reset everything
    def reset_quiz(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.setup()

    def create_listbox_frame(self):
        # Create a frame to hold the listbox
        self.listbox_frame = tk.Frame(self.master)
        self.listbox_frame.place(x=0,y=0)

        # Display List
        self.listbox = tk.Listbox(self.listbox_frame, font=helvFontBold, bg="khaki", fg="black", bd=3)
        self.listbox.pack()


    def next_question(self):
        selected_choice = self.choice_var.get()
        self.selected_choices.append(selected_choice)
        self.listbox.insert(tk.END, '• ' + selected_choice)

        self.current_question_index += 1

        # Prepare gui for displaying next question
        self.question_label.config(text="")
        self.choices_menu.destroy()
        self.next_button.destroy()

        # New question
        self.display_question()

    def display_question(self):
        # Prevent next question from moving down
        if self.question_label:
            self.question_label.pack_forget()
        if self.choices_menu:
            self.choices_menu.pack_forget()
        if self.next_button:
            self.next_button.pack_forget()

        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]

            # Display Question
            self.question_label = tk.Label(self.master, text=question_data["question"], bg="khaki", font=helvFontBold, bd=3)
            self.question_label.pack(pady=10)

            # Display Choices
            self.choice_var = tk.StringVar(value="Choose an option")
            self.choices_menu = tk.OptionMenu(self.master, self.choice_var, *question_data["choices"])
            self.choices_menu.pack(pady=10)

            menu = self.choices_menu.nametowidget(self.choices_menu.menuname)
            menu.configure(font=helvFontBold, background="khaki") 

            # Format items in menu
            for item in menu.winfo_children():
                item.configure(font=helvFontBold, background="khaki")

            # Next Question button
            self.next_button = tk.Button(self.master, text="Next Question", font=helvFontBold,command=self.next_question, bg="gray", fg="gray", bd=5)
            self.next_button.pack(pady=10)
            self.next_button["state"] = tk.DISABLED

            # Enable the "Next Question" button when a choice is made
            self.choice_var.trace_add('write', lambda *args: self.update_button_color())
        else:
            self.show_summary()

    def update_button_color(self):
        # Change the button color green when a choice is made
        self.next_button["bg"] = "green"
        self.next_button["fg"] = "white"
        self.next_button["state"] = tk.NORMAL


    def show_summary(self):
        
        selected_choices = self.get_selected_choices()

        # Read XML data
        xml_file_path = 'fishKB.xml'
        xml_data = read_xml_from_file(xml_file_path)

        # Parse XML
        knowledge_base = parse_knowledge_base(xml_data, selected_choices)

        # Perform chaining
        forward_chaining(knowledge_base)
        find_recommendations(knowledge_base)

        self.display_recommendations(knowledge_base['recommendations'])

    def get_selected_choices(self):
        return self.selected_choices

    def get_filename(self, rec):
        if (rec == "sweet boilie" or rec == "stinky boilie"):
            return "images/boilie.png"
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

        # Create a text to display recommendations
        recommendations_text = tk.Text(self.master, height=5, width=50, font=helvFont, bg="khaki", bd=3)
        recommendations_text.pack(pady=10)

        # Insert recommendations into the text
        recs = ""
        for recommendation in recommendations:
            for i, r in enumerate(recommendation):
                if (i%2 == 0):
                    recs += r + " - "
                else:
                    recs += r + '\n'

        recommendations_text.insert("1.0",recs)
        
        # Adjust the width and height of the text based on the content
        width = max(len(line) for line in recs.split('\n')) + 2
        height = recs.count('\n') + 1

        recommendations_text.config(width=width, height=height)
        recommendations_text.config(state=tk.DISABLED)

        col = 50
        row = 270
        # Display images with text underneath them
        for recommendation in recommendations:
            for r in recommendation:
                image = PhotoImage(file=self.get_filename(r))
                self.images.append(image)
                label = tk.Label(self.master, image=image,
                                compound=tk.TOP, text=r,
                                font=helvFont, bg="khaki", bd=3)
                label.place(x=col, y=row)
                if len(self.images) % 2 == 0:
                    col += image.width() + 50
                else:
                    col += image.width()
                if len(self.images)%8 == 0:
                    row += 270
                    col = 50





