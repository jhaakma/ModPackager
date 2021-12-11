# Merlord's Morrowind Mod Packager

## Introduction
This tool allows you to easily package and release Morrowind mods by running a python script. Multiple mods can be configured by creating a yaml file for each, and passing the file name to the script. You can also integrate with a github action (provided) which will let you pass a version number to the mod packager that will trigger a release on Github.

## Requirements:
- Python >=3
- Pip

## Installation
- Run `ModPackager/build.sh` to install dependencies
- For each mod, add a file in the `ModPackager/config/` folder. The `exampleConfig.yaml` shows which values need to be set
- Add the github action file to your mod repos (see below)

## Github Integration
The action file in `GitHubAction/main.yml` will trigger when a commit is pushed with a tag starting with 'v'.
It will create a new release for that version and bundle it into a 7z file

- Copy `GitHubAction/main.yml` to your repo at `repo/.github/workflows/main.yml`
- In `main.yml`, set env.ARCHIVE_NAME to the name of your mod.
- Commit and push the `main.yml` file
- Pass a version number when using the Mod Packager to trigger a Github release
    e.g. `ModPackager/run.sh myMod v1.0.0`

## Usage
- To create a local build, simply navigate to the ModPackager folder and call `run.sh`, passing it the name of a mod config file. E.g:
    ```
        cd C:/Tools/ModPackager
        ./run.sh testmod
    ```
    Output:
    ```
        Starting Build for Test Mod
        Copying files from Morrowind to repo
        Removed file at C:/mods/testMod/Data Files/TestMod.esp
        Copied file from 'C:/games/Morrowind/Morrowind/Data Files/TestMod.esp' to 'C:/mods/testMod/Data Files/TestMod.esp
        Removed folder at C:/mods/testMod/Data Files/MWSE/mods/mer/testmod
        Copied folder from 'C:/games/Morrowind/Morrowind/Data Files/MWSE/mods/mer/testmod' to 'C:/mods/testMod/Data Files/MWSE/mods/mer/testmod
        Copy successful
        Creating 7z file
        Archive created successfully at 'C:/mods/testMod/TestMod.7z'
    ```