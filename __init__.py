from flask import Flask, render_template, request, redirect
from digit_classifier.forms import SubmitForm
from digit_classifier.model import classify_image
import os


def create_app():
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = "uploads"
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
    app.config["ALLOWED_EXTENSIONS"] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    def file_allowed(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

    @app.route('/', methods=["GET", "POST"])
    def index():
        form = SubmitForm()
        if request.method == "POST":
            # Test that file was actually uploaded
            if "upload" not in request.files:
                return redirect(request.url)

            # Save file and load image
            uploaded_file = request.files["upload"]
            fname = uploaded_file.filename
            if file_allowed(fname):
                img_source = os.path.join("static", app.config["UPLOAD_FOLDER"], fname)
                uploaded_file.save(img_source)
                digit = classify_image(img_source)
                return render_template("result.html", img_source=img_source, digit=digit)
            else:
                return render_template("result.html")

        return render_template("index.html", submit_form=form)

    return app
