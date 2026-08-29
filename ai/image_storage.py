import os
import uuid
import json
from datetime import datetime



IMAGE_FOLDER = "data/images"

METADATA_FILE = "data/images/image_data.json"




def create_image_record(topic, alt_text):


    os.makedirs(
        IMAGE_FOLDER,
        exist_ok=True
    )


    os.makedirs(
        "data/images",
        exist_ok=True
    )



    image_id = str(uuid.uuid4())


    filename = (
        image_id + ".jpg"
    )


    image_path = os.path.join(
        IMAGE_FOLDER,
        filename
    )



    image_url = (
        f"/images/{filename}"
    )



    record = {


        "id":
            image_id,


        "filename":
            filename,


        "path":
            image_path,


        "url":
            image_url,


        "alt":
            alt_text,


        "topic":
            topic,


        "created_at":
            str(datetime.now())

    }



    save_metadata(record)



    return record






def save_metadata(record):


    data = []



    if os.path.exists(
        METADATA_FILE
    ):

        with open(
            METADATA_FILE,
            "r"
        ) as file:

            data = json.load(file)



    data.append(record)



    with open(
        METADATA_FILE,
        "w"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )






if __name__ == "__main__":



    image = create_image_record(

        "Kitchen Organization",

        "best kitchen cabinet organizers ideas"

    )



    print("\n===== IMAGE RECORD =====")


    print("File:")
    print(image["filename"])


    print("\nURL:")
    print(image["url"])


    print("\nALT:")
    print(image["alt"])