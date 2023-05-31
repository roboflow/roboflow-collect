import datetime
import optparse
import os
import warnings
from typing import Tuple

import numpy as np
import requests
import tabulate
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings("ignore", category=FutureWarning)

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

parser.add_option(
    "--INCREMENT",
    dest="INCREMENT",
    help="Increment to group images by",
    default=os.environ.get("INCREMENT", "month"),
)

args = parser.parse_args()

if (
    not args[0].ROBOFLOW_KEY
    or not args[0].ROBOFLOW_PROJECT
    or not args[0].ROBOFLOW_WORKSPACE
    or not args[0].DRIFT_PROJECT
):
    parser.print_help()
    exit()

if args[0].INCREMENT not in ["day", "month", "year"]:
    print("Increment must be day, month, or year")
    exit()


def retrieve_by_period(period: str, images: list) -> Tuple[list, dict]:
    """
    Split up images by time period.
    """
    clip_vectors = {}

    for time in images:
        date = datetime.datetime.strptime(time, period)

        formatted_period = date.strftime(period)

        if formatted_period not in clip_vectors:
            clip_vectors[formatted_period] = []

        clip_vectors[formatted_period].extend(images[time])

    clip_vectors = dict(sorted(clip_vectors.items()))

    avg_clip_vectors = {}

    for time_period in clip_vectors:
        avg_clip_vectors[time_period] = [
            sum(x) / len(x) for x in zip(*clip_vectors[time_period])
        ]

    for time_period in avg_clip_vectors:
        avg_clip_vectors[time_period] = np.array(
            avg_clip_vectors[time_period]
        ).reshape(1, -1)

    return clip_vectors, avg_clip_vectors


def get_clip_vectors(
    project_id: str, is_drift: bool = False, period: str = "%Y-%m"
) -> Tuple[list, dict]:
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
                "fields": ["split", "embedding", "tags", "created"],
                "in_dataset": "true",
                "offset": offset,
            },
        )

        offset += limit

        if response.status_code != 200:
            print(response.status_code)
            break

        response = response.json()

        if len(response["results"]) == 0:
            break

        print(len(response["results"]))

        for image in response["results"]:
            created = image["created"]

            # convert from milliseconds to YYYY-MM-DD
            created = datetime.datetime.fromtimestamp(created / 1000).strftime("%Y-%m-%d")

            if image["split"] != "valid" and not is_drift:
                print(f"Skipping {image['image_id']} because it's not in the valid split")
                continue

            formatted_date = datetime.datetime.strptime(created, "%Y-%m-%d")

            time = f"{formatted_date.year}-{formatted_date.month:02d}"

            if time not in images_by_time:
                images_by_time[time] = []

            images_by_time[time].append(image["embedding"])

            project_clip_vectors.append(image["embedding"])

    avg_clip_vectors_by_month = retrieve_by_period("%Y-%m", images_by_time)

    return project_clip_vectors, avg_clip_vectors_by_month[0]


def main():
    increment = args[0].INCREMENT

    if increment == "day":
        period = "%Y-%m-%d"
    elif increment == "month":
        period = "%Y-%m"
    elif increment == "year":
        period = "%Y"

    main_project_clip_vectors, main_project_clip_vectors_by_period = get_clip_vectors(
        args[0].ROBOFLOW_PROJECT,
        period=period,
    )
    drift_project_clip_vectors, drift_project_clip_vectors_by_period = get_clip_vectors(
        args[0].DRIFT_PROJECT, period=period, is_drift=True
    )

    avg_val_main_clip_vectors = [
        sum(x) / len(x) for x in zip(*main_project_clip_vectors)
    ]

    by_month = []

    for time_period in main_project_clip_vectors_by_period:
        drift_vectors = drift_project_clip_vectors_by_period[time_period]

        by_month.append(
            [
                time_period,
                cosine_similarity([drift_vectors[0]], [avg_val_main_clip_vectors])[0],
            ]
        )

    avg_drift_vectors = [sum(x) / len(x) for x in zip(*drift_project_clip_vectors)]
    avg_main_vectors = [sum(x) / len(x) for x in zip(*main_project_clip_vectors)]

    by_month.append(
        ["All Time", cosine_similarity([avg_drift_vectors], [avg_main_vectors])[0]]
    )

    print(tabulate.tabulate(by_month, headers=["Month", "Cosine Similarity"]))


if __name__ == "__main__":
    main()