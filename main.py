from flask import Flask, request, render_template

app = Flask(__name__, template_folder="template")

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/result", methods=["GET", "POST"])
def speech():
    transcript = ""
    # import os
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "shalithatestproject-4399094c0dde.json"

    # Imports the Google Cloud client library
    from google.cloud import vision

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Performs label detection on the image file
    response = client.label_detection(
        {
            "source": {
                "image_uri": "gs://shalithatestproject.appspot.com/sample/human.jpeg"
            },
        }
    )
    labels = response.label_annotations

    # print("Labels:")
    allDescreiptios = []
    
    for label in labels:
        allDescreiptios.append({label.description:str(round(label.score * 100 ,2))})

    return render_template("index.html", transcript=allDescreiptios)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
