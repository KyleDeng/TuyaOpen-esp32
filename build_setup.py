#!/usr/bin/env python3
# coding=utf-8

import sys
import os

from tools.util import copy_file, record_target, execute_idf_commands
from tools.prepare import platform_prepare, delete_temp_files


SUPPORT_CHIPS = [
    "esp32",
    "esp32c3",
    "esp32s3",
]


def need_setup(root) -> bool:
    '''
    1. sdkconfig.h file exists: no need to be regenerated
    2. Delete the build directory before generation sdkconfig.h
    '''
    build_path = os.path.join(root, "tuya_open_sdk", "build")
    sdkconfig = os.path.join(build_path,
                             "config", "sdkconfig.h")
    if os.path.isfile(sdkconfig):
        return False

    return True


def setup_some_files(root, chip) -> bool:
    delete_temp_files(root)

    tuya_path = os.path.join(root, "tuya_open_sdk")
    sdk_config = os.path.join(tuya_path, f"sdkconfig_{chip}")
    sdk_config_default = os.path.join(tuya_path, "sdkconfig.defaults")
    return copy_file(sdk_config, sdk_config_default)


def setup(root, chip):
    '''
    1. Generate the sdkconfig.h file before the first build
    use: idf.py set-target xxx
    '''
    cmd = f"idf.py set-target {chip}"
    directory = os.path.join(root, "tuya_open_sdk")
    return execute_idf_commands(root, cmd, directory)


def main():
    if len(sys.argv) < 5:
        print(f"Error: At least 4 parameters are needed {sys.argv}.")
    project_name = sys.argv[1]
    platform = sys.argv[2]
    framework = sys.argv[3]
    chip = sys.argv[4]
    print(f'''project_name: ${project_name}
platform: {platform}
framework: {framework}
chip: {chip}''')

    if chip not in SUPPORT_CHIPS:
        print(f"Error: {chip} is not supported.")
        sys.exit(1)

    root = os.path.dirname(os.path.abspath(__file__))

    # prepare first
    if not platform_prepare(root, chip):
        sys.exit(1)

    if not need_setup(root):
        print("No need setup.")
        sys.exit(0)

    if not setup_some_files(root, chip):
        print("Error: setup some files.")
        sys.exit(1)

    if not setup(root, chip):
        print("Error: setup.")
        sys.exit(1)

    # When build_example.sh need set-target again
    target_file = os.path.join(root, ".target")
    record_target(target_file, "need-set-target")

    sys.exit(0)


if __name__ == "__main__":
    main()
