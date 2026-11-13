# Release name
PRODUCT_RELEASE_NAME := t2040

# Inherit from the AOSP base product (32-bit only device)
$(call inherit-product, $(SRC_TARGET_DIR)/product/aosp_base.mk)

# Inherit some common TWRP stuff.
$(call inherit-product, vendor/twrp/config/common.mk)

# Inherit from t2040 device
$(call inherit-product, device/positivo/t2040/device.mk)

PRODUCT_DEVICE := t2040
PRODUCT_NAME := twrp_t2040
PRODUCT_BRAND := positivo
PRODUCT_MODEL := M10 4G PRO X
PRODUCT_MANUFACTURER := positivo

PRODUCT_BUILD_PROP_OVERRIDES += \
    PRIVATE_BUILD_DESC="T2040-user 10 QP1A.190711.020 URBM2021011601 release-keys"

BUILD_FINGERPRINT := positivo/M10/T2040:10/QP1A.190711.020/URBM2021011601:user/release-keys
