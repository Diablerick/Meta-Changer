import os
import re
import sys
import platform
import subprocess
import _tkinter
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from tkinter import PhotoImage
from tkinter import filedialog, messagebox
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2

# ///////////////////////////////////////////////////////VIDEO FILES////////////////////////////////////////////////////////////////
# Function to transform the text to Sentence case
def sentence_case(text):
    # Remove underscores and hyphens
    text = text.replace("_", " ").replace("-", " ")
    # Capitalize the first letter of each word
    return text.capitalize()

# Function to transform the text to Camel case
def camel_case(text):
    return text.title()

# Function to transform text to Uppercase
def uppercase(text):
    return text.upper()

# Function to process files in a directory
def process_files(directory, transformation):
    for filename in os.listdir(directory):
        if filename.lower().endswith((".mp4", ".avi", ".mov", ".wmv", ".mkv")):
            filepath = os.path.join(directory, filename)
            new_title = transformation(filename)
            os.rename(filepath, os.path.join(directory, new_title))
            print(f"Metadatos cambiados para {filename} a {new_title}")

# Function to handle button click
def process_directory():
    directory = filedialog.askdirectory()
    if directory:
        # Get the selected transformation
        selected_transformation = transformation_var.get()
        if selected_transformation == "Sentence case":
            process_files(directory, sentence_case)
        elif selected_transformation == "Camel case":
            process_files(directory, camel_case)
        elif selected_transformation == "Uppercase":
            process_files(directory, uppercase)
        messagebox.showinfo("Éxito", f"Texto cambiado a {selected_transformation}")

# ///////////////////////////////////////////////////////MP3 FILES//////////////////////////////////////////////////////////
def transform_filename(name):
    # Remove file extension
    base, ext = os.path.splitext(name)

    # Extract track number (if present)
    match = re.match(r"(\d{1,3})\s*[-.]?\s*(.*)", base)
    if match:
        track_number, title = match.groups()
        title = title.title().replace("-", "").replace(".", "")
    else:
        track_number = ""
        title = base.title().replace("-", "").replace(".", "")

    # Capitalize the first letter of the title
    title = title.capitalize()

    # Handle parentheses
    if "(" in title:
        title, _, rest = title.partition("(")
        rest = rest.capitalize()
        title += "(" + rest
    title = title.strip()

    # Capitalize the first letter after a period
    title = re.sub(r"\.(\w)", lambda m: "." + m.group(1).upper(), title)

    # Rebuild filename
    new_filename = f"{track_number} {title}{ext}"
    return new_filename

def transform_metadata(mp3_file):
    if mp3_file.lower().endswith(".mp3"):
        audio = ID3(mp3_file)
    else:
        return

    title = audio.get("TIT2", [])[0]
    title = title.capitalize()
    audio["TIT2"] = TIT2(encoding=3, text=title.capitalize())
                    
    # Transform the album
    album = audio.get("TALB", [""])[0]
    album = album.upper()
    audio["TALB"] = TALB(encoding=3, text=album)

    # Transform the artist
    artist = audio.get("TPE1", [""])[0]
    artist = artist.title()
    audio["TPE1"] = TPE1(encoding=3, text=artist)
    
    # save changes
    audio.save()

def transform_folder_name(folder_path):
    try:
        # Get the folder name
        folder_name = os.path.basename(folder_path)
 
        # Transform the name to uppercase
        new_folder_name = folder_name.upper()

        # Create the new route with the transformed name
        new_folder_path = os.path.join(os.path.dirname(folder_path), new_folder_name)

        # Change folder name
        os.rename(folder_path, new_folder_path)

        return new_folder_path
    except Exception as e:
        return str(e)

def transform_files(folder_path):
    for root, _, files in os.walk(folder_path):
        for name in files:
            if name.lower().endswith(".mp3"):
                mp3_file = os.path.join(root, name)
                transform_metadata(mp3_file)
                new_filename = transform_filename(name).replace(".mp3", "")
                os.rename(mp3_file, os.path.join(root, new_filename + ".mp3"))

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        transform_files(folder_path)
        new_folder_path = transform_folder_name(folder_path)
        if not new_folder_path.startswith("Error:"):
            for filename in os.listdir(new_folder_path):
                if filename.capitalize().endswith((".mp3")):
                    mp3_file = os.path.join(new_folder_path, filename)
                    transform_metadata(mp3_file)
            messagebox.showinfo("Éxito", "Metadatos de los archivos MP3.")
        else:
            messagebox.showerror("Error", new_folder_path)
    else:
        messagebox.showwarning("Advertencia", "No se seleccionó ninguna carpeta.")

# /////////////////////////////////////////////////////////IMG FILES///////////////////////////////////////////////////////////

