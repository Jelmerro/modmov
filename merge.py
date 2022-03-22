import argparse
import os
import util


def merge_command(folder, movie, subtitle, attachments):
    base = os.path.splitext(movie)[0]
    if not os.path.isdir(os.path.join(folder, "Merged")):
        os.mkdir(os.path.join(folder, "Merged"))
    command = 'mkvmerge -o "{}.mkv" "{}" "{}.{}"'.format(
        util.escape(os.path.join(folder, "Merged", base)),
        util.escape(os.path.join(folder, movie)),
        util.escape(os.path.join(folder, base)),
        subtitle)
    for attach in attachments:
        command += f' --attach-file "{util.escape(os.path.abspath(attach))}"'
    util.run_command(command)


def handle_movie(folder, movie, attachments):
    base = os.path.splitext(movie)[0]
    util.cprint(f"Found movie: '{movie}'", "green")
    if os.path.isfile(os.path.join(folder, f"{base}.srt")):
        merge_command(folder, movie, "srt", attachments)
    elif os.path.isfile(os.path.join(folder, f"{base}.ass")):
        merge_command(folder, movie, "ass", attachments)
    else:
        util.cprint("No matching subtitle file found!", "red")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Merge mkv/mp4 files with srt/ass subtitles to mkv")
    parser.add_argument(
        "location", help="Location of the folder/file to process")
    parser.add_argument(
        "attachments", nargs="*",
        help="Each font/image is added as an attachment to every mkv file")
    args = parser.parse_args()
    files = util.list_movies(args.location)
    for f in files:
        handle_movie(f["dir"], f["file"], args.attachments)
    if not files:
        print("No movie files found in the specified directory")
        print("Input files are expected to be: .mkv, .mp4, .srt and .ass")
        print("All matched files will be merged to a single .mkv per movie")
