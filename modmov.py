#!/usr/bin/env python3
import os
import sys

from scripts import chapters, compress, concat, defaults, extract, lint, merge

from scripts.util import cprint


def show_help():
    print("Welcome to modmov\n")
    print("Modify Movies with ease using a collection of single task scripts")
    print("\nPlease specify the name of the task you wish to call\n")
    print("Each task has a different set of arguments, use --help for info")
    print("For example: './modmov merge --help' for help on the merge task\n")
    print("usage: modmov TASK [OPTIONS...]\n")
    print("The following tasks are included:")
    cprint("chapters", "green")
    print("  Add a list of chapters to an mkv")
    cprint("  Modifies the original", "yellow")
    cprint("  accepts: a single mkv", "purple")
    cprint("  requires: mkvpropedit (mkvtoolnix)", "purple")
    cprint("compress", "green")
    print("  Compress the bitrate of any mkv or mp4")
    print("  This task will only modify the bitrate, other aspects are untouched")
    cprint("  Creates a separate folder named 'Compressed'", "yellow")
    cprint("  accepts: a folder with mkvs/mp4s or a single mkv/mp4", "purple")
    cprint("  requires: ffmpeg", "purple")
    cprint("concat", "green")
    print("  Concatenate all given movies into a single mp4")
    cprint("  Creates a separate movie named 'Concat.mp4'", "yellow")
    cprint("  accepts: any number of movie files as separate arguments", "purple")
    cprint("  requires: ffmpeg", "purple")
    cprint("defaults", "green")
    print("  Set the default audio/subtitle track for multiple mkvs")
    print("  This task will ask for more details interactively to select the tracks")
    print("  When multiple files share a track layout, the same defaults are applied")
    cprint("  Modifies the original", "yellow")
    cprint("  accepts: a folder with mkvs or a single mkv", "purple")
    cprint("  requires: mkvpropedit and mkvinfo (mkvtoolnix)", "purple")
    cprint("extract", "green")
    print("  Extract a streamable mp4 from any mkv or mp4")
    print("  All movies will be extracted to a single track mp4 well-suited for streaming")
    print("  Only the first audio and first video track are extracted by default")
    print("  Subtiles are never included in the extracted mp4 file")
    print("  But they can be extracted into a separate file with the --subs arg")
    cprint("  Creates a separate folder named 'Extracted'", "yellow")
    cprint("  accepts: a folder with mkvs/mp4s or a single mp4/mkv", "purple")
    cprint("  requires: ffmpeg", "purple")
    cprint("merge", "green")
    print("  Merge mkv/mp4 files with srt/ass/ssa/mks/sub subs to mkv")
    print("  This process is also known as 'muxing' movies")
    print("  You can optionally specify additional resources like fonts or images")
    cprint("  Creates a separate folder named 'Merged'", "yellow")
    cprint("  accepts: a folder with mkvs/mp4s or a single mkv/mp4", "purple")
    cprint("  requires: mkvmerge (mkvtoolnix)", "purple")
    cprint("lint", "green")
    print("  Find common errors in movie files by running a set of linters")
    print("  This is similar to code quality tools, but for movie files")
    cprint("  Does not currently modify files", "yellow")
    cprint("  accepts: a folder with mkvs/mp4s", "purple")
    cprint("  requires: mkvinfo (mkvtoolnix)\n", "purple")
    print("modmov is created by Jelmer van Arnhem")
    print("You may copy and modify the code under the terms of the MIT license")
    print("See https://github.com/Jelmerro/modmov for more information")
    sys.exit()


def main():
    if len(sys.argv) < 2:
        show_help()
    script_name = sys.argv[1]
    if script_name.endswith(".py"):
        script_name = script_name.replace(".py", "")
    module_list = [
        chapters,
        compress,
        concat,
        defaults,
        extract,
        lint,
        merge
    ]
    valid_names = [n.__name__ for n in module_list]
    if "scripts." + script_name not in valid_names:
        show_help()
    sys.argv = [os.path.abspath(script_name)] + sys.argv[2:]
    globals()[script_name].main()


if __name__ == "__main__":
    main()
