LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_CFLAGS = -Wno-psabi

LOCAL_LDLIBS := -llog

LOCAL_MODULE    := myjni
LOCAL_SRC_FILES := native.cpp

include $(BUILD_SHARED_LIBRARY)

