import argparse
import os
import re
import sys
import util


def exit_with_error(chapter):
    util.cprint(
        'Chapters should be formatted like so: "Name,00:00:00.000"'
        f' not as "{chapter}"', "red")
    sys.exit(1)


def process_chapters(chapters):
    processed_chapters = []
    for chapter in chapters:
        if not re.match(r"^\w+,\d\d:\d\d:\d\d\.\d\d\d$", chapter):
            exit_with_error(chapter)
        processed_chapters.append(chapter.split(","))
    util.cprint(processed_chapters, "blue")
    return processed_chapters


def generate_chapter_xml(chapter):
    output_string = f"<ChapterAtom><ChapterTimeStart>{chapter[1]}"
    output_string += "</ChapterTimeStart><ChapterDisplay>"
    output_string += f"<ChapterString>{chapter[0]}</ChapterString>"
    output_string += "<ChapterLanguage>eng</ChapterLanguage>"
    output_string += "</ChapterDisplay></ChapterAtom>"
    return output_string


def generate_xml_file(chapters):
    output_string = '<?xml version="1.0" encoding="UTF-8"?>'
    output_string += '<!DOCTYPE Chapters SYSTEM "matroskachapters.dtd">'
    output_string += "<Chapters><EditionEntry>"
    for chapter in chapters:
        output_string += generate_chapter_xml(chapter)
    output_string += "</EditionEntry></Chapters>"
    with open("chapters.temp.xml", "w") as f:
        f.write(output_string)


def main():
    parser = argparse.ArgumentParser(
        description="Add a list of chapters to an mkv")
    parser.add_argument("file", help="Location of the mkv file to modify")
    parser.add_argument(
        "chapters", nargs="+",
        help='Add a list of chapters like this: "Opening,00:00:00.000" '
             '"Part 1,00:01:30.000"')
    args = parser.parse_args()
    if not args.file.endswith(".mkv"):
        util.cprint("Input file must be an mvk", "red")
        sys.exit(1)
    if not os.path.isfile(args.file):
        util.cprint(f"Mkv file could not be found: '{args.file}'", "red")
        sys.exit(1)
    processed_chapters = process_chapters(args.chapters)
    generate_xml_file(processed_chapters)
    util.run_command(f'mkvpropedit --chapters chapters.temp.xml "{
        util.escape(args.file)}"')
    os.remove("chapters.temp.xml")


if __name__ == "__main__":
    main()
