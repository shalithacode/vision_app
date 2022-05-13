from flask import Flask, request, render_template

app = Flask(__name__, template_folder="template")

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/result", methods=["GET", "POST"])
def speech():
    
    # import os
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "shalitha98-9b0e0cb27e46.json"

    
    from google.cloud import vision
    from google.cloud import storage

    bucket_name = "cats__and__dogs"
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name)

    client = vision.ImageAnnotatorClient()

    cat_list=[]
    dog_list=[]

    for blob in blobs:
        
        path=f'gs://cats__and__dogs/{blob.name}'
         
        response = client.object_localization(
            {
                "source": {
                    "image_uri": path
                },
            }
        )

        objects = response.localized_object_annotations

        for object in objects:
            
            if str(object.name).lower() =='cat' and object.score >= 0.80:
                cat_list.append(f'https://storage.googleapis.com/cats__and__dogs/{blob.name}')
                
            if str(object.name).lower() =='dog' and object.score >= 0.80:
                dog_list.append(f'https://storage.googleapis.com/cats__and__dogs/{blob.name}')


    return render_template("index.html", cats=cat_list,dogs=dog_list)
    


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
