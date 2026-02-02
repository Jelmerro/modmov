import argparse
import os
import util


def main():
    parser = argparse.ArgumentParser(
        description="Concatenate all given movies into a single mp4")
    parser.add_argument(
        "files", nargs="+", help="Locations of the files to process")
    args = parser.parse_args()
    with open("concat.temp.txt", "w") as c:
        for f in args.files:
            name = f.replace("'", "'\\''")
            c.write(f"file '{name}'\n")
    util.run_command(
        'ffmpeg -y -safe 0 -f concat -i concat.temp.txt Concat.mp4')
    os.remove("concat.temp.txt")


if __name__ == "__main__":
    main()
