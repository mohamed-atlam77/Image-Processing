# Import required libraries
from tkinter import *
from PIL import ImageTk, Image, ImageFilter
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import messagebox
import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage

copies_list=list()
global iter
iter=0
# Create an instance of tkinter window
win = Tk()
win.title("Image Processing Project")

# Define the geometry of the window
win.geometry("1000x790+-10+0")
win.resizable(False, False)

def open_image():
    global img, image_directory, iter
    if iter==0:
        image_directory=str(fd.askopenfilename())
        img = Image.open(image_directory)
        save_a_copy()
        iter+=1
    else:
        save_a_copy()
        image_directory=str(fd.askopenfilename())
        img = Image.open(image_directory)
    img.thumbnail((790,700))
    show_image()

def flip_image_vertically():
    global img
    save_a_copy()
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    show_image()

def flip_image_horizontally():
    global img
    save_a_copy()
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    show_image()

def rotate(turns):
    global img
    save_a_copy()
    for i in range(turns):
        img = img.transpose(Image.ROTATE_90)
    show_image()

def to_gray():
    global img
    save_a_copy()
    img = img.convert("L")
    show_image()

def crop():
    global img
    save_a_copy()

    def clear_dimensions():
        dimension1_x_text.delete(1.0, END)
        dimension1_y_text.delete(1.0, END)
        dimension2_x_text.delete(1.0, END)
        dimension2_y_text.delete(1.0, END)

    def get_dimensions():
        global x1, y1, x2, y2
        x1=int(dimension1_x_text.get(1.0, END))
        y1=int(dimension1_y_text.get(1.0, END))
        x2=int(dimension2_x_text.get(1.0, END))
        y2=int(dimension2_y_text.get(1.0, END))


    false_dimensions=True
    while(false_dimensions):
        get_dimensions()
        if(x1<0 or x2<0 or y1<0 or y2<0):
            message=("You can't use negative numbers")
            messagebox.showwarning("Warning", message)
            clear_dimensions()

        elif(x1>=x2 or y1>=y2):
            message=("x1 can't be greater than or equal to x2.\n"+
            "y1 can't be greater than or equal to y2")
            messagebox.showwarning("Warning", message)
            clear_dimensions()

        elif(x2>img.width or y2>img.height):
            message=("x2 can't be greater than {}.\n".format(img.width)+
                     "y2 can't be greater than {}".format(img.height))
            messagebox.showwarning("Warning", message)
            clear_dimensions()

        else:
            false_dimensions=False

    img = img.crop((x1, y1, x2, y2))
    img = img.resize((x2-x1,y2-y1), Image.ANTIALIAS)
    img.thumbnail((790,700))
    clear_dimensions()
    show_image()


def plot_histogram():
    global img
    if(img.mode=="L"):
        img_arr = np.array(img)
        hist = cv2.calcHist(img_arr,[0], None, [256], [0,256])
        intensity_values = np.array([x for x in range(hist.shape[0])])
        plt.bar(intensity_values, hist[:,0], width = 5)
        plt.title("Bar histogram")
        plt.show()
    else:
        message=("The application only plot the histogram for grayscale images.\n"+
                 "Do you want to convert the image to grayscale image, then plot the histogram for it?")
        msgbox=messagebox.askyesno("askyesno", message)
        print(msgbox)
        if(msgbox==True):
            to_gray()
            plot_histogram()

def apply_averaging_filter():
    global img
    save_a_copy()
    noisy_image = np.array(img)
    kernel = np.ones((5,5))/25
    img = cv2.filter2D(src=noisy_image, ddepth=-1, kernel=kernel)
    img = Image.fromarray(img)
    show_image()

def apply_median_filter():
    global img
    save_a_copy()
    img = img.filter(ImageFilter.MedianFilter(size = 3))
    show_image()

def apply_sobel():
    global img
    apply_averaging_filter()
    to_gray()
    save_a_copy()
    initail_image = np.array(img)
    ddepth = cv2.CV_16S
    grad_x = cv2.Sobel(src=initail_image, ddepth=ddepth, dx=1, dy=0, ksize=3)
    grad_y = cv2.Sobel(src=initail_image, ddepth=ddepth, dx=0, dy=1, ksize=3)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    img = Image.fromarray(grad)
    show_image()

def apply_gaussian_filter():
    global img
    save_a_copy()
    initail_image = np.array(img)
    smoothed_img = cv2.GaussianBlur(initail_image,(5,5),cv2.BORDER_DEFAULT)
    img = Image.fromarray(smoothed_img)
    show_image()

