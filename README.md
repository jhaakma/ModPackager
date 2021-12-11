# Merlord's Morrowind Mod Packager

## Introduction
This tool allows you to easily package and release Morrowind mods. Multiple mods can be configured for release using a simple yaml file. You can also integrate with a github action (provided) which will let you pass a version number to the mod packager that will trigger a release on Github.

## Features
- Copy files from Morrowind Directory into your repository
- Build local .7z archive of your mod, ready to be released to Nexus etc.
- Commit and push releases to Github
- Create Github release with changelog based on commit messages and .7z archive
- Configure fixed Modified timestamp for plugin and master files

## Requirements:
- Python >=3
- Pip

## Installation
- Run `ModPackager/build.sh` to install dependencies
- For each mod, add a yaml file in the `ModPackager/config/` (see Mod Config File section)
- Add the github action file to your mod repos (see Github Integration section)


## Mod Config File
Each mod needs a config file to determine paths to files etc. Here is an example:

### Example:
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
    timestamps:
        -
            path: TestMod.esp
            timestamp: 1499358234
```
### Config Values

#### mod_name
The name of your mod, used for logging to the console.

#### contents
Each file/folder configured here will be copied from the Morrowind installation directory into the build. It is recommended that you put all your mod assets into unique folders, so you can simply define the folder itself instead of every individual file. For example, put all your mod textures into `Data Files/Textures/{modName}`, your sounds into `Data Files/Sound/{modName}` etc, then set those folders in the config.

Alternatively, if you want to be able to edit your Lua scripts from the Morrowind install folder and have them reflected in your git repo, you can use symlinks instead. However, symlinking the ESP file has been known to cause issues, so you may want to symlink everything else, keep your ESP file separate and add it to `contents` so it gets copied over when doing a release.

#### version_path (Optional)
For lua mods, set this to a `version.txt` file in your lua mod directory (e.g. `Data Files/MWSE/mods/testmod/version.txt`). Mod Packager will update it to reflect the latest release version, and you can then use it for logging etc in your lua code.

#### repo_path
This is the location of the git repo for your mod. Mod Packager will copy the files from `{{repo_path}}/Data Files` into the archive, and if a version is provided, update and push to the remote repo with the new version tag.

#### archive_path (Optional)
This is the path where the 7z archive file will be created locally. If not set, the local archive will not be created.

#### morrowind_path
This is the path to the Morrowind installation folder. This is required if you are updating the version.txt file or are copying files using the `contents` field.

#### timestamps (Optional)
A list of files that need their timestamps reset. This is important for ESM/ESP files as Morrowind uses timestamps for load order and git doesn't store timestamp information. Go to https://www.unixtimestamp.com/ to convert the "Modified" time on your ESP file to a UNIX timestamp.

You should only have to set this once.


## Github Integration
The action file in `GitHubAction/main.yml` will trigger when a commit is pushed with a tag starting with 'v'.
It will create a new release for that version and bundle it into a 7z file

### Steps to configure Github Action
- Copy `GitHubAction/.github/workflows/main.yml` to your repo at `{repo}/.github/workflows/main.yml`
- In `main.yml`, set env.ARCHIVE_NAME to the name of your mod
- Commit and push the `main.yml` file
- When using Mod Packager, pass a version number as a second argument to trigger a release

    e.g. `ModPackager/run.sh myMod v1.0.0`


## Usage

### Local Build
To create a local build, simply navigate to the ModPackager folder and call `run.sh`, passing it the name of a mod config file. E.g:

```
cd C:/Tools/ModPackager
./run.sh testmod
```

This will do the following:
- Copy any files/folders defined in `config.contents` from your Morrowind install directory into your repo directory
- Add the `Data Files` folder from your repo to a .7z file if `config.repo_path` is set

### Github Release
To push a new release to Github, pass a version number as a second argument. The version must start with a `v`, e.g:

```
cd C:/Tools/ModPackager
./run.sh testmod v1.0.1
```

This will do the following:
- Update the version.txt file if configured
- git pull
- Add and commit any local changes
- Create a tag based on the version number
- Push the tag and the commit to github
- If the workflow action is set up in your remote repo, it will be triggered by the tag and create a release on Github

### Set up Alias
It is recommended you create an alias to run.sh in your `~/.bash_profile`, e.g:
```
    # open bash_profile:
    vim ~/.bash_profile

    # add the following line (change path to wherever you installed Mod Packager)
    alias packagemod='C:/Tools/ModPackager/run.sh`
```

You can then run a build from anywhere by calling the packagemod alias, e.g
```
packagemod myMod v1.0.7
```
