import importlib
from datetime import datetime
from pathlib import Path

AGENTS_DIR = Path("agents")
OUTPUTS_DIR = Path("outputs")

def load_agents():
    """Import every valid agent module from the agents/ folder."""
    agents = []

    # Look through all Python files in agents/
    for path in sorted(AGENTS_DIR.glob("*.py")):
        # Skip private helper files like __init__.py
        if path.name.startswith("_"):
            continue

        # Import the file as a Python module, e.g. agents.googl_stock
        module = importlib.import_module(f"agents.{path.stem}")

        # Only keep modules that define NAME and run()
        if hasattr(module, "NAME") and hasattr(module, "run"):
            agents.append(module)
        else:
            print(f"[skip] {path.name} (missing NAME or run)")

    return agents


def main():
    """Load all agents, run them, and save their outputs."""
    # Create the outputs/ folder if it doesn't exist yet.
    OUTPUTS_DIR.mkdir(exist_ok=True)

    # Run every agent we found.
    for agent in load_agents():
        print(f"[run]  {agent.NAME}")

        try:
            # Call the agent's run() function.
            output = agent.run()

            # Create a timestamped filename like:
            # outputs/weather-brief-2026-07-03_08-00-39.md
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            out_path = OUTPUTS_DIR / f"{agent.NAME}-{timestamp}.md"

            # Write the returned text to disk.
            out_path.write_text(output)

            print(f"[ok]   {agent.NAME} -> {out_path}")
        except Exception as e:
            # If one agent fails, log it and continue with the others.
            print(f"[fail] {agent.NAME}: {e}")


if __name__ == "__main__":
    main()
