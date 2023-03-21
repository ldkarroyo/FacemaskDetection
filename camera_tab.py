import tkinter as tk
from tkinter.filedialog import asksaveasfile
from PIL import Image, ImageTk
import cv2 as cv
import palette
import torch
import numpy as np

# Variables for the Webcam & Object Detection Models
CAMERA_FLAG = False
MODEL_FLAG = False

# Resolution as Input & for Face Recognition
RES_WIDTH = 1920
RES_HEIGHT = 1080

# Resolution for Object Detection
DETECT_WIDTH = 1600
DETECT_HEIGHT = 900

# Display Resolution for Tkinter Window
DISPLAY_WIDTH = 870
DISPLAY_HEIGHT = 490


# Face Mask Detector based on yolov5s.pt weights from YOLOv5
model = torch.hub.load("ultralytics/yolov5",
                              "custom",
                              path="tbd_facedet.pt",
                              force_reload=True)
model.conf = 0.60  # minimum confidence
model.iou = 0.50  # overlap threshold or intersection-over-union
#model.line_thickness = 3  # thickness of bounding boxes' lines
#model.img = 640  # img-size


###############################################
#          Webcam & Object Detection          #
###############################################
def invoke_camera():
    """Invokes the camera, and detections based on conditions"""
    _, frame = capture.read()

    # print(frame.shape)
    # Activates Detection
    if MODEL_FLAG is True:
        str_results = "\nframe:\n"

        # Inference: Face Mask Detection
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        frame = model(frame)  #, size=640
        
        # store the pandas dataframe
        dataframe_results = frame.pandas().xyxy[0]
        dataframe_results = dataframe_results.reset_index()

        frame = np.squeeze(frame.render())

        #Log Lines
        for index, row in dataframe_results.iterrows():
                    rounded_confidence = str(round(row["confidence"] * 100, 2))
                    str_results += ("\t[" + str(row["class"]) + ", " +
                                    str(row["name"]) + ", " +
                                    rounded_confidence + "%]\n")
        
        update_log(log_lines, str_results)
    else:
        # Convert to tkinter-compatible format
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)

    # Resize the display to fit the Tkinter Window
    frame = cv.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT),
                      interpolation=cv.INTER_AREA)

    frame = Image.fromarray(frame)
    frame = ImageTk.PhotoImage(image=frame)
    camera_viewport.imgtk = frame
    camera_viewport.configure(image=frame)
    camera_viewport.after(10, invoke_camera)

def toggle_camera():
    """Toggles camera state between on and off"""
    global CAMERA_FLAG  # global flag for camera state
    global camera_viewport  # camera label as tkinter container
    global capture  # video capture object

    if CAMERA_FLAG is False:
        CAMERA_FLAG = True

        camera_viewport = tk.Label(camera_frame,
                                   bg=palette.PRIMARY_COLOR_02,
                                   fg=palette.PRIMARY_COLOR_02)
        camera_viewport.grid(row=1, column=0, columnspan=3)

        capture = cv.VideoCapture(0)
        if capture is None or not capture.isOpened():
            print("Warning: unable to open video source...")
            tk.messagebox.showerror(
                "No Device Found",
                "Please connect & configure a cameraera for this module to work.",
            )
            CAMERA_FLAG = False
            return

        capture.set(cv.CAP_PROP_FRAME_WIDTH, RES_WIDTH)
        capture.set(cv.CAP_PROP_FRAME_HEIGHT, RES_HEIGHT)
        button_start["state"] = tk.NORMAL
        invoke_camera()
    else:
        CAMERA_FLAG = False
        camera_viewport.destroy()
        capture.release()
        button_start["state"] = tk.DISABLED


##########################################
#       Button-triggered Functions       #
##########################################
def start_model():
    """Triggers detection model invocation at button push"""
    global MODEL_FLAG
    MODEL_FLAG = True

    button_start["state"] = tk.DISABLED
    button_end["state"] = tk.NORMAL
    button_toggle["state"] = tk.DISABLED


def stop_model():
    """Triggers detection model termination at button push"""
    global MODEL_FLAG
    MODEL_FLAG = False

    button_start["state"] = tk.NORMAL
    button_end["state"] = tk.DISABLED
    button_toggle["state"] = tk.NORMAL


def update_log(lines: tk.Listbox, event: str):
    """Function to update listbox based on model output"""
    log_lines.configure(state="normal")
    lines.insert(tk.END, event)
    lines.see("end")
    log_lines.configure(state="disabled")


def clear_log():
    """Clears the log section"""
    log_lines.configure(state="normal")
    log_lines.delete(1.0, tk.END)
    log_lines.configure(state="disabled")


def save_log():
    """Saves the logged events to file"""
    logs_file = asksaveasfile(defaultextension=".txt",
                              initialfile="logs.txt",
                              initialdir="/<filename>")

    if logs_file:
        logs_file.write(log_lines.get(1.0, tk.END))
        logs_file.close()


##############################################
#      Hover Behaviors for the buttons       #
##############################################
def on_enter(button: tk.Button):
    """Changes button properties on hover (enter)"""
    if button.widget["state"] == tk.NORMAL:
        button.widget["bg"] = palette.ACCENT_COLOR_01
        button.widget["fg"] = palette.PRIMARY_COLOR_01


def on_enter_warn(button: tk.Button):
    """Changes button properties on hover (enter)"""
    if button.widget["state"] == tk.NORMAL:
        button.widget["bg"] = palette.ACCENT_COLOR_02
        button.widget["fg"] = palette.PRIMARY_COLOR_01


