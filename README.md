modmov
======

Modify Movies with ease using a collection of single task scripts

# Features

- Very easy to use, zero configuration required
- Clearly defined tasks that do not require an in-depth knowledge of movie tools
- Focus on WHAT you want to do, not HOW you might need to do it
- Most tasks can execute for every movie in a folder, or on a single file
- Remember just one command to modify your movies with ease: modmov

# Tasks

All tasks can be called using the same `modmov` bash script.

- Chapters - Add a list of chapters to an mkv
- Compress - Compress the bitrate of any mkv or mp4
- Defaults - Set the default audio/subtitle track for multiple mkvs
- Extract - Extract a streamable mp4 from any mkv or mp4
- Merge - Merge mkv/mp4 files with srt/ass subtitles to mkv (also called "muxing")

The project is developed exclusively for Linux, although it might also work on Mac.

# Usage

Run `./modmov` without any arguments for help and usage details.
For every task, the following information is presented:

- A brief summary of it's function (also see the list above)
- If the original files will be modified or if a copy will be made (and where)
- The accepted movie input file types
- Additional software that you will need to install on you system (for example ffmpeg)

In short, most tasks are used like this: `./modmov <name> <location>`

To use modmov everywhere on your system, simply create an alias to the bash script.

# Structure

Modmov is essentially a wrapper for more complex movie processing tools.
The tasks are separated into python scripts and are called by the modmov bash script.
The help output of modmov includes a list of the required tools for all the tasks.
The python scripts use subprocess to call ffmpeg/mkvtoolnix commands.
These tools are not included in this project and are covered by different licenses.

# Future

Each time I run into a movie processing related issue or challenge,
the modmov script collection will be expanded with a simplified task to solve it.
This way I do not have to remember a billion different configurations for specific tooling.
You are welcome to add your own specific movie related task to this repository via a PR.

# License

The modmov script collection is created by [Jelmer van Arnhem](https://github.com/Jelmerro).
You may copy and modify the code under the terms of the MIT license.
See the LICENSE file for the exact terms and conditions.
