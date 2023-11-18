ifneq ($(filter $$DEVICE$$,$(TARGET_DEVICE)),)

LOCAL_PATH := device/positivo/t2040

include $(call all-makefiles-under,$(LOCAL_PATH))

endif
