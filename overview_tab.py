import tkinter as tk
import palette


def create_overview_win(root: tk.Tk):
    """Overview Tab"""
    global overview_frame
    overview_frame = tk.Frame(root,
                              height=900,
                              width=1400,
                              bg=palette.PRIMARY_COLOR_03)
    overview_frame.grid(row=0, column=1)
    overview_frame.pack_propagate(False)

    overview_label = tk.Label(
        overview_frame,
        text=
        "Real-time Face Mask Detection and Validation System",
        font=palette.FONT_HEADING,
        bg=overview_frame["background"],
        wraplength=900)
    overview_label.pack(padx=20, pady=20)

    overview_line = tk.Frame(overview_frame,
                             height=2,
                             width=900,
                             bg=palette.PRIMARY_COLOR_02)
    overview_line.pack()

    greeting = tk.Label(
        overview_frame,
        text=
        """Welcome! This application is a project conducted by FEU Institute of Technology students, in accordance with the requirements of the course: System Integration and Architecture 2. Please feel free to contact any team member if you need any guidance!""",
        font=palette.FONT_TIMES,
        bg=overview_frame["background"],
        justify="left",
        wraplength=900,
    )
    greeting.pack(pady=20)

    description_label = tk.Label(overview_frame,
                                 text="A Brief Description:",
                                 font=palette.FONT_TIMES,
                                 bg=overview_frame["background"],
                                 justify="left",
                                 anchor=tk.W,
                                 wraplength=900)
    description_label.pack(fill=tk.X, padx=254, pady=(20, 0))

    description = tk.Label(
        overview_frame,
        text=
        """This application captures media input, uses a custom YOLOv5 Object Detection Model to pick out relevant areas in the input (people's faces and regions-of-interest), and then draws inferences from the image's elements. The main object of scrutiny in this project is the facemasks worn by the subjects, as it evaluates whether or not subjects are wearing them, and if they are, if they are wearing them properly or improperly.""",
        font=palette.FONT_TIMES,
        bg=overview_frame["background"],
        justify="left",
        wraplength=900,
    )
    description.pack(pady=(0, 20))

    members = tk.Label(
        overview_frame,
        text="""Group Name: TBD
Members:
        Arroyo, Lorenze Dionell K.
        Bautista, Raineill Joshua
        Lee, Michael
        Rivera, Aldwin""",
        font=palette.FONT_SMALL,
        bg=overview_frame["background"],
        justify="left",
        anchor=tk.W,
    )
    members.pack(fill=tk.X, padx=50, pady=(50, 0))


# Usage
if __name__ == "__main__":
    print("Please run this module through the main.py module...\n")
else:
    print("Importing overview_tab.py...\n")
