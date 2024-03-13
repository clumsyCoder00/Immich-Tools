# Immich-Tools
A couple of tools to fill in the gaps of published tools to manage offline and untracked files in Immich.

#immich-del-oofline.py
- script to delete offline files, copied from [Remove Offline Files [Community]](https://immich.app/docs/guides/remove-offline-files/), modified to remove offiline files not owned by admin.
- Dependencies
-   I needed to install the following dependencies using:
-   `pip install wheel requests halo tabulate tqdm`

- Usage
-    Enter API key for the admin in order to compile list of offline files (default behaviour)
-    Enter API key for the user who owns the offline files (modified from community version)
