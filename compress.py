import argparse
import os
import util


def handle_movie(folder, movie, compression):
    if not os.path.isdir(os.path.join(folder, "Compressed")):
        os.mkdir(os.path.join(folder, "Compressed"))
    util.cprint(f"Found movie: '{movie}'", "green")
    com_movie = os.path.join(folder, "Compressed", movie)
    movie = os.path.join(folder, movie)
    util.run_command(
        f'ffmpeg -y -i "{movie}" -map 0:v -map 0:a -map 0:s? -scodec copy -crf'
        f' {compression} "{com_movie}"')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compress the bitrate of any mkv or mp4")
    parser.add_argument(
        "location", help="Location of the folder/file to process")
    parser.add_argument(
        "-c", "--compress", type=int, default=20, choices=range(0, 51),
        help="Level of compression, 0=lossless, 50=garbage, 20=default")
    args = parser.parse_args()
    files = util.list_movies(args.location)
    for f in files:
        handle_movie(f["dir"], f["file"], args.compress)
    if not files:
        print("No movie files found in the specified directory")
        print("Input files are expected to be: .mkv or .mp4")
        print("All matched files will be compressed to reduce size")
