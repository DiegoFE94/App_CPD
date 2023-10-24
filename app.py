# Importing required libs
from flask import Flask, render_template, request
from model import preprocess_img, predict_result

# Instantiating flask app
app = Flask(__name__)


# Home route
@app.route("/")
def main():
    return render_template("index.html")

#About route
@app.route('/about')
def about():
    return render_template('about.html')

#Future route
@app.route('/future')
def future():
    return render_template('future.html')

# Prediction route
@app.route('/prediction', methods=['POST'])
def predict_image_file():
    try:
        if request.method == 'POST':
            max_pred, max_box = preprocess_img(request.files['file'].stream)
            pred = predict_result(request.files['file'].stream,max_pred, max_box)
            return render_template("result.html", predictions=str(pred))

    except:
        error = "File cannot be processed."
        return render_template("result.html", err=error)


# Driver code
if __name__ == "__main__":
    app.run(port=9000, debug=True)
