"""Dutch version of 002-murder-castle: same scenes, Dutch narration."""
import importlib.util, os

_spec = importlib.util.spec_from_file_location(
    "_en", os.path.join(os.path.dirname(os.path.abspath(__file__)), "002-murder-castle.py"))
_en = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_en)

SCENES = _en.SCENES
