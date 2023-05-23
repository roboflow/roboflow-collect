import datetime
import optparse
import os
from typing import Tuple

import numpy as np
import requests
import tabulate
from sklearn.metrics.pairwise import cosine_similarity

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
    "--ROBOFLOW_WORKSPACE",
    dest="ROBOFLOW_WORKSPACE",
    help="Roboflow Workspace ID",
    default=os.environ.get("ROBOFLOW_WORKSPACE"),
)

parser.add_option(
    "--DRIFT_PROJECT",
    dest="DRIFT_PROJECT",
    help="ID of your project storing representative images from Roboflow Collect",
    default=os.environ.get("DRIFT_PROJECT"),
)

args = parser.parse_args()

if (
    not args[0].ROBOFLOW_KEY
    or not args[0].ROBOFLOW_PROJECT
    or not args[0].ROBOFLOW_WORKSPACE
    or not args[0].DRIFT_PROJECT
):
    # show help screen
    parser.print_help()
    exit()


def get_clip_vectors(project_id: str) -> Tuple[list, dict]:
    project_clip_vectors = []
    images_by_time = {}

    limit = 125
    offset = 0

    while True:
        response = requests.post(
            f"https://api.roboflow.com/{args[0].ROBOFLOW_WORKSPACE}/{project_id}/search?api_key={args[0].ROBOFLOW_KEY}",
            json={
                "limit": limit,
                "query": "drift",
                "fields": ["split", "embedding", "tags"],
                "in_dataset": "true",
                "offset": offset,
            },
        )

        offset += limit

        if response.status_code != 200:
            print(response.status_code)
            break

        response = response.json()

        for image in response["results"]:
            if image["split"] != "valid":
                continue

            # add tag called time-YYYY-MM-DD
            image["tags"].append(f"time-2023-01-01")

            # get the time from the tags
            for tag in image["tags"]:
                if tag.startswith("time-"):
                    time = tag.lstrip("time-")

                    formatted_date = datetime.datetime.strptime(time, "%Y-%m-%d")

                    time = f"{formatted_date.year}-{formatted_date.month}"

                    if time not in images_by_time:
                        images_by_time[time] = []

                    images_by_time[time].append(image["embedding"])

            project_clip_vectors.append(image["embedding"])

    # split dates by YYYY-MM
    clip_vectors_by_month = {}

    for time in images_by_time:
        date = datetime.datetime.strptime(time, "%Y-%m")
        month = f"{date.year}-{date.month}"

        if month not in clip_vectors_by_month:
            clip_vectors_by_month[month] = []

        clip_vectors_by_month[month].extend(images_by_time[time])

    # order dict by month
    clip_vectors_by_month = dict(sorted(clip_vectors_by_month.items()))

    avg_clip_vectors_by_month = {}

    for month in clip_vectors_by_month:
        avg_clip_vectors_by_month[month] = [
            sum(x) / len(x) for x in zip(*clip_vectors_by_month[month])
        ]

    return project_clip_vectors, avg_clip_vectors_by_month


main_project_clip_vectors, main_project_clip_vectors_by_month = get_clip_vectors(
    args[0].ROBOFLOW_PROJECT
)
drift_project_clip_vectors, drift_project_clip_vectors_by_month = get_clip_vectors(
    args[0].DRIFT_PROJECT
)

avg_val_main_clip_vectors = [sum(x) / len(x) for x in zip(*main_project_clip_vectors)]

by_month = []

for month in main_project_clip_vectors_by_month:
    drift_vectors = drift_project_clip_vectors_by_month[month]
    by_month.append(
        [month, cosine_similarity([drift_vectors], [avg_val_main_clip_vectors])[0]]
    )

avg_drift_vectors = [sum(x) / len(x) for x in zip(*drift_project_clip_vectors)]
avg_main_vectors = [sum(x) / len(x) for x in zip(*main_project_clip_vectors)]

by_month.append(
    ["All Time", cosine_similarity([avg_drift_vectors], [avg_main_vectors])[0]]
)

print(tabulate.tabulate(by_month, headers=["Month", "Cosine Similarity"]))