def on_leave(button: tk.Button):
    """Changes button properties back to normal on hover (exit)"""
    button.widget["bg"] = palette.ACCENT_COLOR_03
    button.widget["fg"] = palette.PRIMARY_COLOR_02


###############################################################
#       Create the Tkinter Window for the Webcam Module       #
###############################################################
def create_camera_win(root: tk.Tk):
    """Webcam Tab"""
    global camera_frame
    camera_frame = tk.Frame(root,
                            height=900,
                            width=900,
                            bg=palette.PRIMARY_COLOR_03)
    camera_frame.grid(row=0, column=1)

    # depends on the layout manager used by widgets INSIDE it
    camera_frame.grid_propagate(False)
    camera_frame.grid_columnconfigure(1, weight=1)

    # Webcam View Label
    global camera_label
    camera_label = tk.Label(
        camera_frame,
        text="Live Webcam Input",
        font=palette.FONT_TITLE,
        bg=palette.PRIMARY_COLOR_03,
    )
    camera_label.grid(row=0, column=0, columnspan=3, pady=20, padx=(25, 0))

    # This is the black box to alternate the camera feed's position
    global camera_box
    camera_box = tk.Frame(camera_frame,
                          height=680,
                          width=1390,
                          bg=palette.PRIMARY_COLOR_02)
    camera_box.grid(row=1, column=0, columnspan=3, padx=(10))

    # Button to signal the camera to turn on/off
    global button_toggle
    button_toggle = tk.Button(
        camera_frame,
        width=16,
        text="Webcam On/Off",
        font=palette.FONT,
        bg=palette.ACCENT_COLOR_03,
        fg=palette.PRIMARY_COLOR_02,
        command=toggle_camera,
    )
    button_toggle.grid(row=2, column=0, padx=(10), pady=(20, 10))
    button_toggle.bind("<Enter>", on_enter)
    button_toggle.bind("<Leave>", on_leave)

    # Button to signal the model to start its operation
    global button_start
    button_start = tk.Button(
        camera_frame,
        width=16,
        text="Start Model",
        font=palette.FONT,
        bg=palette.ACCENT_COLOR_03,
        fg=palette.PRIMARY_COLOR_02,
        state=tk.DISABLED,
        command=start_model,
    )
    button_start.grid(row=2, column=1, padx=(10), pady=(20, 10))
    button_start.bind("<Enter>", on_enter)
    button_start.bind("<Leave>", on_leave)

    # Button to signal the model to stop its operation
    global button_end
    button_end = tk.Button(
        camera_frame,
        width=16,
        text="Stop Model",
        font=palette.FONT,
        bg=palette.ACCENT_COLOR_03,
        fg=palette.PRIMARY_COLOR_02,
        command=stop_model,
        state=tk.DISABLED,
    )
    button_end.grid(row=2, column=2, pady=(20, 10))
    button_end.bind("<Enter>", on_enter_warn)
    button_end.bind("<Leave>", on_leave)

    # Notes Section
    # notes01 = tk.Label(
    #     camera_frame,
    #     text=
    #     """Users, please note that the camera may take a few seconds when being called.\nUsers who have virtual cameras set up (eg. OBS Virtual Camera), if your virtual cameras are not configured and are imposing priority over your physical camera device, a key solution is to temporarily uninstall/deactivate them. Otherwise, please disregard this.\n\nFeel free to ask any team member for assistance. Thank you very much!""",
    #     font=palette.FONT_TINY,
    #     bg=palette.PRIMARY_COLOR_03,
    #     justify="left",
    #     wraplength=500,
    # )
    # notes01.grid(row=4, column=0, columnspan=2, pady=10)

    # Log Section Frame
    log_frame = tk.Frame(root,
                         height=900,
                         width=640,
                         bg=palette.PRIMARY_COLOR_03)
    log_frame.grid(row=0, column=2)
    log_frame.grid_propagate(False)

    # Log-related Buttons
    global button_clear_log
    button_clear_log = tk.Button(
        log_frame,
        width=16,
        text="Clear Log",
        font=palette.FONT_SMALL,
        bg=palette.ACCENT_COLOR_03,
        fg=palette.PRIMARY_COLOR_02,
        command=clear_log,
    )
    button_clear_log.grid(row=0, column=0, pady=(70, 20), padx=(20, 20))
    button_clear_log.bind("<Enter>", on_enter)
    button_clear_log.bind("<Leave>", on_leave)

    global button_save_log
    button_save_log = tk.Button(
        log_frame,
        width=16,
        text="Save Log",
        font=palette.FONT_SMALL,
        bg=palette.ACCENT_COLOR_03,
        fg=palette.PRIMARY_COLOR_02,
        command=save_log,
    )
    button_save_log.grid(row=0, column=1, pady=(70, 20), padx=(0, 20))
    button_save_log.bind("<Enter>", on_enter)
    button_save_log.bind("<Leave>", on_leave)

    # Logs Section; Listbox & Scrollbar
    log_labelframe = tk.LabelFrame(
        log_frame,
        height=root.winfo_height() - 150,
        width=400,
        text="Logged Events [class number, class name, confidence %]",
    )
    log_labelframe.grid(row=1, column=0, columnspan=2, padx=(20, 20))
    log_labelframe.pack_propagate(False)

    scrollbar = tk.Scrollbar(log_labelframe)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    global log_lines
    log_lines = tk.Text(log_labelframe,
                        wrap=tk.WORD,
                        font=palette.FONT_TINY_MONO)
    log_lines.pack(expand=1, fill=tk.BOTH)
    log_lines.configure(state="disabled")

    log_lines.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=log_lines.yview)