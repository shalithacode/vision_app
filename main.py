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

        cat_score = 0
        dog_score = 0

        for object in objects:
            
            if str(object.name).lower() =='cat':
                cat_score = object.score
                
            if str(object.name).lower() =='dog':
                dog_score = object.score

        
        if cat_score > dog_score:
            cat_list.append(blob.name.split('.')[0])
            

        if cat_score < dog_score:
            dog_list.append(blob.name.split('.')[0])
            
    print(cat_list,dog_list)

    cats =  ", ". join(cat_list)
    dogs =  ", ". join(dog_list)

    return render_template("index.html", cats=cats,dogs=dogs)
    



if __name__ == "__main__":
    app.run(debug=True, threaded=True)
