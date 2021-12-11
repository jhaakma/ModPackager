# Merlord's Morrowind Mod Packager

## Introduction
This tool allows you to easily package and release Morrowind mods by running a python script. Multiple mods can be configured by creating a yaml file for each, and passing the file name to the script. You can also integrate with a github action (provided) which will let you pass a version number to the mod packager that will trigger a release on Github.

## Requirements:
- Python >=3
- Pip

## Installation
- Run `ModPackager/build.sh` to install dependencies
- For each mod, add a yaml file in the `ModPackager/config/` (see Mod Config File section)

- Add the github action file to your mod repos (see below)

## Mod Config File
Each mod needs a config file to determine paths to files etc. Here is an example:

### config/testmod.yaml:
```yaml
    mod_name: My Test Mod
    contents:
    - TestMod.esp
    - MWSE/mods/testmod
    - Meshes/testmod
    - Textures/myTexture.dds
    version_path: Data Files/MWSE/mods/testmod/version.txt
    repo_path: C:/ModReleases/TestMod/master
    archive_path: C:/ModReleases/TestMod/TestMod.7z
    morrowind_path: C:/games/Morrowind
```
### mod_name
The name of your mod, used for logging to the console.

### contents
Each file/folder configured here will be copied from the Morrowind installation directory into the build. It is recommended that you put all your mod assets into unique folders, so you can simply define the folder itself instead of every individual file. For example, put all your mod textures into `Data Files/Textures/{modName}`, your sounds into `Data Files/Sound/{modName}` etc, then set those folders in the config.

Alternatively, if you want to be able to edit your Lua scripts from the Morrowind install folder and have them reflected in your git repo, you can use symlinks instead. However, symlinking the ESP file has been known to cause issues, so you may want to symlink everything else, keep your ESP file separate and add it to `contents` so it gets copied over when doing a release.

### version_path (Optional)
For lua mods, set this to a `version.txt` file in your lua mod directory (e.g. `Data Files/MWSE/mods/testmod/version.txt`). Mod Packager will update it to reflect the latest release version, and you can then use it for logging etc in your lua code.

### repo_path
This is the location of the git repo for your mod. Mod Packager will copy the files from `{{repo_path}}/Data Files` into the archive, and if a version is provided, update and push to the remote repo with the new version tag.

### archive_path (Optional)
This is the path where the 7z archive file will be created locally. If not set, the local archive will not be created.

### morrowind_path
This is the path to the Morrowind installation folder. This is required if you are updating the version.txt file or are copying files using the `contents` field.

## Github Integration
The action file in `GitHubAction/main.yml` will trigger when a commit is pushed with a tag starting with 'v'.
It will create a new release for that version and bundle it into a 7z file

- Copy `GitHubAction/.github/workflows/main.yml` to your repo at `{repo}/.github/workflows/main.yml`
- In `main.yml`, set env.ARCHIVE_NAME to the name of your mod
- Commit and push the `main.yml` file
- When using Mod Packager, pass a version number as a second argument to trigger a release

    e.g. `ModPackager/run.sh myMod v1.0.0`

## Usage
- Install the mod packager (see the `Installation` section)
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

- It is recommended you create an alias to run.sh in your `~/.bash_profile`, e.g:
    ```
    # open bash_profile:
    vim ~/.bash_profile

    # add the following line (change path to wherever you installed Mod Packager)
    alias packagemod='C:/Tools/ModPackager/run.sh`
    ```
