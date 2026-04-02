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
@article{bouhenniche2026exadprinter,
  author  = {Bouhenniche Sihem, Laperdrix Pierre, Rudametkin Walter },
  title   = {EXADPrinter: Semi-Exhaustive Permissionless Device Fingerprinting Within the Android Ecosystem},
  journal = {Proceedings on Privacy Enhancing Technologies},
  year    = {2026},
  note    = {To appear (PETS 2026)}
}
```

---

# Repository Structure

```
.
├── DUMMY_DATA/                   # Browserstack devices fingerprints
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

The repository provides a **dummy dataset collected on real Android devices available through the [BrowserStack](https://www.browserstack.com/) platform**.
The dummy dataset contains **22** fingerprints collected from **11** devices, and is intended to:

* demonstrate the expected fingerprint format
* allow testing of the parsing and cleaning pipeline

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

- Create BrowserStack account at [https://www.browserstack.com/](https://www.browserstack.com/) (a free trial provides **100 minutes of Automate testing**).
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
- Install [`jq`](https://jqlang.org/download/) then edit [`DataCollectionSetup/pipeline.sh`](DataCollectionSetup/pipeline.sh) by providing the following variables:

```
API_BASE_RL=
APP_URL=
BROWSERSTACK_USERNAME=
BROWSERSTACK_ACCESS_KEY=
```

Where:

* `API_BASE_URL` is the server receiving fingerprints, if no API_BASE_URL is provided fingerprints will be sent to our servers.
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
4. send fingerprints to your server. To do so, your must implement `<YOUR_SERVER_URL>/saveStructure/` API endpoint and expect a **POST request** containing
* a **fingerprint file** (sent as `file`)
* a **device identifier** (sent as `uuid`)
The endpoint response should follow the schema below:
```json
  UploadResponse {
    message: String
    downloadUrl: String
    fileName: String
  }
```

The list of devices used during the experiment is defined in [`capabilities.json`](DataCollectionSetup/capabilities.json). The file currently contains 10 device configurations. Additional devices can be added by following the BrowserStack capabilities documentation: [https://www.browserstack.com/docs/app-automate/capabilities](https://www.browserstack.com/docs/app-automate/capabilities)

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

