# Polyp Detection

This web app is made using Flask framework and is all about predicting a polyp in a colonoscopic image based on the deep learning model trained using small CNNs.

# Dependencies
- Python (3.9.0)
- Flask
- Keras
- Numpy
- Pillow
- Tensorflow
- Scikit-image
- Scikit-learn
- Opencv-python

## UI Framework

- Bootstrap

# Install Dependencies

Install the dependencies from the **requirements.txt** file.

```commandline
pip install -r requirements.txt
```

# Run

**cd** into the current directory and run the script.

```commandline
flask --app app.py run
```

# Test

- Choose an image from the test images folder.
- You will see a preview of the uploaded image.
- Click on **Predict** button and see the prediction.
