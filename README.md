# Immich-Tools
A couple of tools to fill in the gaps of published tools to manage offline and untracked files in Immich.

---
### immich-del-offline.py
- script to delete offline files, copied from [Remove Offline Files [Community]](https://immich.app/docs/guides/remove-offline-files/), modified to remove offiline files not owned by admin.

***Dependencies***
-   I needed to install the following dependencies using:
-   `pip install wheel requests halo tabulate tqdm`

***Usage***
-    Enter API key for the admin in order to compile list of offline files (default behaviour)
-    Enter API key for the user who owns the offline files (modified from community version)
---
### move_untracked_files.sh
- script to move untracked files from within Immich directories, out to an alternate location where they can be reviewed or deleted. Immich directory paths are maintained at destination directory in order to distinguish between files located "thumbs" diectory (files generated by Immich and are not unique media) and "library or upload" directories (files which may be unique, and may need to be reimported).

***Dependencies***
- this is a BASH script for use in linux environment
- rsync is used to move files

***Usage***
- give executable permission to the script file
- export the untraked.txt file list from the Immich repair page
- populate the following variables within the script

-  `find="/usr/src/app/upload/"` this will probably be the same for every default immich install
-  `replace="path/to/immich/directories"` populate this with the directory path local to the script filesystem
-  `untracked="/path/to/untracked.txt"` populate this with the untracked.txt file location exported from the immich repair page
-  `destination="/path/to/destination/"` populate this with the destination for where the files should be moved
