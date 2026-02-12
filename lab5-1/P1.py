'''
Khanon Charoenphanupong
663040475-1
P1
'''

import tkinter as tk
from PIL import Image, ImageTk

def create_ui():
    root = tk.Tk()
    root.title("Login UI")
    root.geometry("500x750")
    root.configure(bg="#f0f0f0")

    def load_and_resize(path, size=(40, 40)):
        try:
            img = Image.open(path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except:
            return None

    img_g = load_and_resize("g.png")
    img_f = load_and_resize("f.png")
    img_in = load_and_resize("in.png")

    outer_border = tk.Frame(root, bg="#7ea7d8", padx=3, pady=3)
    outer_border.place(relx=0.5, rely=0.5, anchor="center")

    main_frame = tk.Frame(outer_border, bg="white", padx=40, pady=40)
    main_frame.pack()

    tk.Label(main_frame, text="LOGIN", font=("Arial", 14, "bold"),
             bg="white", fg="#555").pack(anchor="w", pady=(0, 30))

    tk.Label(main_frame, text="Email", font=("Arial", 10),
             bg="white", fg="#777").pack(anchor="w")
    e_canvas = tk.Canvas(main_frame, width=280, height=35,
                         bg="white", highlightthickness=0)
    e_canvas.pack(pady=(5, 20))
    e_canvas.create_rectangle(2, 2, 278, 33, outline="#ccc", width=1)
    email_entry = tk.Entry(main_frame, font=("Arial", 12), bd=0)
    e_canvas.create_window(140, 17, window=email_entry, width=260)

    tk.Label(main_frame, text="Password", font=("Arial", 10),
             bg="white", fg="#777").pack(anchor="w")
    p_canvas = tk.Canvas(main_frame, width=280, height=35,
                         bg="white", highlightthickness=0)
    p_canvas.pack(pady=(5, 10))
    p_canvas.create_rectangle(2, 2, 278, 33, outline="#ccc", width=1)
    pass_entry = tk.Entry(main_frame, font=("Arial", 12),
                          bd=0, show="*")
    p_canvas.create_window(140, 17, window=pass_entry, width=260)

    check_frame = tk.Frame(main_frame, bg="white")
    check_frame.pack(fill="x")
    tk.Checkbutton(check_frame, text="Remember me?",
                   bg="white", font=("Arial", 9),
                   activebackground="white",
                   fg="#555").pack(side="left")

    btn_canvas = tk.Canvas(main_frame, width=280, height=45,
                           bg="white", highlightthickness=0, cursor="hand2")
    btn_canvas.pack(pady=(20, 5))

    def draw_round_rect(canvas, x1, y1, x2, y2, radius, color):
        points = [
            x1+radius, y1, x2-radius, y1,
            x2, y1, x2, y1+radius,
            x2, y2-radius, x2, y2,
            x2-radius, y2, x1+radius, y2,
            x1, y2, x1, y2-radius,
            x1, y1+radius, x1, y1
        ]
        return canvas.create_polygon(points, fill=color, smooth=True)

    draw_round_rect(btn_canvas, 0, 0, 280, 40, 20, "#f05a8d")
    btn_canvas.create_text(140, 20, text="LOGIN",
                           fill="white", font=("Arial", 11, "bold"))

    tk.Label(main_frame, text="Forgot Password?",
             bg="white", fg="#aaa",
             font=("Arial", 9)).pack(anchor="e")

    # OR Section
    or_frame = tk.Frame(main_frame, bg="white")
    or_frame.pack(fill="x", pady=25)

    tk.Frame(or_frame, height=1, bg="#ddd").place(relx=0, rely=0.5, relwidth=0.42)

    or_border = tk.Label(
        or_frame,
        text="OR",
        bg="white",
        fg="#aaa",
        font=("Arial", 10),
        highlightbackground="#ddd",
        highlightthickness=1,
        padx=5
    )
    or_border.pack()

    tk.Frame(or_frame, height=1, bg="#ddd").place(relx=0.58, rely=0.5, relwidth=0.42)

    # Social Icons
    social_frame = tk.Frame(main_frame, bg="white")
    social_frame.pack()

    for img in [img_g, img_f, img_in]:
        if img:
            lbl = tk.Label(social_frame, image=img,
                           bg="white", cursor="hand2")
            lbl.image = img
            lbl.pack(side="left", padx=10)

    # Signup
    signup_frame = tk.Frame(main_frame, bg="white")
    signup_frame.pack(pady=(25, 0))

    tk.Label(signup_frame, text="Need an account?",
             bg="white", fg="#777",
             font=("Arial", 10)).pack(side="left")

    tk.Label(signup_frame, text="SIGN UP",
             bg="white",
             font=("Arial", 10, "underline"),
             fg="#555",
             cursor="hand2").pack(side="left", padx=5)

    root.mainloop()


if __name__ == "__main__":
    create_ui()
