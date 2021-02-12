DIRECTORY = "/home/admin/Documents/Application/re/pintool"
PIN_DIRECTORY = "{}/pin-3.15".format(DIRECTORY)
PIN = "{}/pin".format(PIN_DIRECTORY)
SOURCE_CODE = "{}/source/tools/ManualExamples".format(PIN_DIRECTORY)
obj_intel64 = "{}/obj-intel64".format(SOURCE_CODE)
obj_ia32 = "{}/obj-ia32".format(SOURCE_CODE)
INSCOUNT32 = "{}/inscount0.so".format(obj_ia32)
INSCOUNT64 = "{}/inscount0.so".format(obj_intel64)
MIN_NUM = 0x7fffffffffffffff
MAX_NUM = -0x7fffffffffffffff
INSCOUNT = INSCOUNT64

