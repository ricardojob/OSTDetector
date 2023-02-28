import sys
import os
import platform

print(sys.platform)
print(os.uname())
print(os.name)
print(platform.system())
print(platform.platform())
print(platform.uname())
print(platform.version())
print(platform.win32_ver())
print(platform.win32_edition())
print(platform.win32_is_iot())
print(platform.mac_ver())
print(platform.libc_ver())
print(platform.freedesktop_os_release())