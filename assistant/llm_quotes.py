# assistant/llm_quotes.py
import subprocess


def get_llm_quote():
    """
    Uses Ollama + tinyllama to generate a motivational quote.
    Make sure Ollama is running and the model is pulled (e.g. `ollama run tinyllama` once beforehand).
    """
    prompt = "Give me a short motivational message for someone who has severe procrastination and is afraid of failure."
    try:
        # "ollama" is an external command-line tool for running language models, and "tinyllama" is the model name.
        result = subprocess.run(
            ["ollama", "run", "tinyllama"],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            check=True,  # Explicitly set check to True to raise an error on non-zero exit
        )
        output = result.stdout.decode("utf-8").strip()
        return output.split("\n")[-1]  # Return the last line in case of verbose output
    except Exception as e:
        raise RuntimeError(f"LLM call failed: {e}")
