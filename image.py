from tkinter import *
from tkinter import filedialog, Toplevel, Canvas
from PIL import Image, ImageTk, ImageDraw
import os

selected_file = None
cropped_image = None

# Function to create a default circular person icon
def create_person_icon(size=100):
    icon = Image.new("RGBA", (size, size), (200, 200, 200, 0))
    draw = ImageDraw.Draw(icon)
    
    head_radius = size // 4
    head_x = size // 2
    head_y = size // 3
    draw.ellipse((head_x - head_radius, head_y - head_radius, head_x + head_radius, head_y + head_radius), fill=(100, 100, 100))
    draw.rectangle((size // 4, head_y + head_radius, size * 3 // 4, size), fill=(100, 100, 100))
    
    return ImageTk.PhotoImage(icon)

# Function to browse and display the selected image
def showimage():
    global selected_file, cropped_image

    fln = filedialog.askopenfilename(initialdir=os.getcwd(), 
                                     title="Select Image File", 
                                     filetypes=[("JPG files", "*.jpg"), 
                                                ("PNG files", "*.png"), 
                                                ("All files", "*.*")])
    if fln:
        selected_file = fln
        img = Image.open(fln)
        img = img.resize((300, 300))  # Resize for cropping
        cropped_image = img
        img_tk = ImageTk.PhotoImage(img)
        
        lbl.configure(image=img_tk)
        lbl.image = img_tk
        crop_btn.pack(side=LEFT, padx=10)  # Show crop button after an image is loaded

# Crop tool logic
def open_crop_tool():
    global cropped_image

    if cropped_image:
        crop_window = Toplevel(root)
        crop_window.title("Crop Tool")

        canvas = Canvas(crop_window, width=300, height=300)
        canvas.pack()
        img_tk = ImageTk.PhotoImage(cropped_image)
        canvas.create_image(0, 0, anchor=NW, image=img_tk)
        canvas.image = img_tk

        rect_id = [None]  # To store the rectangle ID
        start_x, start_y = [0], [0]

        def start_crop(event):
            start_x[0], start_y[0] = event.x, event.y
            rect_id[0] = canvas.create_rectangle(start_x[0], start_y[0], event.x, event.y, outline="red", width=2)

        def update_crop(event):
            canvas.coords(rect_id[0], start_x[0], start_y[0], event.x, event.y)

        def apply_crop():
            global cropped_image
            if rect_id[0]:
                x1, y1, x2, y2 = canvas.coords(rect_id[0])
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cropped_image = cropped_image.crop((x1, y1, x2, y2))
                crop_window.destroy()

                # Display cropped image in the main window
                img_tk_cropped = ImageTk.PhotoImage(cropped_image.resize((150, 150)))
                lbl.configure(image=img_tk_cropped)
                lbl.image = img_tk_cropped
            else:
                crop_window.destroy()  # Close without cropping if no rectangle drawn

        # Bind events for cropping
        canvas.bind("<Button-1>", start_crop)
        canvas.bind("<B1-Motion>", update_crop)

        # Add Apply button
        Button(crop_window, text="Apply Crop", command=apply_crop).pack(pady=10)

# Function to save the cropped image
def submit_button():
    global cropped_image

    if cropped_image:
        try:
            # Create a folder to store photos if it doesn't exist
            folder_name = "photos"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            
            # Save the cropped image
            file_path = os.path.join(folder_name, "profile_picture.jpg")
            cropped_image.save(file_path)
            
            lbl_result.config(text=f"Profile picture saved as {file_path}!", fg="green")
        except Exception as e:
            lbl_result.config(text=f"Error saving profile picture: {str(e)}", fg="red")
    else:
        lbl_result.config(text="Please upload and crop an image.", fg="red")

# UI Setup
root = Tk()
root.title("User Profile with Crop Tool")
root.geometry("350x500")

# Frame for buttons
frm = Frame(root)
frm.pack(side=BOTTOM, padx=15, pady=15)

# Placeholder for displaying images
lbl = Label(root)
lbl.pack(pady=20)
placeholder_img = create_person_icon(size=150)
lbl.configure(image=placeholder_img)

# Browse button
btn = Button(frm, text="Browse Image", command=showimage)
btn.pack(side=LEFT, padx=10)

# Crop button
crop_btn = Button(frm, text="Crop Image", command=open_crop_tool)

# Submit button
submit_btn = Button(frm, text="Submit", command=submit_button)
submit_btn.pack(side=LEFT, padx=10)

# Label for displaying results
lbl_result = Label(root, text="", fg="green")
lbl_result.pack(pady=10)

# Run the Tkinter main loop
root.mainloop()





