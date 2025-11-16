import argparse
import os
import re
import subprocess
import sys
import util


def handle_movie(folder, movie, audio_list, subs_list, def_audio, def_subs):
    movie = os.path.join(folder, movie)
    str_defaults = ""
    for track in audio_list + subs_list:
        str_defaults += f"--edit track:{track} --set flag-" \
            "default=0 --set flag-forced=0 "
    if def_audio != "none":
        str_defaults += f"--edit track:{def_audio} --set flag-" \
            "default=1 --set flag-forced=0 "
    if def_subs != "none":
        str_defaults += f"--edit track:{def_subs} --set flag-" \
            "default=1 --set flag-forced=0 "
    util.run_command(f'mkvpropedit "{util.escape(movie)}" {str_defaults}')


def extract_track_info(movie, complete_scan=False):
    extra_args = ""
    if complete_scan:
        extra_args = "--all"
    proc = subprocess.run(
        f'mkvinfo {extra_args} "{util.escape(movie)}"', shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    mkvinfo_output = proc.stdout.decode()
    regex = re.compile(r"\| \+ Track(?:.*\n\| {2,}?\+ .*)+")
    info = []
    audio_counter = 0
    subs_counter = 0
    for track in regex.findall(mkvinfo_output):
        track_type = util.mkv_property(track, "Track type")
        if track_type not in ["audio", "subtitles"]:
            continue
        if track_type == "audio":
            audio_counter += 1
            type_number = audio_counter
        if track_type == "subtitles":
            subs_counter += 1
            type_number = subs_counter
        info.append({
            "id": f"{track_type[0]}{type_number}",
            "default": util.mkv_property(track, '"Default track" flag'),
            "forced": util.mkv_property(track, '"Forced display" flag'),
            "language": util.mkv_property(track, "Language"),
            "name": util.mkv_property(track, "Name")
        })
    return info


def print_track_info(info):
    util.cprint("Available tracks found:", "green")
    for track in info:
        util.cprint(track["id"], "blue")
        util.cprint(f"  name: {track['name']}")
        util.cprint(f"  default: {track['default']}")
        util.cprint(f"  forced: {track['forced']}")
        util.cprint(f"  language: {track['language']}")
    util.cprint("You can also pick 'none' as the default below")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Set the default audio/subtitle track for multiple mkvs")
    parser.add_argument(
        "location", help="Location of the folder/file to process")
    args = parser.parse_args()
    files = util.list_movies(args.location, False)
    if not files:
        print("No movie files found in the specified directory")
        print("Input files are expected to be: .mkv")
        print("All matched files will have their default tracks updated")
        sys.exit()
    current_info = ""
    for f in files:
        util.cprint(f"Found movie: '{f['file']}'", "green")
        info = extract_track_info(os.path.join(f["dir"], f["file"]))
        if not info:
            info = extract_track_info(os.path.join(f["dir"], f["file"]), True)
        if info != current_info:
            print_track_info(info)
            audio_tracks = [
                track["id"] for track in info if track["id"].startswith("a")
            ]
            sub_tracks = [
                track["id"] for track in info if track["id"].startswith("s")
            ]
            audio_track = util.question(
                "Which audio track should be set as the default",
                audio_tracks + ["none"])
            sub_track = util.question(
                "Which subtitle track should be set as the default",
                sub_tracks + ["none"])
            if audio_track in audio_tracks:
                audio_tracks.remove(audio_track)
            if sub_track in sub_tracks:
                sub_tracks.remove(sub_track)
            current_info = info
        handle_movie(
            f["dir"], f["file"],
            audio_tracks, sub_tracks, audio_track, sub_track)
