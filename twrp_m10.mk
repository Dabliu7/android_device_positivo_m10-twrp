# Release name
PRODUCT_RELEASE_NAME := t2040

# Inherit some common twrp stuff.
$(call inherit-product, vendor/omni/config/common.mk)

# Inherit from t2040 device
$(call inherit-product, device/positivo/t2040/device.mk)

PRODUCT_DEVICE := t2040
PRODUCT_NAME :=omni_m10
PRODUCT_BRAND := positivo
PRODUCT_MODEL := m10 4g pro x
PRODUCT_MANUFACTURER := positivo

PRODUCT_BUILD_PROP_OVERRIDES += \
    PRIVATE_BUILD_DESC="T2040-user 10 QP1A.190711.020 URFR2021070302 release-keys"

BUILD_FINGERPRINT := positivo/M10/T2040:10/QP1A.190711.020/URFR2021070302:user/release-keys
