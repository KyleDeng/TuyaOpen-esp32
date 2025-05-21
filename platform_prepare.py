#!/usr/bin/env python3
# coding=utf-8

import sys
import os
import shutil
import subprocess
import requests
from git import Git


MIRROR_LIST = [
    "adafruit/asf4",
    "ARMmbed/mbed-os-cypress-capsense-button",
    "ARMmbed/mbed-os-posix-socket",
    "ARMmbed/mbed-os",
    "ARMmbed/mbedtls",
    "atgreen/libffi",
    "ATmobica/mcuboot",
    "bluekitchen/btstack",
    "DaveGamble/cJSON",
    "eclipse/tinydtls",
    "espressif/asio",
    "espressif/aws-iot-device-sdk-embedded-C",
    "espressif/connectedhomeip",
    "espressif/esp-adf",
    "espressif/esp-adf-libs",
    "espressif/esp-at",
    "espressif/esp-ble-mesh-lib",
    "espressif/esp-bootloader-plus",
    "espressif/esp-box",
    "espressif/esp-coex-lib",
    "espressif/esp-cryptoauthlib",
    "espressif/esp-dev-kits",
    "espressif/esp-dl",
    "espressif/esp-hosted",
    "espressif/esp-idf",
    "espressif/esp-idf-provisioning-ios",
    "espressif/esp-ieee802154-lib",
    "espressif/esp-insights",
    "espressif/esp-iot-bridge",
    "espressif/esp-iot-solution",
    "espressif/esp-lwip",
    "espressif/esp-matter",
    "espressif/esp-mesh-lite",
    "espressif/esp-mqtt",
    "espressif/esp-nimble",
    "espressif/esp-phy-lib",
    "espressif/esp-rainmaker",
    "espressif/esp-rainmaker-cli",
    "espressif/esp-rainmaker-common",
    "espressif/esp-rainmaker-ios",
    "espressif/esp-serial-flasher",
    "espressif/esp-sr",
    "espressif/esp-thread-lib",
    "espressif/esp-who",
    "espressif/esp32-bt-lib",
    "espressif/esp32-camera",
    "espressif/esp32-wifi-lib",
    "espressif/esp32c2-bt-lib",
    "espressif/esp32c3-bt-lib",
    "espressif/esp32c5-bt-lib",
    "espressif/esp32c6-bt-lib",
    "espressif/esp32h2-bt-lib",
    "espressif/esptool",
    "espressif/json_generator",
    "espressif/json_parser",
    "espressif/mbedtls",
    "espressif/openthread",
    "espressif/tinyusb",
    "espressif/tlsf",
    "FreeRTOS/FreeRTOS-Kernel",
    "google/boringssl",
    "google/pigweed",
    "h2o/neverbleed",
    "hathach/nxp_driver",
    "hathach/tinyusb",
    "Infineon/abstraction-rtos",
    "Infineon/anycloud-ota",
    "Infineon/bluetooth-freertos",
    "Infineon/btsdk-include",
    "Infineon/btsdk-tools",
    "Infineon/btstack",
    "Infineon/clib-support",
    "Infineon/connectivity-utilities",
    "Infineon/core-lib",
    "Infineon/core-make",
    "Infineon/freertos",
    "Infineon/kv-store",
    "Infineon/mtb-hal-cat1",
    "Infineon/mtb-pdl-cat1",
    "Infineon/ot-ifx-release",
    "Infineon/OT-Matter-30739A0",
    "Infineon/OT-Matter-TARGET_CYW930739M2EVB-01",
    "Infineon/psoc6cm0p",
    "Infineon/recipe-make-cat1a",
    "Infineon/retarget-io",
    "Infineon/secure-sockets",
    "Infineon/serial-flash",
    "Infineon/TARGET_CY8CKIT-062S2-43012",
    "Infineon/whd-bsp-integration",
    "Infineon/wifi-connection-manager",
    "Infineon/wifi-host-driver",
    "Infineon/wifi-mw-core",
    "intel/tinycbor",
    "jedisct1/libhydrogen",
    "jedisct1/libsodium",
    "jeremyjh/ESP32_TFT_library",
    "kmackay/micro-ecc",
    "leethomason/tinyxml2",
    "libexpat/libexpat",
    "lvgl/lvgl",
    "lwip-tcpip/lwip",
    "micropython/axtls",
    "micropython/micropython",
    "micropython/micropython-lib",
    "micropython/mynewt-nimble",
    "micropython/stm32lib",
    "matter-mtk/genio-matter-lwip",
    "matter-mtk/genio-matter-mdnsresponder",
    "mruby/mruby",
    "nayuki/QR-Code-generator",
    "nanopb/nanopb",
    "nestlabs/nlassert",
    "nestlabs/nlfaultinjection",
    "nestlabs/nlio",
    "nestlabs/nlunit-test",
    "nghttp2/nghttp2",
    "nodejs/http-parser",
    "obgm/libcoap",
    "ocornut/imgui",
    "open-source-parsers/jsoncpp",
    "openthread/ot-br-posix",
    "openthread/ot-nxp",
    "openthread/ot-qorvo",
    "openthread/openthread",
    "openweave/cirque",
    "pellepl/spiffs",
    "pfalcon/berkeley-db-1.xx",
    "project-chip/zap",
    "protobuf-c/protobuf-c",
    "pybind/pybind11",
    "Qorvo/qpg-openthread",
    "Qorvo/QMatter",
    "raspberrypi/pico-sdk",
    "tatsuhiro-t/neverbleed",
    "ThrowTheSwitch/CMock",
    "throwtheswitch/cexception",
    "throwtheswitch/unity",
    "ThrowTheSwitch/Unity",
    "troglobit/editline",
    "warmcat/libwebsockets",
    "zserge/jsmn",
]


