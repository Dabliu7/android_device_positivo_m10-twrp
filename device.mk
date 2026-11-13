# API level do firmware de fábrica (Android 10)
PRODUCT_SHIPPING_API_LEVEL := 29

# Fastbootd
PRODUCT_PACKAGES += \
    fastbootd \
    android.hardware.fastboot@1.0-impl-mock \
    android.hardware.fastboot@1.0-impl-mock.recovery

# Dynamic partitions
PRODUCT_USE_DYNAMIC_PARTITIONS := true
