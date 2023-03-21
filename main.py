import tkinter as tk
import camera_tab
import overview_tab
import palette

def open_overview():
    """Opens the overview tab"""
    overview_button.configure(bg=palette.ACCENT_COLOR_01)
    live_camera_button.configure(bg=palette.PRIMARY_COLOR_04)
    destroy_widgets(frame_right)
    overview_tab.create_overview_win(frame_right)


def open_camera_window():
    """Opens the camera window"""
    overview_button.configure(bg=palette.PRIMARY_COLOR_04)
    live_camera_button.configure(bg=palette.ACCENT_COLOR_01)
    destroy_widgets(frame_right)
    camera_tab.create_camera_win(frame_right)


def destroy_widgets(frame):
    """Destroys the currently displayed widgets"""
    if camera_tab.CAMERA_FLAG == True:
        camera_tab.CAMERA_FLAG = False
        camera_tab.capture.release()
        MODEL_FLAG = False

    for widget in frame.winfo_children():
        widget.destroy()


root = tk.Tk()
root.title("Face Recognition")
root.configure(background=palette.PRIMARY_COLOR_01)
window_height = 720
window_width = 1280

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))

root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate,
                                   y_coordinate))
root.resizable(False, False)

frame_left = tk.Frame(root, width=280, height=720, bg=palette.PRIMARY_COLOR_01)
frame_right = tk.Frame(root, width=1000, height=720, bg=palette.PRIMARY_COLOR_03)

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

frame_left.grid(row=0, column=0, sticky="w")
frame_right.grid(row=0, column=1)
frame_right.grid_propagate(False)

global overview_button
overview_button = tk.Button(frame_left,
                            text="Overview",
                            font=palette.FONT,
                            fg=palette.PRIMARY_COLOR_01,
                            width=15,
                            command=open_overview)
overview_button.pack(padx=10, pady=10)

global live_camera_button
live_camera_button = tk.Button(
    frame_left,
    text="Live Webcam",
    font=palette.FONT,
    fg=palette.PRIMARY_COLOR_01,
    width=15,
    command=open_camera_window,
)
live_camera_button.pack(pady=10)

open_overview()
root.mainloop()
