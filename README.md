![Roboflow Collect banner](https://media.roboflow.com/collect/rf-collect.jpg?updatedAt=1680885477994)

# Roboflow Collect

A Docker container through which you can passively collect image data at a specified interval and send your data to the Roboflow platform.

## Use Cases

Roboflow Collect enables:

- Passive data collection to help you start building a dataset for a new computer vision model.
- Collecting data using edge devices to expand an existing dataset.
- Gathering more representative data for edge cases in your dataset.

In tandem with custom tags on the Roboflow platform, described below, you can use Roboflow Collect to collect data that is semantically related to specific images in your dataset. This will help you make your model more robust to edge cases.

You can deploy Roboflow Collect on any device that can run Docker and that has an attached webcam. For instance, you can run Roboflow Collect on:

1. A Raspberry Pi
2. An NVIDIA Jetson

## Installation with Docker

First, ensure you have Docker installed on your edge device. Next, clone this GitHub repository:

```
git clone https://github.com/roboflow/roboflow-collect
```

Next, you will need to collect your Roboflow API key and the workspace name and ID of the workspace to which you want to upload your data. You can learn how to find these values in [our documentation](https://docs.roboflow.com/rest-api#how-to-find-your-model-id-and-version).

Open the `docker-compose.yml` file in this repository and replace the following values with your own:

- `ROBOFLOW_PROJECT` is the name of the project to which you want to upload your data.
- `ROBOFLOW_WORKSPACE` is the name of the workspace to which you want to upload your data.
- `ROBOFLOW_KEY` is your Roboflow API key.
- `SAMPLE_RATE` is the number of seconds between each image capture. For example, if you set `SAMPLE_RATE` to `1`, then Roboflow Collect will capture an image every second.
- `INFER_SERVER_DESTINATION` is the URL of the inference server to which you want to send your images. If you are not using an inference server, you can leave this value as is.
- `COLLECT_ALL` is a boolean value that determines whether Roboflow Collect will collect all images or only images that are tagged with a custom tag. If you set `COLLECT_ALL` to `True`, then Roboflow Collect will collect all images. If you set `COLLECT_ALL` to `False`, then Roboflow Collect will only collect images related to the ones in your Roboflow dataset that are tagged with a custom tag.
- `STREAM_URL` is the URL of the video stream from which you want to collect images. If you are not using a video stream, you can leave this value as is and Roboflow Collect will use your webcam.

Next, build the Roboflow Collect image:

```
docker build -t roboflow-collect .
```

Finally, run the following command to start Roboflow Collect:

```
docker compose up
```

## Contributing

Have feedback on how we can improve Roboflow Collect? Found a bug? Leave an issue in the project Issues. We will review your Issue and get back to you promptly.

## License

This project is licensed under an [MIT License](LICENSE).
