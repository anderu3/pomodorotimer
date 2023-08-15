import tkinter as tk
import math
import os
import sys
from tkinter import simpledialog


#Get image path of tomato after packing

def get_image_path(filename):
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
    else:
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(bundle_dir, filename)
    return image_path

#Variables

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
work_min = 25 # default
short_break_min = 5 #default
long_break_min = 30 #default
reps = 0
timer = None

#Resetting timer

def reset_timer():
    global reps
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer")
    check_marks.config(text="")
    reps = 0
    start_button.config(state="normal")

#Timer

def ask_time(question, default_value):
    answer = simpledialog.askstring(title="Time Input", prompt=question, initialvalue=default_value, parent=window)
    return int(answer) if answer and answer.isdigit() else int(default_value)

def ask_for_time_variables():
    global work_min, short_break_min, long_break_min
    work_min = ask_time("Study time? (minutes)", str(work_min))
    short_break_min = ask_time("Break time? (minutes)", str(short_break_min))
    long_break_min = ask_time("Long break time? (minutes)", str(long_break_min))

    
def start_timer():
    global reps
    reps += 1
    work_sec = work_min * 60
    short_break_sec = short_break_min * 60
    long_break_sec = long_break_min * 60
    start_button.config(state="disable")

    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="Break", fg=GREEN)
    if reps % 2 != 0:
        count_down(work_sec)
        timer_label.config(text="Study", fg=YELLOW)
    if reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="Break", fg=RED)

#Countdown

def count_down(count):
    global timer
    count_minute = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_minute}:{count_sec}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        enable_start_button()

def enable_start_button():
        start_button.config(state="normal")
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✓"
        check_marks.config(text=marks)
        window.focus_force()


#UI

window = tk.Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=PINK)

timer_label = tk.Label(text="Timer", fg=YELLOW, font=(FONT_NAME, "40", "bold"), bg=PINK)
timer_label.grid(column=1, row=0)

canvas = tk.Canvas(width=200, height=224, bg=PINK, highlightthickness=0)
tomato_img_path = get_image_path("tomato.png")
tomato_img = tk.PhotoImage(file=tomato_img_path)
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="black", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = tk.Button(text="Start", bg=PINK, highlightbackground=PINK, command=start_timer)
start_button.grid(column=0, row=3)
reset_button = tk.Button(text="Reset", bg=PINK, highlightbackground=PINK, command=reset_timer)
reset_button.grid(column=2, row=3)

check_marks = tk.Label(bg=PINK)
check_marks.grid(column=1, row=4)

window.after(100, ask_for_time_variables)

window.update_idletasks()
window_width = window.winfo_reqwidth()
window_height = window.winfo_reqheight()
position_right = int(window.winfo_screenwidth()/2 - window_width/2)
position_down = int(window.winfo_screenheight()/2 - window_height/2)
window.geometry("+{}+{}".format(position_right, position_down))

window.mainloop()