COUNTRY_CODE = ""  # "China" or other


def set_country_code():
    global COUNTRY_CODE
    if len(COUNTRY_CODE):
        return COUNTRY_CODE

    try:
        response = requests.get('http://www.ip-api.com/json', timeout=5)
        response.raise_for_status()

        result = response.json()
        country = result.get("country", "")
        print(f"country code: {country}")

        COUNTRY_CODE = country
    except requests.exceptions.RequestException as e:
        print(f"country code error: {e}")

    return COUNTRY_CODE


def get_country_code():
    global COUNTRY_CODE
    if len(COUNTRY_CODE):
        return COUNTRY_CODE
    return set_country_code()


def _rm_rf(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        return True
    elif os.path.isdir(file_path):
        shutil.rmtree(file_path)


def do_subprocess(cmds, directory=""):
    if not cmds:
        print("Subprocess cmds is empty.")
        return 0

    if directory:
        if os.path.exists(directory):
            os.chdir(directory)
        else:
            print(f"Subprocess not found [{directory}].")
            return 1

    print(f'''do subprocess:
directory: {directory}
cmds: {cmds}''')
    ret = 1  # 0: success
    original_dir = os.getcwd()
    try:
        # bufsize=1启用行缓冲
        process = subprocess.Popen(
            cmds,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        )

        for line in iter(process.stdout.readline, ''):
            sys.stdout.write(line)

        ret = process.wait()

        stderr = process.stderr.read()
        if stderr:
            sys.stderr.write(stderr)
    finally:
        os.chdir(original_dir)

    print(f"do subprocess result: {ret}")
    return ret


def need_prepare(prepare_file, target):
    if not os.path.exists(prepare_file):
        return True
    with open(prepare_file, "r", encoding='utf-8') as f:
        old_target = f.read().strip()
    print(f"old_target: {old_target}")
    if target != old_target:
        return True
    return False


def record_prepare(prepare_file, target):
    with open(prepare_file, "w", encoding='utf-8') as f:
        f.write(target)
    return True


def delete_temp_files(root):
    delete_list = [".target", ".app", ".prepare"]
    for d in delete_list:
        delete_file = os.path.join(root, d)
        print(f"delete: {d}")
        _rm_rf(delete_file)

    root = os.path.join(root, "tuya_open_sdk")
    delete_list = ["sdkconfig", "sdkconfig.old", "sdkconfig.defaults", "build"]
    for d in delete_list:
        delete_file = os.path.join(root, d)
        print(f"delete: {d}")
        _rm_rf(delete_file)
    pass


def exists_idf_py():
    try:
        result = subprocess.run(
            ["idf.py", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(f"idf.py version: {result.stdout.strip()}")
            return True
    except Exception as e:
        print(f"Run idf.py error: {str(e)}")

    return False


def export_idf_path(root):
    idf_path = os.path.join(root, "esp-idf")
    idf_tools_path = os.path.join(root, ".espressif")
    os.environ["IDF_PATH"] = idf_path
    os.environ["IDF_TOOLS_PATH"] = idf_tools_path
    pass


def jihu_mirro(unset=False):
    if get_country_code() != "China":
        return
    g = Git()
    for repo in MIRROR_LIST:
        jihu = f"https://jihulab.com/esp-mirror/{repo}"
        if unset:
            g.config(
                "--global",
                "--unset",
                f"url.{jihu}.insteadOf")
            g.config(
                "--global",
                "--unset",
                f"url.{jihu}.git.insteadOf")
        else:
            github = f"https://github.com/{repo}"
            g.config(
                "--global",
                f"url.{jihu}.insteadOf",
                f"{github}")
            g.config(
                "--global",
                f"url.{jihu}.git.insteadOf",
                f"{github}")
    pass


def download_esp_idf():
    print("Downloading ESP_IDF ...")

    jihu_mirro(unset=False)

    idf_path = os.environ["IDF_PATH"]
    if not os.path.exists(idf_path):
        idf_version = "v5.4"
        cmds = [
            "git",
            "clone",
            "--recursive",
            "https://github.com/espressif/esp-idf",
            "-b",
            idf_version,
            "--depth=1",
            idf_path,
        ]
        if do_subprocess(cmds) != 0:
            jihu_mirro(unset=True)
            return False

    cmds = [
        "git",
        "submodule",
        "update",
        "--init",
        "--recursive",
    ]
    if do_subprocess(cmds, idf_path) != 0:
        jihu_mirro(unset=True)
        return False

    jihu_mirro(unset=True)
    print("Download ESP_IDF success.")
    return True


def install_target(target):
    if get_country_code() != "China":
        os.environ["IDF_GITHUB_ASSETS"] = "dl.espressif.cn/github_assets"
    else:
        os.environ["IDF_GITHUB_ASSETS"] = "dl.espressif.com/github_assets"

    idf_path = os.environ["IDF_PATH"]
    cmds = [
        "./install.sh",
        target,
    ]
    if do_subprocess(cmds, idf_path) != 0:
        return False

    print(f"Install target [{target}] success.")
    return True


def main():
    target = "esp32s3" if len(sys.argv) < 2 else sys.argv[1]
    print(f"target: {target}")
    root = os.path.dirname(os.path.abspath(__file__))
    prepare_file = os.path.join(root, ".prepare")
    if not need_prepare(prepare_file, target):
        print("No need prepare.")
        sys.exit(0)
    print("Need prepare.")
    delete_temp_files(root)
    # if not exists_idf_py():
    export_idf_path(root)
    if not download_esp_idf():
        print("Download ESP_IDF failed.")
        sys.exit(1)
    if not install_target(target):
        print(f"Install target [{target}] failed.")
        sys.exit(1)
    record_prepare(prepare_file, target)
    sys.exit(0)


if __name__ == "__main__":
    main()
