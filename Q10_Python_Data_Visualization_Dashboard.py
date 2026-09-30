"""Q10: Clean student marks CSV, summarize subjects and export three charts.

Install: python -m pip install pandas matplotlib
Expected columns: enrollment,name,Subject1,Subject2,...
Missing marks are filled with that subject's mean; invalid/out-of-range marks
are treated as missing. Charts and CSV outputs are written to the chosen folder.
"""
from pathlib import Path
import sys


def main():
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
    except ImportError:
        print("Install dependencies: python -m pip install pandas matplotlib")
        return

    source = Path(input("Marks CSV path: ").strip())
    output = Path(input("Output folder: ").strip())
    if not source.is_file():
        print("CSV file not found."); return
    output.mkdir(parents=True, exist_ok=True)

    try:
        df = pd.read_csv(source)
        required = {"enrollment", "name"}
        if not required.issubset(df.columns):
            raise ValueError("CSV must contain enrollment and name columns")
        subjects = [col for col in df.columns if col not in required]
        if not subjects:
            raise ValueError("No subject columns found")
        for subject in subjects:
            df[subject] = pd.to_numeric(df[subject], errors="coerce")
            df.loc[~df[subject].between(0, 100), subject] = float("nan")
            mean = df[subject].mean()
            df[subject] = df[subject].fillna(0 if pd.isna(mean) else mean)
        df.to_csv(output / "cleaned_marks.csv", index=False)

        summary = pd.DataFrame({
            "subject": subjects,
            "average": [df[s].mean() for s in subjects],
            "minimum": [df[s].min() for s in subjects],
            "maximum": [df[s].max() for s in subjects],
            "std_dev": [df[s].std(ddof=0) for s in subjects],
        })
        summary.to_csv(output / "summary.csv", index=False)

        all_marks = df[subjects].to_numpy().flatten()
        bins = [0, 40, 50, 60, 70, 80, 90, 101]
        labels = ["0–39", "40–49", "50–59", "60–69", "70–79", "80–89", "90–100"]
        grade = pd.cut(all_marks, bins=bins, labels=labels, right=False, include_lowest=True)
        grade.value_counts(sort=False).plot(kind="bar")
        plt.title("Grade Distribution"); plt.xlabel("Marks"); plt.ylabel("Count")
        plt.tight_layout(); plt.savefig(output / "grade_distribution.png"); plt.close()

        summary.plot(x="subject", y="average", kind="bar", legend=False)
        plt.title("Subject-wise Average"); plt.ylabel("Average Marks")
        plt.tight_layout(); plt.savefig(output / "subject_average.png"); plt.close()

        df["total"] = df[subjects].sum(axis=1)
        top = df.nlargest(10, "total").sort_values("total")
        plt.figure(figsize=(9, 5))
        plt.barh(top["name"].astype(str), top["total"])
        plt.title("Top Performers"); plt.xlabel("Total Marks")
        plt.tight_layout(); plt.savefig(output / "top_performers.png"); plt.close()

        for name in ("cleaned_marks.csv", "summary.csv", "grade_distribution.png",
                     "subject_average.png", "top_performers.png"):
            print(output / name)
    except (OSError, ValueError, Exception) as exc:
        print("Processing error:", exc)


if __name__ == "__main__":
    main()
