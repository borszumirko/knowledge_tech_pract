import tkinter as tk

class Questions:
    def __init__(self, master):
        self.master = master
        self.master.title("Fishing Method Recommendation System")

        self.questions = [
            {"question": "At what kind of body of water are you fishing?", "choices": ["lake", "river", "pond", "sea", "ocean"]},
            {"question": "Do you see any plants at the shore?", "choices": ["reeds", "trees"]},
            {"question": "How deep is the water?", "choices": ["more than 5m", "less than 5m"]},
            {"question": "What is the weather like?", "choices": ["rainy", "sunny"]},
            # Add more questions as needed
        ]

        self.current_question_index = 0
        self.selected_choices = []

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
        self.listbox_frame.pack(side="left", padx=10)

        # Display List
        self.listbox = tk.Listbox(self.listbox_frame)
        self.listbox.pack()

    def display_question(self):
        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]

            # Display Question
            self.question_label = tk.Label(self.master, text=question_data["question"])
            self.question_label.pack(pady=10)

            # Display Choices
            self.choice_var = tk.StringVar(value=question_data["choices"][0])
            self.choices_menu = tk.OptionMenu(self.master, self.choice_var, *question_data["choices"])
            self.choices_menu.pack(pady=10)

            # Next Question button
            self.next_button = tk.Button(self.master, text="Next Question", command=self.next_question)
            self.next_button.pack(pady=10)
            self.next_button["state"] = tk.DISABLED

            # Enable the "Next Question" button when a choice is made
            self.choice_var.trace_add('write', lambda *args: self.next_button.config(state=tk.NORMAL))
        else:
            self.show_summary()

    def next_question(self):
        selected_choice = self.choice_var.get()
        self.selected_choices.append(selected_choice)
        self.listbox.insert(tk.END, selected_choice)

        # Move to the next question
        self.current_question_index += 1

        # Update the listbox in the separate frame
        self.listbox.delete(0, tk.END)
        for choice in self.selected_choices:
            self.listbox.insert(tk.END, choice)

        # Update the existing widgets with new content
        self.question_label.config(text="")
        self.choices_menu.destroy()
        self.next_button.destroy()

        # Display the next question
        self.display_question()

    def show_summary(self):
        # No more questions, display a summary or perform some other action
        summary_label = tk.Label(self.master, text="Questionnaire completed! Here are your choices:")
        summary_label.pack()

        # Update the listbox in the separate frame with the final choices
        self.listbox.delete(0, tk.END)
        for choice in self.selected_choices:
            self.listbox.insert(tk.END, choice)

    def get_selected_choices(self):
        return self.selected_choices


