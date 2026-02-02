import argparse
import os
import re
import subprocess
import sys
from glob import glob
from . import util


def time_to_sec(t):
    h, m, s = map(int, t.split(':'))
    return h * 3600 + m * 60 + s


def extract_track_info(movie, complete_scan=False):
    extra_args = ""
    if complete_scan:
        extra_args = "--all"
    proc = subprocess.run(
        f'mkvinfo {extra_args} "{util.escape(movie)}"', shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        mkvinfo_output = proc.stdout.decode()
    except UnicodeDecodeError:
        util.cprint(movie, "green")
        util.cprint("Failed to decode mkvinfo output!", "red")
        if not complete_scan:
            util.cprint(proc.stdout)
        return None
    chapters = len([
        ln for ln in mkvinfo_output.split("\n") if ln == "|  + Chapter atom"
    ])
    if not complete_scan and not chapters:
        return None
    regex = re.compile(r"\| \+ Track(?:.*\n\| {2,}?\+ .*)+")
    all_tracks = []
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
        all_tracks.append({
            "id": f"{track_type[0]}{type_number}",
            "default": util.mkv_property(track, '"Default track" flag'),
            "forced": util.mkv_property(track, '"Forced display" flag'),
            "language": util.mkv_property(track, "Language"),
            "name": util.mkv_property(track, "Name")
        })
    duration_string = re.search(r"\| \+ Duration: (.*)", mkvinfo_output)
    duration = 0
    if duration_string:
        duration = time_to_sec(duration_string.group(1).split(".")[0])
    return {"tracks": all_tracks, "chapters": chapters, "duration": duration}


def print_track_errors(f, info):
    errors = []
    warnings = []
    # Check for chapters in files over 15 minutes
    if info["chapters"] < 2 and info["duration"] > 900:
        errors.append("No chapters present in file!")
    # Check if there are audio and sub tracks enabled by default
    audio_tracks = [tr for tr in info["tracks"] if tr["id"].startswith("a")]
    sub_tracks = [tr for tr in info["tracks"] if tr["id"].startswith("s")]
    # disabled_audio = [tr for tr in audio_tracks if tr["default"] == "0"]
    # if len(audio_tracks) == len(disabled_audio):
    #     errors.append("No audio tracks enabled by default!")
    disabled_sub = [tr for tr in sub_tracks if tr["default"] == "0"]
    if sub_tracks and len(sub_tracks) == len(disabled_sub):
        errors.append("No sub tracks enabled by default!")
    # Warn for implicit defaults when there are multiple tracks
    implicit_audio = [tr for tr in audio_tracks if tr["default"] == ""]
    if len(implicit_audio) > 1:
        warnings.append("Using implicit defaults on multiple audio tracks!")
    implicit_sub = [tr for tr in sub_tracks if tr["default"] == ""]
    if len(implicit_sub) > 1:
        warnings.append("Using implicit defaults on multiple sub tracks!")
    # Check for duplicate default tracks, undocumented behavior in players
    default_audio = [tr for tr in audio_tracks if tr["default"] == "1"]
    if len(default_audio) > 1:
        errors.append("Multiple default audio tracks set!")
    default_sub = [tr for tr in sub_tracks if tr["default"] == "1"]
    if len(default_sub) > 1:
        errors.append("Multiple default sub tracks set!")
    # Check for files with multiple tracks that don't specify language
    # no_lang_audio = [tr for tr in default_audio if tr["language"] == ""]
    # if len(audio_tracks) > 1 and no_lang_audio:
    #     errors.append("No audio track language on a default audio track!")
    # no_lang_sub = [tr for tr in default_sub if tr["language"] == ""]
    # if len(sub_tracks) > 1 and no_lang_sub:
    #     errors.append("No sub track language on a default sub track!")
    # Check if jp/jpn audio exists, but is not set as the default
    if default_audio:
        jp_au = [tr for tr in audio_tracks if tr["language"] in ["jp", "jpn"]]
        if jp_au and not default_audio[0]["language"].startswith("jp"):
            warnings.append(
                "Default audio track not set to jpn, even though it exists!")
    active_sub = None
    if default_sub:
        active_sub = default_sub[0]
    elif implicit_sub:
        active_sub = implicit_sub[0]
    if active_sub:
        en_sub = [tr for tr in sub_tracks if tr["language"] in ["en", "eng"]]
        if en_sub and not active_sub["language"].startswith("en"):
            if "songs" not in en_sub[0]["name"].lower():
                if "signs" not in en_sub[0]["name"].lower():
                    if "s&s" not in en_sub[0]["name"].lower():
                        warnings.append(
                            "Default sub track not set to eng, "
                            "even though it exists!")
        if "songs" in active_sub["name"].lower():
            warnings.append(
                "Default sub track seems to be set to a signs & songs track")
        if "signs" in active_sub["name"].lower():
            warnings.append(
                "Default sub track seems to be set to a signs & songs track")
        if "s&s" in active_sub["name"].lower():
            warnings.append(
                "Default sub track seems to be set to a signs & songs track")
    # print errors and warnings
    if errors or warnings:
        util.cprint(f, "green")
        if warnings or len(errors) > 1 or "No chapters" not in errors[0]:
            for track in info["tracks"]:
                util.cprint(track["id"], "blue")
                util.cprint(f"  name: {track['name']}")
                util.cprint(f"  default: {track['default']}")
                util.cprint(f"  forced: {track['forced']}")
                util.cprint(f"  language: {track['language']}")
        for err in errors:
            util.cprint(err, "red")
        for warn in warnings:
            util.cprint(warn, "yellow")
    return len(errors), len(warnings)


def main():
    parser = argparse.ArgumentParser(
        description="Run a set of linters to find out if the movies are clean")
    parser.add_argument(
        "location", help="Location of the folder to process with subfolders")
    args = parser.parse_args()
    base = os.path.abspath(args.location)
    files = glob("**/*.mkv", root_dir=base, recursive=True)
    if not files:
        print("No movie files found in the specified directory")
        print("Input files are expected to be: .mkv")
        sys.exit()
    files = [os.path.join(base, f) for f in files]
    all_err = 0
    all_warns = 0
    for f in files:
        info = extract_track_info(f)
        if not info:
            info = extract_track_info(f, True)
        if info:
            err, warn = print_track_errors(f, info)
            all_err += err
            all_warns += warn
    util.cprint(f"\nTotal: {all_err} errors and {all_warns} warnings", "blue")


if __name__ == "__main__":
    main()
