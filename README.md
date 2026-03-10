# EXADPrinter Pipeline Example

This repository provides a **minimal example pipeline for processing Android device fingerprints collected with EXADPrinter**.

It accompanies the paper:

**EXADPrinter: Semi-Exhaustive Permissionless Device Fingerprinting Within the Android Ecosystem** (PETS 2026)

The repository demonstrates how to:

* parse collected fingerprints
* clean and normalize attributes
* inspect the fingerprint structure
* run a small example data collection pipeline

To preserve user privacy, the repository **does not contain the original datasets used in the paper**, but includes **dummy datasets** that reproduce the expected data format.

### Citation

If you use this artifact in your research, please cite:

```

```

---

# Repository Structure

```
.
├── DUMMY_DATA/                   # Example raw fingerprints
├── DUMMY_DATA_PREPARED/          # Cleaned example fingerprints
├── DUMMY_DATA_STRUCTURE/         # Extracted fingerprint structure
├── fingerprint_parser/           # Python module for parsing attributes
├── data_cleaning_pipeline.ipynb  # Notebook demonstrating cleaning pipeline
├── DataCollectionSetup/          # Example automation pipeline
└── requirements.txt              # Python dependencies
```

---

# Requirements

Tested on:

* Ubuntu 20.04+
* Python 3.13
* pip

Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

# Using the Dummy Dataset

The repository provides a **small dummy dataset** collected from a limited number of Android devices.

The dataset is intended to:

* demonstrate the expected fingerprint format
* allow testing of the parsing and cleaning pipeline
* reproduce the workflow described in the paper

Run the cleaning notebook:

```bash
jupyter notebook data_cleaning_pipeline.ipynb
```

The notebook will:

1. load fingerprints from `DUMMY_DATA`
2. parse attributes using `fingerprint_parser`
3. apply cleaning rules
4. generate processed fingerprints in:

```
DUMMY_DATA_PREPARED/
DUMMY_DATA_STRUCTURE/
```

---

# Running a Data Collection Example (Optional)

*This step is optional and not required to evaluate the artifact. The repository already contains dummy datasets that allow testing the full processing pipeline.*

Instead of using the dummy dataset, you can run a **small fingerprint collection experiment** using the provided automation pipeline.

This example uses **BrowserStack real Android devices**. Official documentation for the BrowserStack App Automate service can be found [here](https://www.browserstack.com/docs/app-automate/appium/getting-started/python/pytest?fw-lang=python%2Fpytest).

### 1. Create a BrowserStack account

- Create an account on: https://www.browserstack.com/
- You will need your BrowserStack credentials to run the automation pipeline.
- You can retrieve them from your account dashboard: [https://www.browserstack.com/accounts/settings](https://www.browserstack.com/accounts/settings)
- These values correspond to:
```
BROWSERSTACK_USERNAME
BROWSERSTACK_ACCESS_KEY
```

For more information, check the documentation: [https://www.browserstack.com/docs/app-automate/appium/getting-started/python/pytest#configure-browserstack-credentials](https://www.browserstack.com/docs/app-automate/appium/getting-started/python/pytest#configure-browserstack-credentials)

### 2. Upload the application to BrowserStack
Before running the automation, you must upload the [EXADPrinter demo application](./DataCollectionSetup/exadprinterDemoApp.apk).

- Upload the APK using the BrowserStack API as described here: [https://www.browserstack.com/docs/app-automate/appium/set-up-test-env/upload-and-manage-apps](https://www.browserstack.com/docs/app-automate/appium/set-up-test-env/upload-and-manage-apps?fw-lang=python%2Fpytest)
- After uploading the application, BrowserStack will return an app URL similar to:
```
bs://<app-id>
```
- This value should be used fo `APP_URL` later.

### 3. Configure the pipeline

Edit:

```
DataCollectionSetup/pipeline.sh
```

Provide the following variables:

```
API_BASE_RL=
APP_URL=
BROWSERSTACK_USERNAME=
BROWSERSTACK_ACCESS_KEY=
```

Where:

* `API_BASE_RL` is the server receiving fingerprints, if no API_END_POINT is provided fingerprints will be sent to our servers.
* `APP_URL` is the URL of the `exadprinterDemoApp.apk`
* `BROWSERSTACK_USERNAME` and `BROWSERSTACK_ACCESS_KEY` are your BrowserStack credentials

### 4. Run the pipeline

```bash
./pipeline.sh
```

The script will:

1. create BrowserStack sessions
2. install the EXADPrinter demo application
3. run fingerprint collection
4. send fingerprints to the configured API endpoint (check [FingerprintApi.kt](https://github.com/AmIUniqueTools/AmIUniqueApp/blob/main/app/src/main/java/com/amiunique/amiuniqueapp/network/FingerprintApi.kt) for the expected endpoint schema schema )

---

# Related Repositories

This repository is part of the **EXADPrinter artifact ecosystem**.

### Android fingerprinting library

[https://github.com/AmIUniqueTools/AmIUniqueApp](https://github.com/AmIUniqueTools/AmIUniqueApp)

Contains:

* the **EXADPrinter Android library**
* the **AmIUnique Android application**

---

# Dataset Availability

The **original dataset collected from real participants is not publicly available** due to privacy and ethical considerations.

Instead, this repository includes:

* a **small dummy dataset**
* the **full processing pipeline**
* the **complete data collection framework**

---

# License

This project is released under the license specified in the repository.

