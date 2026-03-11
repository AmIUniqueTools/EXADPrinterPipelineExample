import os
import zipfile
import json
import pickle
import hashlib
from fingerprint_parser.shell_attributes_parser import ShellAttributeParser
from fingerprint_parser.sdk_attributes_parser import SdkAttributeParser
from fingerprint_parser.cp_attributes_parser import CpAttributeParser

INPUT_FILE_PATH="DUMMY_DATA/1afe3e42-8731-4c44-9e09-ebd276ed0e62_1773071323547.zip"
INPUT_FILE_NAME="1afe3e42-8731-4c44-9e09-ebd276ed0e62_1773071323547.zip"

def load_json_file(file_path):
    """Helper function to load JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

# Hash the sdk structure
def hash_sdk_structure(l):
    return hashlib.sha256(pickle.dumps(l)).hexdigest()

def check_device_virtual(data):
    """
    Check if the device is virtual (emulator or virtual machine) based on build properties.
    """
    is_device_virtual = False

    # Convert properties to lowercase for case-insensitive checks
    manufacturer = str(data.get("android.os.Build.MANUFACTURER", "")).lower()
    model = str(data.get("android.os.Build.MODEL", "")).lower()
    hardware = str(data.get("android.os.Build.HARDWARE", "")).lower()
    fingerprint = str(data.get("android.os.Build.FINGERPRINT", "")).lower()
    product = str(data.get("android.os.Build.PRODUCT", "")).lower()
    board = str(data.get("android.os.Build.BOARD", "")).lower()
    brand = str(data.get("android.os.Build.BRAND", "")).lower()
    device = str(data.get("android.os.Build.DEVICE", "")).lower()
    kernel = str(data.get("kernel_information", "")).lower()
    system_logs = str(data.get("system_logs", "")).lower()
    
    virtual_flags = ["vbox", "virtual", "qemu", "vmware", "hypervisor", "kvm", "xen", "bochs", "nox"]
    # Check conditions for emulator or virtual machine
    is_emulator = (
        "genymotion" in manufacturer
        or "google_sdk" in model
        or "droid4x" in model
        or "emulator" in model
        or "android sdk built for x86" in model
        or hardware == "goldfish"
        or hardware == "vbox86"
        or "nox" in hardware
        or fingerprint.startswith("generic")
        or product in ["sdk", "google_sdk", "sdk_x86", "vbox86p"]
        or "nox" in product
        or "nox" in board
        or (brand.startswith("generic") and device.startswith("generic"))
        or "x86" in kernel 
        or "amd64" in kernel
        or any(flag in system_logs for flag in virtual_flags)
    )

    is_device_virtual = is_emulator

    return is_device_virtual

def preapre_fingerprint(data, filename):
    cleaned_data = {}
    is_incomplete = True
    suffix = ".ANDROID_ID"
    uuid,timestamp = filename.split("_")
    timestamp = int(timestamp.split(".")[0])
    sdk_structure = set()
    for item in data:
        # Check the first (and only) key-value pair in the dictionary
        for key, value in item.items():
            # Mark as complete if a key ends with the required suffix
            if key.endswith(suffix):
                is_incomplete = False
                
            # Parse shell attributes
            if ShellAttributeParser.isShellAttribute(key):
                value = ShellAttributeParser.parse(key, value, timestamp)
                # add it to cleaned data
                if value : 
                    if key == "ringtones_list_ext":
                        key = "ringtones_list"
                    # Flatten if is a dict
                    if isinstance(value, dict):
                        for k,v in value.items():
                            cleaned_data[f"{key}.{k}"] = v
                    elif isinstance(value, list):
                        if len(value)> 0 and len(value) == 1:
                            cleaned_data[key] = value[0]
                        elif len(value)>0 : 
                            cleaned_data[key] = value
                    else: 
                        cleaned_data[key] = value
            elif SdkAttributeParser.isSdkAttribute(key):
                # For SDK attributes, keep the nbSdk and SDK Structure
                sdk_structure.add(key)
                # Parse using SdkAttributeParser
                value = SdkAttributeParser.parse(key, value)
                # add it to cleaned data
                if value :
                    # Flatten if is a dict
                    if isinstance(value, dict):
                        for k,v in value.items():
                            cleaned_data[f"{key}.{k}"] = v
                    elif isinstance(value, list):
                        if len(value)> 0 and len(value) == 1:
                            cleaned_data[key] = value[0]
                        elif len(value)>0 : 
                            cleaned_data[key] = value
                    else: 
                        cleaned_data[key] = value
            elif CpAttributeParser.isCpAttribute(key):
                value = CpAttributeParser.parse(key,value)
                if value: 
                    # Flatten if is a dict
                    if isinstance(value, dict):
                        for k,v in value.items():
                            cleaned_data[f"{key}.{k}"] = v
                    elif isinstance(value, list):
                        if len(value)> 0 and len(value) == 1:
                            cleaned_data[key] = value[0]
                        elif len(value)>0 : 
                            cleaned_data[key] = value
                    else: 
                        cleaned_data[key] = value
            else: 
                cleaned_data[key] = value
            break # contains only one key-value pair in each dictionary
    # Return empty list if no complete fingerprints are found
    if is_incomplete : 
        return {}
    
    sdk_structure = sorted(list(sdk_structure))
    cleaned_data["structureSdk"] = hash_sdk_structure(sdk_structure)
    cleaned_data["nbSdk"] = len(sdk_structure)
    cleaned_data["timestamp"] = timestamp
    cleaned_data["uuid"] = uuid
    cleaned_data["isDeviceVirtual"] = check_device_virtual(cleaned_data)
    if "isDeviceRooted" not in cleaned_data:
        cleaned_data["isDeviceRooted"] = "unknown"
    if "isDeveloperModeEnabled" not in cleaned_data:
        cleaned_data["isDeveloperModeEnabled"] = -1 # means unknown
    
    # save the sdk structure 
    print(f"This fingerprint contains {len(sdk_structure)} SDK APIs")
    
    return cleaned_data


def extract_and_clean_archive(filename,file_path):
    """
    Extract archive, clean the JSON data,
    """
    cleaned_data_size = 0
    data_size = 0
    
    # Check if the file is a zip archive
    if filename.endswith('.zip'):  
        # Extract the archive
        with zipfile.ZipFile(file_path, 'r') as archive:
            # Check if data.json is in the archive
            if 'data.json' in archive.namelist():
                archive.extract('data.json', "./")
                # Load and clean the JSON data
                json_file_path = os.path.join('data.json')
                with open(json_file_path, 'r') as json_file:
                    data = json.load(json_file)
                    cleaned_data = preapre_fingerprint(data,filename)
                    if cleaned_data:
                        data_size = len(data)
                        cleaned_data_size = len(cleaned_data)
                        print(f"Processed '{filename}'")
                    
                    # Remove the extracted data.json file
                    os.remove(json_file_path)
    
    print(f"Original data size : {data_size} attributes") 
    print(f"Cleaned data size : {cleaned_data_size} attributes") 
    

extract_and_clean_archive(INPUT_FILE_NAME,INPUT_FILE_PATH)
   