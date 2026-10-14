"""Run a B&W case's art script in the DETAILED COLOUR style: python3 art_color.py NN [scene ...] -> work/art-NN-color.
Uses dkit (detailed characters + colour scenery) and, if present, art_caseNN_color.py (hand-painted plates)."""
import os, sys, importlib
os.environ["TW_ART_SUFFIX"] = "-color"
import dkit
n = int(sys.argv[1]); want = [a for a in sys.argv[2:] if not a.startswith("--")]
A = importlib.import_module(f"art_case{n:02d}")
try: importlib.import_module(f"art_case{n:02d}_color").apply(A)
except ModuleNotFoundError as e:
    if f"art_case{n:02d}_color" not in str(e): raise
from layers import save_layers
J = [j for j in A.jobs() if not want or j["name"] in want]
save_layers(A.OUT, J, dkit.make_ink)
