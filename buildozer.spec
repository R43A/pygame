[app]

# (str) Title of your application
title = Pong

# (str) Package name
package.name = pong

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py lives
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
requirements = python3,kivy,pygame

# (list) Application additional configuration
osx.python_version = 3

# (str) Application version
version = 1.0

# (str) Regular expression for versioning
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py