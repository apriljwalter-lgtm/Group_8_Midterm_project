# Diagnoses, Admission Type, and Hospital Readmission

**CAI5735 Applied Data Science – Mid-Term Project, Group 8**

Group members: Ryan Merlino, Nikolas Platon, April Walter

## Research question

How is the number of diagnoses related to hospital readmission, and does that relationship differ by admission type (Emergency, Urgent, Elective)?

## Dataset

`diabetes_130.csv` is a 3,000-row sample of the **Diabetes 130-US Hospitals (1999–2008)** dataset from the UCI Machine Learning Repository, provided for this course. Each row is one hospital encounter for a patient with diabetes.

Columns used in this project:

| Column | Description |
|---|---|
| `number_diagnoses` | Number of diagnoses recorded for the encounter |
| `readmitted` | Not readmitted, After 30 days, or Within 30 days |
| `admission_type` | Emergency, Urgent, or Elective |

## What the notebook does

The analysis is in `notebook.py`, a [marimo](https://marimo.io) notebook. It:

1. Loads the data and checks its size
2. Keeps only the columns the question uses
3. Adds computed columns: a readmitted flag (0/1) and a diagnosis group (1-4, 5-6, 7-8, 9+)
4. Filters to Emergency admissions to check the pattern within one admission type
5. Groups by admission type and diagnosis group to calculate readmission rates
6. Sorts the groups by readmission rate
7. Draws a histogram, a boxplot, a scatter plot, and charts comparing admission types

## How to run it

### Option 1: In your browser (nothing to install)

Open the notebook on marimo's website:

https://marimo.app/github.com/apriljwalter-lgtm/Group_8_Midterm_project/blob/main/notebook.py

### Option 2: On your computer

You need [uv](https://docs.astral.sh/uv/) installed.

```
git clone https://github.com/apriljwalter-lgtm/Group_8_Midterm_project.git
cd Group_8_Midterm_project
uv sync
uv run marimo edit notebook.py
```

The notebook opens in your browser. It loads the data from this GitHub repository, so it needs an internet connection.

## Presentation

`slides/Slides.pdf` is the 5-minute class presentation. `slides/make_slides.py` rebuilds the figures and slides from the CSV.

## Files

| File | Purpose |
|---|---|
| `notebook.py` | The marimo analysis notebook |
| `diabetes_130.csv` | The dataset |
| `pyproject.toml`, `uv.lock` | The Python packages the notebook needs |
| `slides/` | Presentation (PDF) and the script that builds it |
| `Notebook.pdf` | PDF export of the notebook for submission |
