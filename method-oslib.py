import sys
import os
import platform

print(f'os.name: {os.name}') #name of the operating system dependent module imported.
# print(f'os.ctermid(): {os.ctermid()}') #filename corresponding 
# print(f'os.environ: {os.environ}') #mapping
# print(f'os.environb: {os.environb}') #mapping
# print(f'os.getenv: {os.getenv("SHELL")}') 
# print(f'os.getenvb: {os.getenv("SHELL")}') 
print(f'os.supports_bytes_environ: {os.supports_bytes_environ}') #True if the native OS type of the environment is bytes (eg. False on Windows).
print(f'os.uname(): {os.uname()}') #Returns information identifying the current operating system. 
# print(f'os.pathconf_names: {os.pathconf_names}') #Dictionary mapping names accepted by pathconf() and fpathconf()
# print(f'os.supports_fd: {os.supports_fd}')
# print(f'os.confstr_names: {os.confstr_names}') #Dictionary mapping names accepted by confstr() to the integer values

# https://docs.python.org/3/library/sys.html
#This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. It is always available.

print(50*'--')
print(f'sys.abiflags: {sys.abiflags}')
print(f'sys.argv: {sys.argv}')
print(f'sys.getprofile(): {sys.getprofile()}')
# print(f'sys.getwindowsversion(): {sys.getwindowsversion()}') #



# print(sys.platform)

# print(platform.system())
# print(platform.platform())
# print(platform.uname())
# print(platform.version())
# métodos especificos para plataformas especificas
print(platform.win32_ver())
print(platform.win32_edition())
print(platform.win32_is_iot())
print(platform.mac_ver())
print(platform.libc_ver())
print(platform.freedesktop_os_release())

"""
# https://docs.python.org/3/library/os.html

# Process Parameters
# These functions and data items provide information and operate on the current process and user.
print(f'os.ctermid: {os.ctermid()}') #Return the filename corresponding to the controlling terminal of the process.
print(f'os.environ: {os.environ}') #A mapping object where keys and values are strings that represent the process environment. 
print(f'os.environb: {os.environb}') #Bytes version of environ: a mapping object where both keys and values are bytes objects representing the process environment. 
print(f'os.chdir: {os.chdir("/")}') 
# print(f'os.fchdir(fd): { os.fchdir(None)}')
print(f'os.getcwd: {os.getcwd()}') #These functions are described in Files and Directories.
print(f'os.fsencode: {os.fsencode(".")}') #Encode path-like filename to the filesystem encoding and error handler;
# os.fsencode(filename)
# Encode path-like filename to the filesystem encoding and error handler; return bytes unchanged.

"""
