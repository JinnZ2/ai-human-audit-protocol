import pathlib
import sys

# physics/ modules that are also runnable as scripts from within physics/
# use bare sibling imports (e.g. `from reference_frame import ...`).
# Adding physics/ to sys.path lets pytest resolve those the same way a direct
# invocation from physics/ would, without modifying the CC0 source files.
_physics = str(pathlib.Path(__file__).parent / "physics")
if _physics not in sys.path:
    sys.path.insert(0, _physics)
