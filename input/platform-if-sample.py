# https://github.com/RoboStack/vinca/blob/c01600faa53a1dc6bc752db89964d2e4186a6d68/vinca/main.py
def get_conda_subdir():
    if config.parsed_args.platform:
        return config.parsed_args.platform

    sys_platform = sys.platform
    machine = platform.machine()

    if sys_platform.startswith("linux"):
        if machine == "aarch64":
            return "linux-aarch64"
        elif machine == "x86_64":
            return "linux-64"
        else:
            raise RuntimeError("Unknown machine!")
    elif sys_platform == "darwin":
        if machine == "arm64":
            return "osx-arm64"
        else:
            return "osx-64"
    elif sys_platform == "win32":
        return "win-64"