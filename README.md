![Roboflow Collect banner](https://media.roboflow.com/collect/rf-collect.jpg?updatedAt=1680885477994)

# Roboflow Collect

An application through which you can passively collect image data at a specified interval and send your data to the Roboflow platform.

Roboflow Collect also provides a mechanism through which you can measure data drift in your dataset.

Read the [project documentation](https://roboflow.github.io/roboflow-collect/) for the full installation and setup tutorial.

## Use Cases

Roboflow Collect enables:

- Passive data collection to help you start building a dataset for a new computer vision model.
- Collecting data using edge devices to expand an existing dataset.
- Gathering more representative data for edge cases in your dataset.

In tandem with custom tags on the Roboflow platform, described below, you can use Roboflow Collect to collect data that is semantically related to specific images in your dataset. This will help you make your model more robust to edge cases.

You can deploy Roboflow Collect on edge devices with an attached webcam. You need to be able to run a Docker container on the device. For instance, you can run Roboflow Collect on:

1. A Raspberry Pi
2. An NVIDIA Jetson
3. A macOS device (ideal for testing)

## Contributing

Have feedback on how we can improve Roboflow Collect? Found a bug? Leave an issue in the project Issues. We will review your Issue and get back to you promptly.

## License

This project is licensed under an [MIT License](LICENSE).

[^1]: The timer starts after evaluation. Thus, if a photo takes a second to evaluate, a one second timer will mean a photo will be taken every two seconds: one second will pass for the delay, and another will pass during evaluation.
