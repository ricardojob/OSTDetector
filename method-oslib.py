import sys
import os
import platform

# https://docs.python.org/3/library/sys.html
#This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. 
print(f'sys.platform: {sys.platform}') #This string contains a platform identifier that can be used to append platform-specific components to sys.path, for instance.
# print(f'sys.getwindowsversion(): {sys.getwindowsversion()}') #Return a named tuple describing the Windows version currently running.

# print(f'sys.abiflags: {sys.abiflags}')
# print(f'sys.argv: {sys.argv}')
# print(f'sys.int_info: {sys.int_info}')
# print(f'sys.modules: {sys.modules}')
# print(f'sys.path: {sys.path}') #A list of strings that specifies the search path for modules
# print(f'sys.platform: {sys.platform}') #This string contains a platform identifier that can be used to append platform-specific components to sys.path, for instance.
# print(f'sys.getprofile(): {sys.getprofile()}')
# print(f'sys.thread_info: {sys.thread_info}')
# print(f'sys.version: {sys.version}')
# print(f'sys.getwindowsversion(): {sys.getwindowsversion()}') #Return a named tuple describing the Windows version currently running.


# https://docs.python.org/3/library/platform.html
#  platform — Access to underlying platform’s identifying data¶: platform module for achieving accurate OS version.
# print(f'platform.machine(): {platform.machine()}')
# print(f'platform.node(): {platform.node()}')
print(f'platform.platform(): {platform.platform()}') #Returns a single string identifying the underlying platform with as much useful information as possible.
print(f'platform.system(): {platform.system()}') #Returns the system/OS name, such as 'Linux', 'Darwin', 'Java', 'Windows'. 
print(f'platform.version(): {platform.version()}') #Returns the system’s release version, e.g. '#3 on degas'
print(f'platform.uname(): {platform.uname()}') #Returns a namedtuple() containing six attributes: system, node, release, version, machine, and processor.
# métodos que retornam informações específicas sobre o sistema operacional
print(f'platform.win32_edition(): {platform.win32_edition()}')
print(f'platform.win32_ver(): {platform.win32_ver()}')
print(f'platform.win32_is_iot(): {platform.win32_is_iot()}')
print(f'platform.mac_ver(): {platform.mac_ver()}')
print(f'platform.libc_ver(): {platform.libc_ver()}')
print(f'platform.freedesktop_os_release(): {platform.freedesktop_os_release()}')



# https://docs.python.org/3/library/os.html
# os — Miscellaneous operating system interfaces
# This module provides a portable way of using operating system dependent functionality. 
print(f'os.name: {os.name}') #name of the operating system dependent module imported.
print(f'os.supports_bytes_environ: {os.supports_bytes_environ}') #True if the native OS type of the environment is bytes (eg. False on Windows).
print(f'os.uname(): {os.uname()}') #Returns information identifying the current operating system. 

# Process Parameters: these functions and data items provide information and operate on the current process and user.
# The following data values are used to support path manipulation operations. 

# print(f'os.name: {os.name}') #name of the operating system dependent module imported.
# print(f'os.ctermid: {os.ctermid()}') #Return the filename corresponding to the controlling terminal of the process.
# print(f'os.environ: {os.environ}') #A mapping object where keys and values are strings that represent the process environment. 
# print(f'os.environb: {os.environb}') #Bytes version of environ: a mapping object where both keys and values are bytes objects representing the process environment. 
# print(f'os.getenv: {os.getenv("SHELL")}') 
# print(f'os.getenvb: {os.getenv("SHELL")}') 
# print(f'os.supports_bytes_environ: {os.supports_bytes_environ}') #True if the native OS type of the environment is bytes (eg. False on Windows).
# print(f'os.uname(): {os.uname()}') #Returns information identifying the current operating system. 
# print(f'os.pathconf_names: {os.pathconf_names}') #Dictionary mapping names accepted by pathconf() and fpathconf()
# print(f'os.supports_fd: {os.supports_fd}')
# print(f'os.confstr_names: {os.confstr_names}') #Dictionary mapping names accepted by confstr() to the integer values
# print(f'os.times(): {os.times()}') 
# print(f'os.chdir: {os.chdir("/")}') 
# print(f'os.fchdir(fd): { os.fchdir(None)}')
# print(f'os.getcwd: {os.getcwd()}') #These functions are described in Files and Directories.
# print(f'os.fsencode: {os.fsencode(".")}') #Encode path-like filename to the filesystem encoding and error handler;
