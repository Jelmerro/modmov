import argparse
import os
import re
import util


def handle_movie(folder, movie):
    if not os.path.isdir(os.path.join(folder, "Streamable")):
        os.mkdir(os.path.join(folder, "Streamable"))
    util.cprint(f"Found movie: '{movie}'", "green")
    movie_mp4 = os.path.join(
        folder, "Streamable",
        re.sub(r"(\.mkv|\.mp4)$", ".mp4", movie))
    movie = os.path.join(folder, movie)
    util.run_command(f'ffmpeg -i "{movie}" -c copy "{movie_mp4}"')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract a streamable mp4 from any mkv or mp4")
    parser.add_argument(
        "location", help="Location of the folder/file to process")
    args = parser.parse_args()
    files = util.list_movies(args.location)
    for f in files:
        handle_movie(f["dir"], f["file"])
    if not files:
        print("No movie files found in the specified directory")
        print("Input files are expected to be: .mkv or .mp4")
        print("All matched files will be extracted to a single mp4 per movie")
