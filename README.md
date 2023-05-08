![Roboflow Collect banner](https://media.roboflow.com/collect/rf-collect.jpg?updatedAt=1680885477994)

# Roboflow Collect

An application through which you can passively collect image data at a specified interval and send your data to the Roboflow platform.

## Use Cases

Roboflow Collect enables:

- Passive data collection to help you start building a dataset for a new computer vision model.
- Collecting data using edge devices to expand an existing dataset.
- Gathering more representative data for edge cases in your dataset.

In tandem with custom tags on the Roboflow platform, described below, you can use Roboflow Collect to collect data that is semantically related to specific images in your dataset. This will help you make your model more robust to edge cases.

You can deploy Roboflow Collect on any device that can run Docker and that has an attached webcam. For instance, you can run Roboflow Collect on:

1. A Raspberry Pi
2. An NVIDIA Jetson

## Manual Installation

To install Roboflow Collect manually, run the following commands:

```
git clone https://github.com/roboflow/roboflow-collect
pip3 install -r requirements.txt
```

### Configure Inference Server

If you already have a Roboflow inference server running locally, you can skip to the next step. Otherwise, install the Roboflow inference server and start it using these commands:

#### CPU

```
sudo docker pull roboflow/roboflow-inference-server-arm-cpu:latest
sudo docker run --net=host roboflow/roboflow-inference-server-arm-cpu:latest
```

#### Jetson GPU

```
sudo docker pull roboflow/roboflow-inference-server-arm-cpu:latest
sudo docker run --net=host roboflow/roboflow-inference-server-arm-cpu:latest
```

### Configure Roboflow Collect

Then, set the following values in your environment: 

- `ROBOFLOW_PROJECT` is the name of the project to which you want to upload your data.
- `ROBOFLOW_WORKSPACE` is the name of the workspace to which you want to upload your data.
- `ROBOFLOW_KEY` is your Roboflow API key.
- `SAMPLE_RATE` is the number of seconds between each image capture. For example, if you set `SAMPLE_RATE` to `1`, then Roboflow Collect will capture an image every second.
- `INFER_SERVER_DESTINATION` is the URL of the inference server to which you want to send your images. If you install using Docker, leave this value as it is in the example `docker-compose.yml` file.
- `COLLECT_ALL` is a boolean value that determines whether Roboflow Collect will collect all images or only images that are tagged with a custom tag. If you set `COLLECT_ALL` to `True`, then Roboflow Collect will collect all images. If you set `COLLECT_ALL` to `False`, then Roboflow Collect will only collect images related to the ones in your Roboflow dataset that are tagged with a custom tag.
- `STREAM_URL` is the URL of the video stream from which you want to collect images. If you are not using a video stream, you can leave this value as is and Roboflow Collect will use your webcam. Only YouTube video streams are supported at this time.

Here is an example configuration for a project that will collect an image to evaluate (approximately [^1]) once every second:

```
export ROBOFLOW_PROJECT=""
export ROBOFLOW_WORKSPACE=""
export ROBOFLOW_KEY=""
export SAMPLE_RATE=1
export COLLECT_ALL=True
```

### Run the Application

To start using Roboflow Collect, run this command:

```
python3 app.py
```

## Installation with Docker (WIP)

*Note: This installation system is a work-in-progress.*

First, ensure you have Docker installed on your edge device. Next, clone this GitHub repository:

```
git clone https://github.com/roboflow/roboflow-collect
```

Next, you will need to collect your Roboflow API key and the workspace name and ID of the workspace to which you want to upload your data. You can learn how to find these values in [our documentation](https://docs.roboflow.com/rest-api#how-to-find-your-model-id-and-version).

Open the `docker-compose.yml` file in this repository and replace the "Configuration Options" documented in the manual installation section with the values required for your project.

Next, build the Roboflow Collect image:

```
docker build -t roboflow-collect .
```

Finally, run the following command to start Roboflow Collect:

```
docker compose up
```

## CLIP Semantic Similarity Configuration

Roboflow Collect can collect images that are semantically similar to either:

1. A CLIP prompt
2. Another image in a Roboflow-hosted dataset

You can use this to focus Collect on only images that are relevant to your project.

### CLIP Prompt

To collect images that are similar to a CLIP prompt, set the following configuration value in your environment or `docker-compose.yml` file:

```
CLIP_TEXT_PROMPT=train
```

This prompt will only collect images whose CLIP vector is similar to the vector for the term `train`.

### Roboflow Hosted Images

To collect images similar to an image on Roboflow, go to the `Dataset` section of your dataset. Then, click on an image to go into annotation mode.

You will need to create three new tags in the `Tags` editor in the annotation interface. Here are the tags you need to add:

- `sample-more`
- `sample-threshold:80`: Only select images that are 80 percent similar to the image to which you have affixed the tag. You can use any percentage value.
- `sample-tag:train-rf-collect`: Adds the tag `train-rf-collect` to any image that is uploaded by Roboflow Collect that meets the rule. You can set any text value for the tag.

## Contributing

Have feedback on how we can improve Roboflow Collect? Found a bug? Leave an issue in the project Issues. We will review your Issue and get back to you promptly.

## License

This project is licensed under an [MIT License](LICENSE).

[^1]: The timer starts after evaluation. Thus, if a photo takes a second to evaluate, a one second timer will mean a photo will be taken every two seconds: one second will pass for the delay, and another will pass during evaluation.
