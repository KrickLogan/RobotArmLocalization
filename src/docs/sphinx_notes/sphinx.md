# Sphinx notes

- init files caused problems for the sphinx-autodoc -o command which generates rst files for each module. I just removed all the files I didn't want rst files for and ran it.
- modify the sphinx-autodoc -o command to run on files from the utilities folder (./utilities/ eg)
- in conf file, add the utilities folder to the path
- haven't modified them to be classes yet
- add the name of each rst file to the modules.rst file
- Had to adjust the imports in each of the files which is creating a problem. Sphinx doesn't want: ` import arm_localizer.object_detector`, it will keep looking for the arm_localizer module. remove this. This does cause a problem for the package though. quick fix is to just remove the ```arm_localizer``` prefix, run the sphinx-autodoc command, and then replace them. This is something that should be solved using the init files inside the package.


