[app]
# (str) Title of your application
title = Ruiz Assistant

# (str) Package name
package.name = ruizassistant

# (str) Package domain (needed for android)
package.domain = org.ruiz

# (str) Source code where the main.py is located
source.dir = .

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
requirements = python3,kivy,pyjnius

# (str) Supported orientation
orientation = portrait

# (list) Permissions
android.permissions = RECORD_AUDIO, INTERNET, CALL_PHONE, SEND_SMS

# (str) Minimum Android API to support
android.minapi = 21

# (str) Android API the app will be built against
android.api = 33

# (list) Android architectures
android.arch = armeabi-v7a, arm64-v8a

# (str) Presplash image
# presplash.filename = %(source.dir)s/data/presplash.png

# (bool) Copy the application instead of symlink
# (default False)
copy_source = False
