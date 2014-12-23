from distutils.core import setup
import py2exe
options={
        "bundle_files":1,
        "compressed":1,
        }
setup(
        options={"py2exe":options},
        zipfile=None,
        console=["main.py"]
        )
