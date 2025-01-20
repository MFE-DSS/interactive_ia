import sys
import os

print("PYTHONPATH:", sys.path)
print("Chemin absolu pour src:", os.path.abspath("src"))

try:
    from src.api.llm_handler import LLMHandler
    print("Import réussi : LLMHandler")
except ModuleNotFoundError as e:
    print("Erreur d'import :", e)
