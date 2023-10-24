# Importing required libs
import skimage.io
from keras.models import *
import cv2
import math

# Declare windows size and step of the window
WINDOW_SIZES = [150]      
window_sizes=WINDOW_SIZES 
step=10
# Loading model to make predictions
model = load_model("model.h5")


# Preparing and pre-processing the image
def preprocess_img(img_path):
    # Load image using skimage.io.imread
    or_img = skimage.io.imread(img_path)
    # Remove black borders, as they may affect the predictions.
    img = or_img[20:280,45:340,:]
    # Inicialize empty/0 variables
    max_pred = 0.0 # maximum prediction
    max_box = []   # box for the polyp detection
    # Loop window sizes: I will use only 150x150
    for win_size in window_sizes:
    # Loop on both dimensions of the image
        for top in range(0, img.shape[0] - win_size + 1, step):
            for left in range(0, img.shape[1] - win_size + 1, step):
            # compute the (top, left, bottom, right) of the bounding box
                box = (top, left, top + win_size, left + win_size)
            # crop the original image
                cropped_img = img[box[0]:box[2], box[1]:box[3],:]
            # normalize the cropped image (the same processing used for the CNN dataset)
                cropped_img = cropped_img * 1./255
            # reshape from (150, 150, 3) to (1, 150, 150, 3) for prediction
                cropped_img = cropped_img.reshape((1, cropped_img.shape[0], cropped_img.shape[1], cropped_img.shape[2]))
            # make a prediction for only one cropped small image 
                preds = model.predict(cropped_img, batch_size=None, verbose=0)
            # print(box[0],box[2],box[1],box[3], preds[0][0])
                if preds[0][0]> max_pred:
                    max_pred = preds[0][0]
                    max_box = box
    return max_pred, max_box 

# Predicting results in image
def predict_result(img_path, max_pred, max_box):
    # Load image using skimage.io.imread
    image = skimage.io.imread(img_path)
    # Define the coordinates of the rectangle (upper left corner and lower right corner).
    rectangle_top_left = (max_box[1]+45, max_box[0]+20)  
    rectangle_bottom_right = (max_box[3]+45, max_box[2]+20)
    # Convert the image uploaded in NumPy format to OpenCV format (BGR)
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # Truncate max_pred to draw in image
    pred = max_pred
    pred = math.trunc(pred * 100) / 100

    # Add rectangle and text if 'pred' is greater than or equal to 0.50
    if pred >= 0.50:
        # Determine the colour and thickness of the rectangle according to the value of 'pred'.
        if 0.50 <= pred < 0.65:
            color = (0, 255, 255)  # Yellow
        elif 0.65 <= pred < 0.80:
            color = (173, 255, 47)   # Yellow-Green
        else:
            color = (0, 128, 0)   # Blue
        thickness = 2
        cv2.rectangle(image_bgr, rectangle_top_left, rectangle_bottom_right, color, thickness)

        # Add text to the rectangle
        text = 'Polyp:{:.2f}'.format(pred)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_thickness = 1
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        text_position = (rectangle_top_left[0], rectangle_top_left[1] + text_size[1] + 5)

        # Get the background dimensions of the text
        text_bg_width = text_size[0] + 10
        text_bg_height = text_size[1] + 5

        # Create a background of the same colour as the rectangle.
        text_bg = image_bgr[rectangle_top_left[1]:rectangle_top_left[1] + text_bg_height,
                            rectangle_top_left[0]:rectangle_top_left[0] + text_bg_width]
        text_bg[:] = color

        # Write the text on the background
        cv2.putText(text_bg, text, (5, text_size[1]), font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)

        # Copy background with text back to the original image
        image_bgr[rectangle_top_left[1]:rectangle_top_left[1] + text_bg_height,
                  rectangle_top_left[0]:rectangle_top_left[0] + text_bg_width] = text_bg

    # Save the image for display
    output_path = 'static/image_with_rectangle.jpg'
    cv2.imwrite(output_path, image_bgr)
    # Return prediction
    porcentaje = math.trunc(max_pred * 10000) / 100
    if pred >= 0.50:
        max_pred = "Se han detectado pólipos en la imagen." 
    else:
        max_pred = "No se han detectado pólipos en la imagen."
    return max_pred