def apply_adaptive_threshold():
    global img
    to_gray()
    save_a_copy()
    initail_image = np.array(img)
    threshold_img = cv2.adaptiveThreshold(initail_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    img = Image.fromarray(threshold_img)
    show_image()

def equalize_histogram():
    global img
    to_gray()
    save_a_copy()
    initail_image = np.array(img)
    equ = cv2.equalizeHist(initail_image)
    img = Image.fromarray(equ)
    show_image()

def apply_erosion():
    global img
    save_a_copy()
    kernel = np.ones((3,3), np.uint8)
    initail_image = np.array(img)
    img_erosion = cv2.erode(initail_image, kernel, iterations=1)
    img = Image.fromarray(img_erosion)
    show_image()

def apply_dilation():
    global img
    save_a_copy()
    kernel = np.ones((3,3), np.uint8)
    initail_image = np.array(img)
    img_dilation = cv2.dilate(initail_image, kernel, iterations=1)
    img = Image.fromarray(img_dilation)
    show_image()

def adjust_brightness_and_contrast():
    global img
    save_a_copy()
    initail_image = np.array(img)
    alpha_=float(contrast_constant_text.get(1.0, END))
    beta_=float(brightness_constant_text.get(1.0, END))
    new_image = cv2.convertScaleAbs(initail_image, alpha=alpha_, beta=beta_)
    img = Image.fromarray(new_image)
    contrast_constant_text.delete(1.0, END)
    brightness_constant_text.delete(1.0, END)
    show_image()

def save_a_copy():
    global img
    copies_list.append(img)

def save_image():
    global img
    directory=fd.asksaveasfilename(title = "Select file")
    img.save(directory)

def undo():
    global img
    if len(copies_list)!=0:
        if len(copies_list)==1:
            img = copies_list[0]
        else:
            img= copies_list.pop()
        show_image()

def show_image():
    new_img = ImageTk.PhotoImage(img)
    label.configure(image=new_img)
    label.image=new_img



# left_frame
left_frame = Frame(win, width=700, height=790)
left_frame.pack()
left_frame.place(anchor='nw', relx=0, rely=0)

label = Label(left_frame, width=700, height=790)
label.pack()
label.place(anchor='center', relx=0.5, rely=0.5)

# right_frame
right_frame=Frame(win, width=300, height=790)
right_frame.pack()
right_frame.place(anchor='nw', relx=0.7, rely=0)

# buttons

# A frame for openning and saving image
open_save_frame = LabelFrame(right_frame, text="Open/Save Image")
image_button = Button(open_save_frame, text="Open New Image", width=19 , pady=5, command=open_image)
save_button =  Button(open_save_frame, text="Save Image", width=19 , pady=5, command=save_image)
# A frame for rotating image
rotation_frame = LabelFrame(right_frame, text="Rotation")
clockwise_rotation = Button(rotation_frame, text="ClockWise", width=19, pady=5, command=lambda:rotate(3))
counter_clockwise_rotation = Button(rotation_frame, text="Counter ClockWise", width=19, pady=5, command=lambda:rotate(1))
# A frame for flipping image
flipping_frame = LabelFrame(right_frame, text="Flipping")
vertical_flip = Button(flipping_frame, text="Vertical Flip", width=19, pady=5, command=flip_image_vertically)
horizontal_flip = Button(flipping_frame, text="Horizontal Flip", width=19, pady=5, command=flip_image_horizontally)
# cropping frame
crop_frame = LabelFrame(right_frame, text="Cropping")
ll= Label(crop_frame, text="Assign Values to x and y to crop the image", width=40, pady=5, padx=4)
dimension1_x = Label(crop_frame, text="x1:", width=3, pady=5, padx=2)
dimension1_x_text = Text(crop_frame, height=1, width=4, bd=5)
dimension1_y = Label(crop_frame, text="y1:", width=3, pady=5, padx=2)
dimension1_y_text = Text(crop_frame, height=1, width=4, bd=5)
dimension2_x = Label(crop_frame, text="x2:", width=3, pady=5, padx=2)
dimension2_x_text = Text(crop_frame, height=1, width=4, bd=5)
dimension2_y = Label(crop_frame, text="y2:", width=3, pady=5, padx=2)
dimension2_y_text = Text(crop_frame, height=1, width=4, bd=5)
crop_button = Button(crop_frame, text="Crop", width=25, pady=5, command=crop)
# A frame for Morphological Transformations
transformation_frame = LabelFrame(right_frame, text="Morphological Transformations")
erosion_button = Button(transformation_frame, text="Apply erosion", width=19, pady=5, command=apply_erosion)
dilation_button = Button(transformation_frame, text="Apply Dilation", width=19, pady=5, command=apply_dilation)
# A frame for bluring Image
blur_frame = LabelFrame(right_frame, text="Blur Image")
avg_filter = Button(blur_frame, text="Apply Averaging filter", width=19, pady=5, command=apply_averaging_filter)
median_filter = Button(blur_frame, text="Apply median filter", width=19, pady=5, command=apply_median_filter)
gaussian_filter = Button(blur_frame, text="Apply Gaussian filter", width=38, pady=5, command=apply_gaussian_filter)
# A frame for brightness and contrast adjustment
brightness_contrast_frame = LabelFrame(right_frame, text="Brightness and Contrast Adjustment")
brightness_constant = Label(brightness_contrast_frame, text="brightness constant: ", pady=5, padx=2)
brightness_constant_text = Text(brightness_contrast_frame, height=1, width=7, bd=5)
contrast_constant = Label(brightness_contrast_frame, text="contrast constant: ", pady=5, padx=2)
contrast_constant_text = Text(brightness_contrast_frame, height=1, width=7, bd=5)
bright_contrast_button = Button(brightness_contrast_frame, text="Adjust Brightness and Contrast", width=40, pady=5, command=adjust_brightness_and_contrast)

grayscale_button = Button(right_frame, text="Convert To Gray-Scale", width=40, pady=5, command=to_gray)
undo_button = Button(right_frame, text="UNDO", width=40, pady=5, command=undo)
separator1 = ttk.Separator(right_frame, orient='horizontal')
separator2 = ttk.Separator(right_frame, orient='horizontal')
separator3 = ttk.Separator(right_frame, orient='horizontal')
histogram_button = Button(right_frame, text="Plot Histogram", width=40, pady=5, command=plot_histogram)
threshold_button = Button(right_frame, text="Apply Adaptive Threshold", width=40, pady=5, command=apply_adaptive_threshold)
hist_equalization_button = Button(right_frame, text="Apply Histogram Equalization", width=40, pady=5, command=equalize_histogram)
sobel_button = Button(right_frame, text="Apply Sobel Edge Detection", width=40, pady=5, command=apply_sobel)

exit_button= Button(right_frame, text="Exit", width=40, pady=5, command=win.quit)

# packing open_save_frame
open_save_frame.pack()
image_button.grid(row=0, column=0)
save_button.grid(row=0, column=1)
# packing flipping_frame
flipping_frame.pack()
vertical_flip.grid(row=0, column=0)
horizontal_flip.grid(row=0, column=1)
# packing rotation_frame
rotation_frame.pack()
clockwise_rotation.grid(row=0, column=0)
counter_clockwise_rotation.grid(row=0, column=1)
# packing cropping frame
crop_frame.pack()
ll.grid(row=0, column=0, columnspan=8)
dimension1_x.grid(row=1, column=0, columnspan=1)
dimension1_x_text.grid(row=1, column=1, columnspan=1)
dimension1_y.grid(row=1, column=2, columnspan=1)
dimension1_y_text.grid(row=1, column=3, columnspan=1)
dimension2_x.grid(row=1, column=4, columnspan=1)
dimension2_x_text.grid(row=1, column=5, columnspan=1)
dimension2_y.grid(row=1, column=6, columnspan=1)
dimension2_y_text.grid(row=1, column=7, columnspan=1)
crop_button.grid(row=2, column=0, columnspan=8)
#packing separator1
separator1.pack(fill='x', pady=3)
# packing grayscale_button
grayscale_button.pack()
# packing blur_frame
blur_frame.pack()
avg_filter.grid(row=0, column=0, columnspan=1)
median_filter.grid(row=0, column=1, columnspan=1)
gaussian_filter.grid(row=1, column=0, columnspan=2)
# packing brightness_contrast_frame
brightness_contrast_frame.pack()
brightness_constant.grid(row=0, column=0, columnspan=1)
brightness_constant_text.grid(row=0, column=1, columnspan=1)
contrast_constant.grid(row=1, column=0, columnspan=1)
contrast_constant_text.grid(row=1, column=1, columnspan=1)
bright_contrast_button.grid(row=2, column=0, columnspan=2)
# packing separator2
separator2.pack(fill='x', pady=3)
# packing some buttons
hist_equalization_button.pack()
threshold_button.pack()
sobel_button.pack()
histogram_button.pack()
# packing transformation_frame
transformation_frame.pack()
erosion_button.grid(row=0, column=0)
dilation_button.grid(row=0, column=1)
# packing separator3
separator3.pack(fill='x', pady=3)
# packing some buttons
undo_button.pack()
exit_button.pack()

image_directory=""
while image_directory=="":
    try:
        open_image()
    except:
        image_directory=""


win.mainloop()
