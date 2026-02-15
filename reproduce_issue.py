import os
import sys
import time

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from src.core.lyra_client import LyraClient


def test_ollama():
    print("Testing LyraClient with Ollama...")

    # Force mock config if needed, or just rely on LyraClient loading it
    # But to be sure, let's pass arguments explicitly first

    ollama_url = "http://localhost:11434"

    # Use list_models to find one

    client = LyraClient(provider="ollama", ollama_url=ollama_url)

    print("Fetching models...")
    models = client.list_models()
    print(f"Models found: {models}")

    if not models:
        print("No models found. is Ollama running?")
        return

    client.model = models[0]  # Use first available model
    print(f"Using model: {client.model}")

    print("Asking 'prova'...")
    start = time.time()
    response = client.ask("prova")
    end = time.time()

    print(f"Response ({end - start:.2f}s): {response}")


if __name__ == "__main__":
    test_ollama()
