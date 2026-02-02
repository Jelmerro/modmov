modmov
======

Modify Movies with ease using a collection of single task scripts

# Features

- Very easy to use, zero configuration required
- Clearly defined tasks that do not require an in-depth knowledge of movie tools
- Focus on WHAT you want to do, not HOW you might need to do it
- Most tasks can execute for every movie in a folder, or on a single file
- Remember just one command to modify your movies with ease: modmov

All tasks can be called using the same `modmov` Python script:

- Chapters - Add a list of chapters to an mkv
- Compress - Compress the bitrate of any mkv or mp4
- Concat - Concatenate all given movies into a single mp4
- Defaults - Set the default audio/subtitle track for multiple mkvs
- Extract - Extract a streamable mp4 from any mkv or mp4
- Merge - Merge mkv/mp4 files with srt/ass/ssa/mks/sub subtitles to mkv (muxing)
- Lint - Check for common errors in movie files by running a set of linters

## Install

### Pip

```bash
pip install --user -I git+https://github.com/Jelmerro/modmov
```

### Python

Download or clone the repo, then run `python modmov.py` directly.

### [Github](https://github.com/Jelmerro/modmov/releases)

Download a stable installer or executable for your platform from Github.

### [Fedora](https://jelmerro.nl/fedora)

I host a custom Fedora repository that you can use for automatic updates.

```bash
sudo dnf config-manager addrepo --from-repofile=https://jelmerro.nl/fedora/jelmerro.repo
sudo dnf install modmov
```

## Contribute

You can support my work on [ko-fi](https://ko-fi.com/Jelmerro) or [Github sponsors](https://github.com/sponsors/Jelmerro).
Another way to help is to report issues or suggest new features.
Please try to follow recommendations by flake8 and pylint when developing.
For an example vimrc that can auto-format based on the included linters,
you can check out my personal [vimrc](https://github.com/Jelmerro/vimrc).

## Building

To create your own builds you can use [jfpm](https://github.com/Jelmerro/jfpm).
Please clone or download both this repo and jfpm, then run `../jfpm/release_py_deps.sh`.
This will build releases for various platforms and output them to `dist`.

# Usage

Run `modmov` without any arguments for help and usage details.
For every task, the following information is presented:

- A brief summary of it's function (also see the list above)
- If the original files will be modified or if a copy will be made (and where)
- The accepted movie input file types
- Additional software that you will need to install on you system (for example ffmpeg)

In short, most tasks are used like this: `modmov <name> <location>`
