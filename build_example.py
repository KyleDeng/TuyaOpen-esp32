#!/usr/bin/env python3
# coding=utf-8
# 参数说明：
# $1 - params path: $1/build_param.[cmake/config/json]
# $2 - user cmd: build/clean/...

import os
import sys
import json

from tools.util import (
    copy_file, need_settarget,
    record_target, set_target,
    execute_idf_commands
)
from tools.prepare import delete_temp_files


def clean(root):
    delete_temp_files(root)
    pass


def parser_para_file(json_file):
    if not os.path.isfile(json_file):
        print(f"Error: Not found [{json_file}].")
        return {}
    try:
        f = open(json_file, 'r', encoding='utf-8')
        json_data = json.load(f)
        f.close()
    except Exception as e:
        print(f"Parser json error:  [{str(e)}].")
        return {}
    return json_data


def set_environment(build_param_path, param_data):
    os.environ["BUILD_PARAM_DIR"] = build_param_path
    os.environ["TUYAOS_HEADER_DIR"] = param_data["OPEN_HEADER_DIR"]
    os.environ["TUYAOS_LIBS_DIR"] = param_data["OPEN_LIBS_DIR"]
    os.environ["TUYAOS_LIBS"] = param_data["PLATFORM_NEED_LIBS"]
    open_root = param_data["OPEN_ROOT"]
    board_path = os.path.join(open_root, "boards", "ESP32")
    os.environ["TUYAOS_BOARD_PATH"] = board_path
    pass


def set_partitions(root, param_data):
    if param_data.get("CONFIG_PLATFORM_FLASHSIZE_16M", False):
        flash = "16M"
    elif param_data.get("CONFIG_PLATFORM_FLASHSIZE_8M", False):
        flash = "8M"
    else:
        flash = "4M"

    print(f"Set flash size {flash}")
    tuya_path = os.path.join(root, "tuya_open_sdk")
    source = os.path.join(tuya_path, f"partitions_{flash}.csv")
    target = os.path.join(tuya_path, "partitions.csv")
    copy_file(source, target)
    pass


def main():
    '''
    1. 调用idf.py生成固件
    2. 提前配置一些环境变量
    3. 如果编译的项目变化，则清理现场并set-target
    4. 如果target变化，则清理现场并set-target
    5. 配置正确的partitions.csv
    '''
    if len(sys.argv) < 2:
        print(f"Error: At least 2 parameters are needed {sys.argv}.")
    build_param_path = sys.argv[1]
    user_cmd = sys.argv[2]
    root = os.path.dirname(os.path.abspath(__file__))
    if "clean" == user_cmd:
        clean(root)
        sys.exit(0)

    build_param_file = os.path.join(build_param_path, "build_param.json")
    param_data = parser_para_file(build_param_file)
    if not len(param_data):
        sys.exit(1)

    # Set environment variables
    set_environment(build_param_path, param_data)

    # check app / check target
    app_file = os.path.join(root, ".app")
    target_file = os.path.join(root, ".target")
    app_name = param_data["CONFIG_PROJECT_NAME"]
    chip = param_data["PLATFORM_CHIP"]
    if need_settarget(app_file, app_name) or need_settarget(target_file, chip):
        clean(root)
        if not set_target(root, chip):
            print("Error: set-target failed.")
            sys.exit(1)
    record_target(app_file, app_name)
    record_target(target_file, chip)

    set_partitions(root, param_data)

    cmd = "idf.py build"
    directory = os.path.join(root, "tuya_open_sdk")
    if not execute_idf_commands(root, cmd, directory):
        print("Error: Build failed.")
        sys.exit(1)

    app_version = param_data["CONFIG_PROJECT_VERSION"]
    print(f"Start generate {app_name}_QIO_{app_version}.bin")

    sys.exit(0)


if __name__ == "__main__":
    main()
