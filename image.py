import cv2
import tkinter as tk
from tkinter import filedialog, Scale, Button
from PIL import Image, ImageTk

file_path = ""
sketch_image = None

def convert_to_sketch(image_path, line_thickness=3, contrast=1.3, brightness=50):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Increase the contrast
    adjusted_image = cv2.convertScaleAbs(gray_image, alpha=contrast, beta=0)

    # Adjust brightness
    if brightness < 0:
        darkened_image = cv2.subtract(adjusted_image, -brightness)
    else:
        darkened_image = cv2.add(adjusted_image, brightness)

    # Apply GaussianBlur to the adjusted grayscale image
    blurred_image = cv2.GaussianBlur(darkened_image, (21, 21), 0)

    # Invert the blurred image
    inverted_image = cv2.bitwise_not(blurred_image)

    # Convert the inverted image to a sketch-like effect
    sketch = cv2.divide(gray_image, inverted_image, scale=256.0)

    # Apply bilateral filter to smooth the sketch
    sketch_smoothed = cv2.bilateralFilter(sketch, 9, 75, 75)

    return sketch_smoothed

def update_sketch(*args):
    # Get the current values of the scales
    line_thickness = line_thickness_scale.get()
    contrast = contrast_scale.get()
    brightness = brightness_scale.get()

    # Convert the image to a sketch with the updated parameters
    global sketch_image
    sketch_image = convert_to_sketch(
        file_path,
        line_thickness=line_thickness,
        contrast=contrast,
        brightness=brightness,
    )

    # Display the updated sketch image
    sketch_image_label.image = ImageTk.PhotoImage(
        image=Image.fromarray(sketch_image).resize((300, 300))
    )
    sketch_image_label.config(image=sketch_image_label.image)

def save_sketch():
    if sketch_image is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            cv2.imwrite(file_path, sketch_image)

def select_image():
    global file_path
    # Open a fi-+
    # le dialog to select an image
    file_path = filedialog.askopenfilename()

    # Check if a file is selected
    if file_path:
        # Display the original image
        original_image_label.image = ImageTk.PhotoImage(
            image=Image.open(file_path).resize((300, 300))
        )
        original_image_label.config(image=original_image_label.image)

        # Update the sketch with the current parameters
        update_sketch()

# Create the main window
root = tk.Tk()
root.title("Image to Sketch Converter")

# Create a button to select an image
select_button = tk.Button(root, text="Select Image", command=select_image)
select_button.pack(pady=10)

# Create scales for adjusting line thickness, contrast, and brightness
line_thickness_scale = Scale(
    root, label="Line Thickness", from_=1, to=10, orient=tk.HORIZONTAL, length=300, command=update_sketch
)
line_thickness_scale.pack()

contrast_scale = Scale(
    root, label="Contrast", from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL, length=300, command=update_sketch
)
contrast_scale.set(1.3)
contrast_scale.pack()

brightness_scale = Scale(
    root, label="Brightness", from_=-100, to=100, orient=tk.HORIZONTAL, length=300, command=update_sketch
)
brightness_scale.set(50)
brightness_scale.pack()

# Create labels to display the original image and the sketch image side by side
images_frame = tk.Frame(root)
images_frame.pack(padx=10, pady=5)

original_image_label = tk.Label(images_frame)
original_image_label.pack(side=tk.LEFT, padx=10)

sketch_image_label = tk.Label(images_frame)
sketch_image_label.pack(side=tk.RIGHT, padx=10)

# Create a "Save" button to save the sketch image
save_button = Button(root, text="Save", command=save_sketch)
save_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
