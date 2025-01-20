import sys
import os

def test_debug_path():
    print("Chemins Python utilisés :", sys.path)
    assert os.path.abspath("src") in sys.path, "Le chemin vers 'src' est absent du PYTHONPATH"
