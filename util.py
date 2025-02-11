import os
import re
import subprocess


COLORS = {
    "red": "\x1b[31m",
    "green": "\x1b[32m",
    "yellow": "\x1b[33m",
    "blue": "\x1b[34m",
    "purple": "\x1b[35m"
}
END = "\x1b[0m"


def cprint(text, color=None):
    if not color or color not in COLORS:
        print(text)
        return
    print(f"{COLORS[color]}{text}{END}")


def run_command(command):
    cprint(command, "blue")
    proc = subprocess.Popen(command, shell=True)
    proc.communicate()


def capture_command(command):
    proc = subprocess.run(
        command, shell=True,
        stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return proc.stdout.decode().strip(), proc.stderr.decode().strip()


def escape(contents):
    contents = contents.replace('\\', '\\\\').replace('"', '\\"')
    contents = contents.replace('`', '\\`').replace('$', '\\$')
    return contents


def question(question, valid_options):
    result = None
    while result not in valid_options:
        result = input(f"{COLORS['purple']}{question}?{END} ").lower().strip()
    return result


def list_movies(location, allow_mp4=True):
    if os.path.isfile(location):
        return [{
            "dir": os.path.dirname(location),
            "file": os.path.basename(location)
        }]
    if not os.path.isdir(location):
        return []
    return [
        {
            "dir": location, "file": f
        } for f in sorted(os.listdir(location))
        if f.endswith(".mkv") or (f.endswith(".mp4") and allow_mp4)
    ]


def mkv_property(track, property_name):
    result = re.search(fr"\|  \+ {property_name}: (.*)", track)
    if result:
        return result.group(1)
    return ""
