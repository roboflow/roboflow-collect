![Roboflow Collect banner](https://media.roboflow.com/collect/rf-collect.jpg?updatedAt=1680885477994)

# Roboflow Collect

An application through which you can passively collect image data at a specified interval and send your data to the Roboflow platform.

Roboflow Collect also provides a mechanism through which you can measure data drift in your dataset.

Read the [project documentation](https://roboflow.github.io/roboflow-collect/) for the full installation and setup tutorial.

Read [Collect Images at the Edge with Roboflow Collect](https://blog.roboflow.com/roboflow-collect/) for a complete guide on how to use Collect.

https://github.com/roboflow/roboflow-collect/assets/37276661/5fcc17b8-3dca-4570-9a3c-ba3b28c8a114

## 💡 Use Cases

Roboflow Collect enables:

- Passive data collection to help you start building a dataset for a new computer vision model.
- Collecting data using edge devices to expand an existing dataset.
- Gathering more representative data for edge cases in your dataset.

In tandem with custom tags on the Roboflow platform, described below, you can use Roboflow Collect to collect data that is semantically related to specific images in your dataset. This will help you make your model more robust to edge cases.

You can deploy Roboflow Collect on edge devices with an attached webcam. You need to be able to run a Docker container on the device. For instance, you can run Roboflow Collect on:

1. A Raspberry Pi
2. An NVIDIA Jetson
3. A macOS device (ideal for testing)

## 🏆 Contributing

Have feedback on how we can improve Roboflow Collect? Found a bug? Leave an issue in the project Issues. We will review your Issue and get back to you promptly.

## 📄 License

This project is licensed under an [MIT License](LICENSE).

[^1]: The timer starts after evaluation. Thus, if a photo takes a second to evaluate, a one second timer will mean a photo will be taken every two seconds: one second will pass for the delay, and another will pass during evaluation.

## 💻 explore more Roboflow open source projects

|Project | Description|
|:---|:---|
|[supervision](https://roboflow.com/supervision) | General-purpose utilities for use in computer vision projects, from predictions filtering and display to object tracking to model evaluation.
|[Autodistill](https://github.com/autodistill/autodistill) | Automatically label images for use in training computer vision models. |
|[Inference](https://github.com/roboflow/inference) | An easy-to-use, production-ready inference server for computer vision supporting deployment of many popular model architectures and fine-tuned models.
|[Notebooks](https://roboflow.com/notebooks) | Tutorials for computer vision tasks, from training state-of-the-art models to tracking objects to counting objects in a zone.
|[Collect](https://github.com/roboflow/roboflow-collect) (this project) | Automated, intelligent data collection powered by CLIP.

<br>

<div align="center">

  <div align="center">
      <a href="https://youtube.com/roboflow">
          <img
            src="https://media.roboflow.com/notebooks/template/icons/purple/youtube.png?ik-sdk-version=javascript-1.4.3&updatedAt=1672949634652"
            width="3%"
          />
      </a>
      <img src="https://raw.githubusercontent.com/ultralytics/assets/main/social/logo-transparent.png" width="3%"/>
      <a href="https://roboflow.com">
          <img
            src="https://media.roboflow.com/notebooks/template/icons/purple/roboflow-app.png?ik-sdk-version=javascript-1.4.3&updatedAt=1672949746649"
            width="3%"
          />
      </a>
      <img src="https://raw.githubusercontent.com/ultralytics/assets/main/social/logo-transparent.png" width="3%"/>
      <a href="https://www.linkedin.com/company/roboflow-ai/">
          <img
            src="https://media.roboflow.com/notebooks/template/icons/purple/linkedin.png?ik-sdk-version=javascript-1.4.3&updatedAt=1672949633691"
            width="3%"
          />
      </a>
      <img src="https://raw.githubusercontent.com/ultralytics/assets/main/social/logo-transparent.png" width="3%"/>
      <a href="https://docs.roboflow.com">
          <img
            src="https://media.roboflow.com/notebooks/template/icons/purple/knowledge.png?ik-sdk-version=javascript-1.4.3&updatedAt=1672949634511"
            width="3%"
          />
      </a>
      <img src="https://raw.githubusercontent.com/ultralytics/assets/main/social/logo-transparent.png" width="3%"/>
      <a href="https://disuss.roboflow.com">
          <img
            src="https://media.roboflow.com/notebooks/template/icons/purple/forum.png?ik-sdk-version=javascript-1.4.3&updatedAt=1672949633584"
            width="3%"
          />
      <img src="https://raw.githubusercontent.com/ultralytics/assets/main/social/logo-transparent.png" width="3%"/>
      <a href="https://blog.roboflow.com">
          <img
            src="https://media.roboflow.com/notebooks/template/icons/purple/blog.png?ik-sdk-version=javascript-1.4.3&updatedAt=1672949633605"
            width="3%"
          />
      </a>
      </a>
  </div>

</div>
