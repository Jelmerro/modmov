import argparse
import util


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Concatenate all given movies into a single mp4")
    parser.add_argument(
        "files", nargs="+", help="Locations of the files to process")
    args = parser.parse_args()
    util.run_command(f'ffmpeg -i "concat:{"|".join(args.files)}" Concat.mp4')