# Function to process files in a directory
def process_img_files(directory, transformation):
    for filename in os.listdir(directory):
        if filename.lower().endswith((".jpeg", ".jpg", ".gif", ".png", ".tiff", ".raw", ".bmp")):
            filepath = os.path.join(directory, filename)
            new_title = transformation(filename)
            os.rename(filepath, os.path.join(directory, new_title))
            print(f"Metadatos cambiados para {filename} a {new_title}")

# Function to handle button click
def process_img_directory():
    directory = filedialog.askdirectory()
    if directory:
        # Get the selected transformation
        selected_transformation_img = transformation_var_img.get()
        if selected_transformation_img == "Sentence case":
            process_img_files(directory, sentence_case)
        elif selected_transformation_img == "Camel case":
            process_img_files(directory, camel_case)
        elif selected_transformation_img == "Uppercase":
            process_img_files(directory, uppercase)
        messagebox.showinfo("Éxito", f"Texto cambiado a {selected_transformation_img}")

# ///////////////////////////////////////////////////////////PDF FILES///////////////////////////////////////////////////////////////

# Function to process files in a directory
def process_pdf_files(directory, transformation):
    for filename in os.listdir(directory):
        if filename.lower().endswith((".pdf")):
            filepath = os.path.join(directory, filename)
            new_title = transformation(filename)
            os.rename(filepath, os.path.join(directory, new_title))
            print(f"Metadatos cambiados para {filename} a {new_title}")

# Function to handle button click
def process_pdf_directory():
    directory = filedialog.askdirectory()
    if directory:
        # Get the selected transformation
        selected_transformation_pdf = transformation_var_pdf.get()
        if selected_transformation_pdf == "Sentence case":
            process_pdf_files(directory, sentence_case)
        elif selected_transformation_pdf == "Camel case":
            process_pdf_files(directory, camel_case)
        elif selected_transformation_pdf == "Uppercase":
            process_pdf_files(directory, uppercase)
        messagebox.showinfo("Éxito", f"Texto cambiado a {selected_transformation_pdf}")

#///////////////////////////////////////////////////////// CLEAR CACHE ///////////////////////////////////////////////////////////
def clear_app_cache():
    try:
        if platform.system() == "Windows":
            # Clear application cache in Windows
            os.system("rmdir /s /q %temp%")
        else:
            # Clear application cache on Unix/Linux
            subprocess.run(["rm", "-rf", "/tmp/*"], check=True)
        return "Cache deleted successfully."
    except Exception as e:
        return f"Error deleting app cache: {str(e)}"

def clear_cache_button_clicked():
    result = clear_app_cache()
    if not result.startswith("Error:"):
        messagebox.showinfo("Success Cache cleared", result)
    else:
        messagebox.showerror("Error", result)

# ///////////////////////////////////////////////////////// GRAFIC INTERFACE /////////////////////////////////////////////////////////
root = tk.Tk()
root.title("Meta Changer")
root.geometry("270x320")
menubar = tk.Menu(root)
root.config(menu=menubar)
root.iconphoto(True, icon)
root.resizable(width=False, height=False)

# About the App Text
sample_text = """
                                                                            ¡Welcome to Meta Changer! 🎉
                                This application offers you the possibility of organizing file names to facilitate your digital work.
                                     It works with Mp3, Mp4, Avi, Mov, Wmv, Mkv, Jpeg, Jpg, Gif, Png, Tiff, Raw, Bmp and Pdf files.

Names and metadata are changed using the following code rules.

These are the 3 types of text version.

1. **Sentence case**:
    - The first letter becomes uppercase, and the rest becomes lowercase.

2. **Camel case**:
    - Each word begins with a capital letter.

3. **Uppercase**:
    - All words are in CAPITAL LETTERS.

                                **Transformation of metadata with mp3 files**:
For the transformation of metadata with mp3 files, a single rule is used for each type of metadata.

- **Name**: Sentence case
- **Interpreter**: Camel case
- **Album**: Uppercase

                                **Transformation of metadata with video, image and PDF files**:
Changing text is done with the same rules, except that they contain a selector to choose which type of case you want to use.
Note: This segment only works with the file name, it does not add interpreter or any other type of metadata.

- **Case selector**:
   - Option 1: "Sentence"
   - Option 2: "Camel case"
   - Option 3: "Uppercase"

                                **Button that adds the folder that contains the files to organize**.

Upon completion of the metadata transformation, the application throws an alert
which demonstrates what data has been transformed to the chosen case:

- **Alert type 1**: "Success: Text changed to Sentence case."
- **Alert type 2**: "Success: Text changed to Camel case."
- **Alert type 3**: "Success: Text changed to Uppercase."

                                                                Thank you for choosing this app!

"""

def AboutMess():
    MsgBox =  tk.messagebox.showinfo("Welcome", sample_text)

# Menu bar
filemenu = tk.Menu(menubar, tearoff=0) 
menubar.add_cascade(label="Menu", menu=filemenu)
filemenu.add_command(label="About", command=AboutMess)
filemenu.add_command(label="Exit",command=root.destroy)

