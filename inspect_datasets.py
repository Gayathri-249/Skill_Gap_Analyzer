
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

resume_path = DATA_DIR / "resumes" / "Resume" / "Resume.csv"
jobs_path = DATA_DIR / "job_postings" / "postings.csv"
job_skills_path = DATA_DIR / "job_postings" / "jobs" / "job_skills.csv"
onet_dir = DATA_DIR / "onet" / "db_31_0_excel"


def inspect_csv(path, name, sample_rows=5):
    print("\n" + "=" * 70)
    print(f"DATASET: {name}")
    print("=" * 70)

    if not path.exists():
        print(f"FILE NOT FOUND: {path}")
        return

    try:
        # Read a small sample instead of loading a potentially large CSV.
        sample = pd.read_csv(path, nrows=sample_rows, low_memory=False)

        print(f"File: {path}")
        print(f"Sample shape: {sample.shape}")
        print("\nColumns:")
        print(sample.columns.tolist())
        print("\nSample records:")
        print(sample.head().to_string(index=False))

        # Read a larger sample to estimate missing-value patterns.
        larger_sample = pd.read_csv(path, nrows=1000, low_memory=False)
        print("\nMissing values in first 1000 rows:")
        print(larger_sample.isnull().sum().sort_values(
            ascending=False
        ).head(15))

    except Exception as exc:
        print(f"Could not inspect {name}: {exc}")


def inspect_excel(path, name):
    print("\n" + "=" * 70)
    print(f"O*NET FILE: {name}")
    print("=" * 70)

    try:
        preview = pd.read_excel(path, nrows=5)
        print(f"File: {path}")
        print("Columns:", preview.columns.tolist())
        print("\nSample records:")
        print(preview.head().to_string(index=False))
    except Exception as exc:
        print(f"Could not inspect {name}: {exc}")


if __name__ == "__main__":
    inspect_csv(resume_path, "Resume dataset")
    inspect_csv(jobs_path, "Job postings dataset")
    inspect_csv(job_skills_path, "Job skills dataset")

    onet_files = [
        "Occupation Data.xlsx",
        "Essential Skills.xlsx",
        "Knowledge.xlsx",
        "Software Skills.xlsx",
    ]

    for filename in onet_files:
        path = onet_dir / filename
        if path.exists():
            inspect_excel(path, filename)
        else:
            print(f"\nO*NET FILE NOT FOUND: {path}")

    print("\nDataset inspection complete.")
