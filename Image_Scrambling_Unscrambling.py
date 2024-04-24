from PIL import Image
import numpy as np
import random
import string 
import secrets 
import tkinter
from tkinter import *
import tkinter as tk
import tkinter.messagebox as mbox
from tkinter import ttk
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter
from PIL import Image, ImageTk



#created main window
window = Tk()
window.geometry("1200x800")
window.title("Image Scrambling/Unscrambling")
window.configure(bg="light blue")



# this piece of code will convert the seed into key for PRNG 
def seed(key):
    seed=" "
    for char in key:
        if char.isdigit():
            seed+=char
        elif char.isalpha():
            seed+=str(ord(char))
        else:
            print("your seed was incorrect kindly insert the correct seed")
    #print(seed)
    return int(seed)


# it will generate a list of indexes in order the pixels get shuffle
# those indices will determine by PRNG (pseudorandom number generator) and PRNG will determined by key/seed 
def pseudoRandomnumber(array,key = None):
    if not key:
        alphabet = string.ascii_letters + string.digits 
        key = ''.join(secrets.choice(alphabet) for i in range(16)) 
        print("remember this key to decrypt your image= ", key)
    
    random.seed(seed(key)) #PRNG generator
    random_list=[]
    for i in range (len(array)-1,-1,-1):
        pick=random.randint(0,i)
        random_list.insert(0,pick)
    return random_list



# this will shuffle the pixels using FISHER YATES shuffling algorithm
def knuth_shuffles(array,key = None):
    PRNG = pseudoRandomnumber(array,key)
    #print(PRNG)
    #print(len(PRNG))

    for i in range(len(array)-1,-1,-1):
        j=PRNG[i]
        array[i],array[j]=array[j],array[i]
    return array

#this will reverse the algorithm to get the original image back
def reverse_shuffle(Shuffled_array,key = None):
    PRNG = pseudoRandomnumber(Shuffled_array,key)
    for i in range(0,len(Shuffled_array),+1):
                j=PRNG[i]
                Shuffled_array[j],Shuffled_array[i]=Shuffled_array[i],Shuffled_array[j]
    return Shuffled_array



def open_img():
    global width, height, Array
    filename = filedialog.askopenfilename(title="Select an Image File")
    if filename:
        img = Image.open(filename)
        print(img.size)
        width, height = img.size
        pixel_list = list(img.getdata())
        print(len(pixel_list))
        Array = np.array(pixel_list, dtype=int)

        # Resize the image to fit within a smaller size
        max_width = 400
        max_height = 300
        img = img.resize((max_width, max_height))

        # Convert PIL Image to PhotoImage
        img = ImageTk.PhotoImage(img)

        # Display the resized image on the GUI
        img_label = Label(window, image=img)
        img_label.image = img  # Keep reference to avoid garbage collection
        img_label.place(x=100, y=270)


#scrambling the image
def en_img():
    global width, height
    shuffled = knuth_shuffles(Array)
    print("extracting the pixels from the image......")
    pixels = [tuple(row) for row in shuffled]
    scrambled_image = Image.new("RGB", (width, height))
    scrambled_image.putdata(pixels)
    scrambled_image.save("scrambled_image.png")
    # Resize the image to a smaller size
    resized_image = scrambled_image.resize((400, 300))  # Adjust size as needed
    # Convert PIL Image to PhotoImage
    img = ImageTk.PhotoImage(resized_image)
    # Display the scrambled image on the GUI
    img_label = Label(window, image=img)
    img_label.image = img  # Keep reference to avoid garbage collection
    img_label.place(x=700, y=270)


#unscrambling the image 
def de_img():
    global width, height
    Key = input("kindly insert the key here: ")
    original_array = reverse_shuffle(Array, Key)
    pixels = [tuple(row) for row in original_array]
    original_image = Image.new("RGB", (width, height))
    original_image.putdata(pixels)
    original_image.save("original_image.jpg")
    # Resize the image to a smaller size
    resized_image = original_image.resize((400, 300))  # Adjust size as needed
    # Convert PIL Image to PhotoImage
    img = ImageTk.PhotoImage(resized_image)
    # Display the decrypted image on the GUI
    img_label = Label(window, image=img)
    img_label.image = img  # Keep reference to avoid garbage collection
    img_label.place(x=700, y=270)




def main():
    # top label
    top_level = Label(window, text="Image Scrambling/Descrambling", font=("Arial", 30), fg="#ffffff",bg="#333333")
    top_level.place(x=350, y=10)

    # original image label
    start1 = tk.Label(text="Original\nImage", font=("Arial", 26),fg="#FFFFFF",bg="#6F42C1")
    start1.place(x=150, y=150)

    # edited image label
    start1 = tk.Label(text="Scrambled/Unscrambled\nImage", font=("Arial", 26), fg="#FFFFFF",bg="#6F42C1")
    start1.place(x=850, y=150)

    # choose button created
    chooseb = Button(window, text="Choose", command=open_img, font=("Arial", 20), bg="orange", fg="blue", borderwidth=3, relief="raised")
    chooseb.place(x=150, y=40)

    # Encrypt button created
    enb = Button(window, text="Scramble", command=en_img, font=("Arial", 20), bg="light green", fg="blue", borderwidth=3, relief="raised")
    enb.place(x=150, y=600)

    # decrypt button created
    deb = Button(window, text="Unscramble", command=de_img, font=("Arial", 20), bg="light green", fg="blue", borderwidth=3, relief="raised")
    deb.place(x=1000, y=600)

    # exit button created
    exitb = Button(window, text="EXIT", command=exit_win, font=("Arial", 20), bg="red", fg="blue", borderwidth=3, relief="raised")
    exitb.place(x=1000, y=40)

    window.protocol("WM_DELETE_WINDOW", exit_win)
    window.mainloop()

def exit_win():
    if mbox.askokcancel("Exit", "Do you want to exit?"):
        window.destroy()

if __name__ == "__main__":
    main()


