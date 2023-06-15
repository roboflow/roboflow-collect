import base64
import json
import optparse
import os
import time
import uuid
import string
import datetime

import cv2
import numpy as np
import requests
import roboflow
from sklearn.metrics.pairwise import cosine_similarity
from vidgear.gears import CamGear

# make image_queue dir if it doesn't exist
if not os.path.exists("image_queue"):
    os.mkdir("image_queue")

parser = optparse.OptionParser()

parser.add_option(
    "--ROBOFLOW_KEY",
    dest="ROBOFLOW_KEY",
    help="Roboflow API Key",
    default=os.environ.get("ROBOFLOW_KEY"),
)

parser.add_option(
    "--ROBOFLOW_PROJECT",
    dest="ROBOFLOW_PROJECT",
    help="Roboflow Project ID",
    default=os.environ.get("ROBOFLOW_PROJECT"),
)

parser.add_option(
    "--SAMPLE_RATE",
    dest="SAMPLE_RATE",
    help="Number of seconds between samples",
    default=os.environ.get("SAMPLE_RATE", 1),
)

parser.add_option(
    "--ROBOFLOW_WORKSPACE",
    dest="ROBOFLOW_WORKSPACE",
    help="Roboflow Workspace ID",
    default=os.environ.get("ROBOFLOW_WORKSPACE"),
)

# make bool
parser.add_option(
    "--COLLECT_ALL",
    help="Collect all images, not just those with sample-more tags",
    dest="COLLECT_ALL",
    default=os.environ.get("COLLECT_ALL", False),
)

parser.add_option(
    "--INFER_SERVER_DESTINATION",
    dest="INFER_SERVER_DESTINATION",
    help="URL of the server on which to run inference",
    default=os.environ.get("INFER_SERVER_DESTINATION"),
)

parser.add_option(
    "--STREAM_URL",
    dest="STREAM_URL",
    help="URL of the stream from which to collect data",
    default=os.environ.get("STREAM_URL", None),
)

parser.add_option(
    "--UNIQUE_FRAME_BUFFER",
    dest="UNIQUE_FRAME_BUFFER",
    help="Number of frames that should pass before a frame is considered unique",
    default=os.environ.get("UNIQUE_FRAME_BUFFER", 0),
)

parser.add_option(
    "--CLIP_TEXT_PROMPT",
    dest="CLIP_TEXT_PROMPT",
    help="Text prompt to use for CLIP",
    default=os.environ.get("CLIP_TEXT_PROMPT", ""),
)

parser.add_option(
    "--DRIFT_PROJECT",
    dest="DRIFT_PROJECT",
    help="The workspace into which random images should be added for measuring model drift",
    default=os.environ.get("DRIFT_PROJECT", ""),
)

parser.add_option(
    "--CLIP_TEXT_PROMPT_THRESHOLD",
    dest="CLIP_TEXT_PROMPT_THRESHOLD",
    help="Threshold for CLIP text prompt",
    default=os.environ.get("CLIP_TEXT_PROMPT_THRESHOLD", 0.2),
)

parser.add_option(
    "--STOP_COLLECTING_AFTER",
    dest="STOP_COLLECTING_AFTER",
    help="Stop collecting images after this many have been collected",
    default=os.environ.get("STOP_COLLECTING_AFTER", 0),
)

args = parser.parse_args()

if (
    not args[0].ROBOFLOW_KEY
    or not args[0].ROBOFLOW_PROJECT
    or not args[0].SAMPLE_RATE
    or not args[0].ROBOFLOW_WORKSPACE
    or not args[0].INFER_SERVER_DESTINATION
):
    # show help screen
    parser.print_help()
    exit()

API_KEY = args[0].ROBOFLOW_KEY
PROJECT_ID = args[0].ROBOFLOW_PROJECT
WORKSPACE_ID = args[0].ROBOFLOW_WORKSPACE
INFER_SERVER = args[0].INFER_SERVER_DESTINATION.strip("/")
UNIQUE_FRAME_BUFFER = int(args[0].UNIQUE_FRAME_BUFFER)
CLIP_TEXT_PROMPT = args[0].CLIP_TEXT_PROMPT

CLIP_TEXT_PROMPT_THRESHOLD = float(args[0].CLIP_TEXT_PROMPT_THRESHOLD)

# 1 in 100
RANDOM_SAMPLE_CHANCES = 100

if args[0].STREAM_URL:
    STREAM_URL = args[0].STREAM_URL
    video_feed = CamGear(source=STREAM_URL, stream_mode=True, logging=True).start()
else:
    video_feed = cv2.VideoCapture(0)

SEARCH_URL = (
    f"https://api.roboflow.com/{WORKSPACE_ID}/{PROJECT_ID}/search?api_key={API_KEY}"
)

rf = roboflow.Roboflow(api_key=API_KEY)
project = rf.project(PROJECT_ID)

images_saved = 0

if args[0].DRIFT_PROJECT:
    drift_project = rf.project(args[0].DRIFT_PROJECT)


