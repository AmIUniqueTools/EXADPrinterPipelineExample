#!/bin/bash

# Define device brand patterns for each Android version
CAPABILITIES_FILE="capabilities.json"
API_END_POINT="API_END_POINT"

# Requirements: jq must be installed
command -v jq >/dev/null 2>&1 || { echo "jq is required. Install it first."; exit 1; }

# Replace env from .env
# Upload manually the `exadprinterDemoApp.apk` and get URL
APP_URL="APP_URL"

# Get your BrowserStack credentials
BROWSERSTACK_USERNAME="BROWSERSTACK_USERNAME"
BROWSERSTACK_ACCESS_KEY="BROWSERSTACK_ACCESS_KEY"

# Configure project and build
project="BrowserStack EXADPrinter Test"
buildTemplate="bstack-fingerprint-test"

jq -c '.[]' "$CAPABILITIES_FILE" | while read -r cap; do
  deviceName="$(jq -r '.deviceName' <<< "$cap")"
  platformVersion="$(jq -r '.platformVersion' <<< "$cap")"
  platformName="$(jq -r '.platformName' <<< "$cap")"

  echo "▶ Select $deviceName (Android $platformVersion)"

  buildIdentifier="$(echo "$deviceName-$platformVersion-$i" | tr ' /' '__')"

  # Generate browserstack.yml (ONE DEVICE)
  cat > browserstack.yml <<EOL
userName: $BROWSERSTACK_USERNAME
accessKey: $BROWSERSTACK_ACCESS_KEY
projectName: $project
buildName: $buildTemplate
buildIdentifier: "$buildIdentifier"
framework: pytest
app: $APP_URL
browserstackLocal: false
deviceLogs: false
appiumLogs: false 
platforms:
  - platformName: $platformName
    deviceName: "$deviceName"
    platformVersion: "$platformVersion"
    appium:optionalIntentArguments: '--es API_END_POINT "$API_END_POINT"'
EOL

  echo "🚀 Running test on $deviceName (Android $platformVersion)"
  browserstack-sdk pytest -s test_app.py
  echo "✅ Done: $deviceName"

  rm -f browserstack.yml
  # Comment the exit 1 line if want to run all iterations
  done
done