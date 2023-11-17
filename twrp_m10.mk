#
# Copyright (C) 2022 The Android Open Source Project
# Copyright (C) 2022 SebaUbuntu's TWRP device tree generator
#
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/aosp_base.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit some common twrp stuff.
$(call inherit-product, vendor/twrp/config/common.mk)

# Inherit from java device
$(call inherit-product, device/positivo/m10/device.mk)

PRODUCT_DEVICE := m10
PRODUCT_NAME := twrp_m10
PRODUCT_BRAND := positivo
PRODUCT_MODEL := m10 4g pro x
PRODUCT_MANUFACTURER := positivo

PRODUCT_GMS_CLIENTID_BASE := android-positivo

PRODUCT_BUILD_PROP_OVERRIDES += \
    PRIVATE_BUILD_DESC="T2040-user 10 QP1A.190711.020 URFR2021070302 release-keys"

BUILD_FINGERPRINT := positivo/M10/T2040:10/QP1A.190711.020/URFR2021070302:user/release-keys
