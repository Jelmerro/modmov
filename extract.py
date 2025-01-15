import argparse
import os
import re
import util


def handle_movie(folder, movie, subs):
    if not os.path.isdir(os.path.join(folder, "Extracted")):
        os.mkdir(os.path.join(folder, "Extracted"))
    util.cprint(f"Found movie: '{movie}'", "green")
    movie_mp4 = os.path.join(
        folder, "Extracted", re.sub(r"(\.mkv|\.mp4)$", ".mp4", movie))
    movie = os.path.join(folder, movie)
    if subs != "only":
        util.run_command(f'ffmpeg -y -i "{movie}" -c copy "{movie_mp4}"')
    if subs != "no":
        for ext in ["srt", "ass", "ssa", "mks", "sub"]:
            _, output = util.capture_command(f'ffprobe "{movie}"')
            if f" ({ext})" in output:
                output = os.path.join(
                    folder, "Extracted",
                    re.sub(r"(\.mkv|\.mp4)$", f".{ext}", movie))
                util.run_command(f'ffmpeg -y -i "{movie}" -c copy "{output}"')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract a streamable mp4 from any mkv or mp4")
    parser.add_argument(
        "-s", "--subs", choices=["yes", "only", "no"], default="no",
        help="Control if subs should be extracted as well (or do only that)")
    parser.add_argument(
        "location", help="Location of the folder/file to process")
    args = parser.parse_args()
    files = util.list_movies(args.location)
    for f in files:
        handle_movie(f["dir"], f["file"], args.subs)
    if not files:
        print("No movie files found in the specified directory")
        print("Input files are expected to be: .mkv or .mp4")
        print("All matched files will be extracted to a single mp4 per movie")
        print("Optionally you can extract the subtitles to the right file too")
