from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


def run_script(script_name):
    """Run a Python script from the scripts directory."""
    script_path = SCRIPTS_DIR / script_name

    if not script_path.exists():
        print(f"⚠️ Skipped: {script_name} not found")
        return

    print(f"\n▶ Running {script_name}...")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT
    )

    if result.returncode == 0:
        print(f"✅ Completed: {script_name}")
    else:
        print(f"❌ Failed: {script_name}")


def main():
    """Run the main Mutual Fund Analytics data pipeline."""

    scripts = [
        "data_ingestion.py",
        "day2_clean_and_load.py",
    ]

    for script in scripts:
        run_script(script)

    print("\n✅ Mutual Fund Analytics pipeline completed.")


if __name__ == "__main__":
    main()