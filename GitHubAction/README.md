## Github Packager
This GitHub Action triggers when a commit is pushed with a tag starting with 'v'.
It will create a new release for that version and bundle it into a 7z file

- Step 1: set env.ARCHIVE_NAME to the name of your mod.

- Step 2: Commit the main.yml file in your repo at .github/workflows/main.yml
  (or create it in github via the Actions tab)

- Step 3: Use the ModPackager, passing it a version number (e.g 'v1.0.3') to create a release
  This will trigger the action and create a new Release in Github