# Canvas with a vertical scroll bar
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set, width=225, height=310, bg="whitesmoke")
canvas.pack(side="left", fill="both")
canvas.place(x=50, y=0)
scrollbar.pack(side="right", fill="y")

# Frame inside the canvas
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="ne")

# Separator lines
separator1 = tk.Frame(frame, height=2, bd=1, relief="sunken")
separator1.pack(fill="x", padx=0, pady=1)
# MP3 transformer
select_folder_aud_label = tk.Label(frame, text="MP3 Transform", bg="whitesmoke", fg="#273747", width=22, height=1)
select_folder_aud_label.pack(fill="x", pady=2)
select_button_audio = tk.Button(frame, text="Open folder", command=select_folder, width=22, height=1, bg="#273747", fg="whitesmoke")
select_button_audio.pack(fill="x", pady=10)

# Separator lines
separator1 = tk.Frame(frame, height=2, bd=1, relief="sunken")
separator1.pack(fill="x", padx="0",pady=1)
# Video transformer
select_folder_vid_label = tk.Label(frame, text="Video Transform", bg="whitesmoke", fg="#273747", width=22, height=1)
select_folder_vid_label.pack(fill="x", pady=2)
# Dropdown menu for transformation options
transformation_var = tk.StringVar()
transformation_var.set("Sentence case")
transformation_options = ["Sentence case", "Camel case", "Uppercase"]
transformation_dropdown = tk.OptionMenu(frame, transformation_var, *transformation_options)
transformation_dropdown.config(bg="#273747", fg="white", width=19, height=1, text="Fill X") 
transformation_dropdown.pack(fill="x", pady=2)
# Button to select a directory
select_directory_button = tk.Button(frame, text="Open folder", command=process_directory)
select_directory_button.config(bg="#273747", fg="whitesmoke", width=22, height=1)
select_directory_button.pack(fill="x", pady=10)

# Separator lines
separator1 = tk.Frame(frame, height=2, bd=1, relief="sunken")
separator1.pack(fill="x", padx=0, pady=2)
# Dropdown menu for transformation options
transformation_var_img = tk.StringVar()
transformation_var_img.set("Sentence case")
transformation_options_img = ["Sentence case", "Camel case", "Uppercase"]
transformation_label_img = tk.Label(frame, text="Img Transform", bg="whitesmoke", fg="#273747", height=1)
transformation_label_img.pack(fill="x", pady=2)
transformation_dropdown_img = tk.OptionMenu(frame, transformation_var_img, *transformation_options_img)
transformation_dropdown_img.config(bg="#273747", fg="white", width=19, height=1, text="Fill X")
transformation_dropdown_img.pack(fill="x", pady=2)
# Button to select a directory
select_directory_button_img = tk.Button(frame, text="Open folder", command=process_img_directory)
select_directory_button_img.config(bg="#273747", fg="whitesmoke", width=22, height=1)
select_directory_button_img.pack(fill="x", pady=7)

# Separator lines
separator1 = tk.Frame(frame, height=2, bd=1, relief="sunken")
separator1.pack(fill="x", padx=0, pady=1)
# Dropdown menu for transformation options
transformation_var_pdf = tk.StringVar()
transformation_var_pdf.set("Sentence case")
transformation_options_pdf = ["Sentence case", "Camel case", "Uppercase"]
transformation_label_pdf = tk.Label(frame, text="Pdf Transform", bg="whitesmoke", fg="#273747", height=1)
transformation_label_pdf.pack(fill="x", pady=2)
transformation_dropdown_pdf = tk.OptionMenu(frame, transformation_var_pdf, *transformation_options_pdf)
transformation_dropdown_pdf.config(bg="#273747", fg="white", width=19, height=1, text="Fill X")
transformation_dropdown_pdf.pack(fill="x", pady=2)
# Button to select a directory
select_directory_button_pdf = tk.Button(frame, text="Open folder", command=process_pdf_directory)
select_directory_button_pdf.config(bg="#273747", fg="whitesmoke", width=22, height=1)
select_directory_button_pdf.pack(fill="x", pady=7)

# Separator lines
separator1 = tk.Frame(frame, height=2, bd=1, relief="sunken")
separator1.pack(fill="x", padx=0, pady=1)
# Cache clear button
select_folder_cache_label = tk.Label(frame, text="Clear Cache", bg="whitesmoke", fg="#273747", width=22, height=1)
select_folder_cache_label.pack(fill="x", pady=2)
clear_cache_button = tk.Button(frame, text="Wipe", command=clear_cache_button_clicked, width=22, height=1, bg="#273747", fg="whitesmoke")
clear_cache_button.pack(fill="x", pady=7)

# Separator lines
separator1 = tk.Frame(frame, height=2, bd=1, relief="sunken")
separator1.pack(fill="x", padx=0, pady=1)

# Update the canvas scroll region
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

root.mainloop()
