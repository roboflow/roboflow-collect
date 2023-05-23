## Measuring Data Drift

Data drift refers in changes to the information in your project dataset over time. This can happen intentionally as a result of changing the scope of your model (i.e. adding a new class to identify, which requires gathering information in a new environment), but can also happen unintentionally (i.e. as a result of adding a camera to collect images in an environment different from that where your model is operating).

To measure data drift, first create a new project in Roboflow. Then, provide the ID associated with that project as the `DRIFT_PROJECT` documented above in the `Configure Roboflow Collect` documentation.

For each frame gathered by Roboflow Collect, there is a 1 in 100 chance that image will be uploaded to your `DRIFT_PROJECT`.

The `drift.py` script measures the difference between the average CLIP vector in your `DRIFT_PROJECT` versus the average CLIP vector for all images in the validation set of your `ROBOFLOW_PROJECT`.

After gathering some data from Roboflow Collect, run the `drift.py` script with these arguments:

```
python3.9 drift.py --ROBOFLOW_KEY=Cu7ojo7vihCtOYAUa6gd --ROBOFLOW_WORKSPACE=roboflow-universe-projects --ROBOFLOW_PROJECT=basketball-players-fy4c2 --DRIFT_PROJECT=taco-object-detection-kcxyn
```

Where `ROBOFLOW_PROJECT` is the main project in which you are gathering data, and `DRIFT_PROJECT` is where you are randomly collecting images.

This script will return a table showing data drift for each month for which data is available, as well as an aggregate score showing how similar images are between your `ROBOFLOW_PROJECT` and the images collected via Roboflow Collect and saved in the `DRIFT_PROJECT`.