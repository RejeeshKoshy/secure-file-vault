# Module-4: ML-Based File Risk Detector

## Overview

This module implements a machine learning–based file risk detector for the Secure File Vault project.
It classifies files as **safe** or **risky** based on extracted features like size, entropy, extension, and MIME type.

---

## Contents

* `extract_features.py`: Extracts numerical and categorical features from files
* `generate_dataset.py`: Builds a CSV dataset from sample files for training
* `train_model.py`: Trains a Random Forest classifier using the dataset
* `evaluate_model.py`: Evaluates the trained model, outputs classification report, and saves performance plots (confusion matrix, ROC curve)
* `predict_file.py`: Predicts risk for a single file using the trained model
* `streamlit_app.py`: Streamlit-based interactive UI to upload files and see risk prediction
* `data/dataset.csv`: Example dataset file
* `model/`: Contains saved ML model and encoders
* `plots/`: Contains saved evaluation plots

---

## Setup Instructions

1. Create and activate a Python virtual environment (recommended)

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Generate dataset from test files (optional if dataset already present):

   ```
   python generate_dataset.py
   ```

4. Train the model:

   ```
   python train_model.py
   ```

5. Evaluate model performance:

   ```
   python evaluate_model.py
   ```

6. Run the interactive Streamlit UI:

   ```
   streamlit run streamlit_app.py
   ```

7. Predict a single file risk from command line:

   ```
   python predict_file.py <file_path>
   ```

---

## Notes

* This module is currently designed for offline/experimental use and should not be used in production without further testing and refinement.
* The dataset and model are basic and intended as a starting point.
* Additional features, larger datasets, and advanced models are recommended for improved accuracy.
