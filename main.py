import tkinter as tk
import webcam_tab
import cctv_tab
import overview_tab
import video_upload
import image_tab
import palette

global temp


def open_overview():
    overview_button.configure(bg=palette.ACCENT_COLOR_01)
    # video_upload_button.configure(bg=palette.PRIMARY_COLOR_04)
    # live_button.configure(bg=palette.PRIMARY_COLOR_04)
    live_webcam_button.configure(bg=palette.PRIMARY_COLOR_04)
    # image_upload_button.configure(bg=palette.PRIMARY_COLOR_04)
    destroy_widgets(frame_right)
    overview_tab.create_overview_win(frame_right)


def open_video_upload_window():
    overview_button.configure(bg=palette.PRIMARY_COLOR_04)
    # video_upload_button.configure(bg=palette.ACCENT_COLOR_01)
    # live_button.configure(bg=palette.PRIMARY_COLOR_04)
    live_webcam_button.configure(bg=palette.PRIMARY_COLOR_04)
    # image_upload_button.configure(bg=palette.PRIMARY_COLOR_04)
    destroy_widgets(frame_right)
    video_upload.video_frame(frame_right)


def open_cctv_window():
    overview_button.configure(bg=palette.PRIMARY_COLOR_04)
    # video_upload_button.configure(bg=palette.PRIMARY_COLOR_04)
    # live_button.configure(bg=palette.ACCENT_COLOR_01)
    live_webcam_button.configure(bg=palette.PRIMARY_COLOR_04)
    # image_upload_button.configure(bg=palette.PRIMARY_COLOR_04)
    destroy_widgets(frame_right)
    cctv_tab.initialize_frame(frame_right)


def open_webcam_window():
    overview_button.configure(bg=palette.PRIMARY_COLOR_04)
    # video_upload_button.configure(bg=palette.PRIMARY_COLOR_04)
    # live_button.configure(bg=palette.PRIMARY_COLOR_04)
    live_webcam_button.configure(bg=palette.ACCENT_COLOR_01)
    # image_upload_button.configure(bg=palette.PRIMARY_COLOR_04)
    destroy_widgets(frame_right)
    webcam_tab.create_webcam_win(frame_right)


def open_image_upload_window():
    destroy_widgets(frame_right)
    image_tab.create_frames(frame_right)


def destroy_widgets(frame):
    if webcam_tab.WEBCAM_FLAG == True:
        webcam_tab.WEBCAM_FLAG = False
        webcam_tab.capture.release()

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
frame_right = tk.Frame(root,
                       width=1000,
                       height=720,
                       bg=palette.PRIMARY_COLOR_03)

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
overview_button.pack(padx=50, pady=30)

global live_webcam_button
live_webcam_button = tk.Button(
    frame_left,
    text="Live Webcam",
    font=palette.FONT,
    fg=palette.PRIMARY_COLOR_01,
    width=15,
    command=open_webcam_window,
)
live_webcam_button.pack(pady=30)

# global image_upload_button
# image_upload_button = tk.Button(frame_left,
#                                 text="Image Upload",
#                                 font=palette.FONT,
#                                 fg=palette.PRIMARY_COLOR_01,
#                                 width=15)
# image_upload_button.pack(pady=30)

# root.update()

open_overview()
root.mainloop()