def get_sample_more() -> dict:
    """
    Return a dictionary of sample-more tags and their associated embeddings and thresholds.
    """
    all_sample_more = {}

    payload = {"tag": "sample-more", "fields": ["id", "name", "tags", "embedding"]}

    try:
        response = requests.post(SEARCH_URL, json=payload)
    except Exception as e:
        print(e)
        return all_sample_more

    json_data = response.json()

    with open("sample-more.json", "w") as f:
        f.write(json.dumps(json_data, indent=4))

    for item in json_data["results"]:
        threshold = None
        reason = None

        for tag in item["tags"]:
            if tag.startswith("sample-threshold:"):
                threshold = tag.split(":")[1]
            elif tag.startswith("sample-tag:"):
                reason = tag.split(":")[1]

        if not threshold or not reason:
            continue

        if all_sample_more.get(reason):
            all_sample_more[reason].append(
                {"embedding": item["embedding"], "threshold": threshold}
            )
        else:
            all_sample_more[reason] = [
                {"embedding": item["embedding"], "threshold": threshold}
            ]

        print(
            f"Will send images related to {reason} with threshold > {threshold}% confidence to Roboflow"
        )

    return all_sample_more


def save_image(frame: cv2.VideoCapture, tags: list, project: roboflow.Project) -> None:
    """
    Run inference on an image and save predictions to CSV file.
    """
    uuid_for_image = uuid.uuid4().hex

    tags = [t.replace(" ", "-") for t in tags]
    tags = [t.translate(str.maketrans("", "", string.punctuation)) for t in tags]

    tags.append(datetime.datetime.now().strftime("%Y-%m-%d"))

    cv2.imwrite("image_queue/" + uuid_for_image + ".jpg", frame)

    project.upload("image_queue/" + uuid_for_image + ".jpg", tag_names=tags)

    print(f"Saved image {uuid_for_image}")

    os.remove("image_queue/" + uuid_for_image + ".jpg")

    global images_saved

    images_saved += 1


def get_clip_text_prompt() -> str:
    """
    Return a text prompt to use for CLIP.
    """

    text_prompt = requests.post(
        f"{INFER_SERVER}/clip/embed_text?api_key={API_KEY}",
        json={"text": CLIP_TEXT_PROMPT},
    ).json()["embeddings"][0]

    return text_prompt


def main() -> None:
    semantically_similar_images_to_check = get_sample_more()

    last_n_frame_buffer = []

    if CLIP_TEXT_PROMPT:
        text_prompt = get_clip_text_prompt()

    while True:
        if args[0].STOP_COLLECTING_AFTER and images_saved >= int(
            args[0].STOP_COLLECTING_AFTER
        ):
            print(
                f"Stopping collection because {images_saved} images have been collected."
            )
            break

        if args[0].STREAM_URL:
            frame = video_feed.read()
        else:
            _, frame = video_feed.read()

        embedding = requests.post(
            f"{INFER_SERVER}/clip/embed_image?api_key={API_KEY}",
            json={
                "image": [
                    {
                        "value": base64.b64encode(
                            cv2.imencode(".jpg", frame)[1]
                        ).decode("utf-8"),
                        "type": "base64",
                    }
                ]
            },
        )

        if not embedding.ok:
            print(f"Error getting embedding: {embedding.text}")
            continue

        embedding = embedding.json()

        if UNIQUE_FRAME_BUFFER > 1:
            last_n_frame_buffer.append(embedding["embeddings"][0])

            # get average of last 10 frames
            if len(last_n_frame_buffer) > 10:
                last_n_frame_buffer.pop(0)

            embedding["embeddings"][0] = np.mean(last_n_frame_buffer, axis=0)

        # compare to all embeddings
        if CLIP_TEXT_PROMPT:
            target1 = np.array([embedding["embeddings"][0]])
            target2 = np.array([text_prompt])

            similarity = cosine_similarity(target1, target2)[0][0]

            print(f"Similarity between frame and text prompt: {similarity}")

            if similarity >= CLIP_TEXT_PROMPT_THRESHOLD:
                save_image(frame, [CLIP_TEXT_PROMPT], project)
        else:
            similar_set = False

            for tag, embeddings in semantically_similar_images_to_check.items():
                similar = []

                for e in embeddings:
                    target1 = np.array([embedding["embeddings"][0]])
                    target2 = np.array([e["embedding"]])

                    similarity = cosine_similarity(target1, target2)[0][0]

                    print(f"Similarity between {tag} and image: {similarity}")

                    if similarity >= float(e["threshold"]) / 100:
                        similar.append(tag)
                        print(f"Found {tag} with similarity {similarity}")
                        similar_set = True

            if similar_set:
                save_image(frame, similar, project)

        if args[0].COLLECT_ALL: #is True:
            save_image(frame, "", project)

        if (
            args[0].DRIFT_PROJECT
            and np.random.randint(0, RANDOM_SAMPLE_CHANCES) == 0
        ):
            save_image(frame, [args[0].DRIFT_PROJECT], drift_project)

        time.sleep(float(args[0].SAMPLE_RATE))


# if args[0].STREAM_URL:
#     video_feed.release()

if __name__ == "__main__":
    main()

    # remove all image_queue files
    for f in os.listdir("image_queue"):
        os.remove(os.path.join("image_queue", f))
