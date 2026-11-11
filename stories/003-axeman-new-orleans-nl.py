"""Dutch version of 003-axeman-new-orleans: same scenes, Dutch narration."""
import importlib.util, os

_spec = importlib.util.spec_from_file_location(
    "_en", os.path.join(os.path.dirname(os.path.abspath(__file__)), "003-axeman-new-orleans.py"))
_en = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_en)

SCENES = _en.SCENES
