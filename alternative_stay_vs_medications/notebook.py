import marimo

__generated_with = "0.14.0"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"""
    # CAI5735 Mid-Term Project: Diabetes 130-US Hospitals

    **Group members:** Ryan Merlino, April Walter, Nikolas Platon

    **GitHub repository:** https://github.com/ryanmerlino21-debug/diabetes-readmission

    ## Research question

    > **How is the length of a hospital stay (`time_in_hospital`) related to the number of
    > medications given (`num_medications`), and does that relationship differ depending on
    > whether and when the patient was readmitted (`readmitted`)?**

    The question uses three columns: two numeric (`time_in_hospital`, `num_medications`) and one
    categorical (`readmitted`).

    **Dataset:** Diabetes 130-US Hospitals for Years 1999-2008 (UCI Machine Learning Repository,
    https://doi.org/10.24432/C5230J; Strack et al., 2014). The course provides a simplified sample
    of 3,000 stays with 10 columns.
    """)
    return


@app.cell
def _():
    # GitHub repository: https://github.com/ryanmerlino21-debug/diabetes-readmission
    # (Required by the assignment: link to the repo as a comment in the notebook.)
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import stats

    # Imports live in one cell so every later cell can use them.
    return mo, np, pd, plt, stats


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Load and inspect the data
    Load the CSV and check its size, types and missing values before analysing anything.
    """)
    return


@app.cell
def _(pd):
    df = pd.read_csv("../diabetes_130.csv")
    # Order readmission categories from best to worst outcome so plots read left to right.
    readmit_order = ["Not readmitted", "After 30 days", "Within 30 days"]
    df["readmitted"] = pd.Categorical(df["readmitted"], categories=readmit_order, ordered=True)
    print("Shape:", df.shape)
    print("Missing values:", int(df.isna().sum().sum()))
    print(df.dtypes)
    df.head()
    return df, readmit_order


@app.cell
def _(mo):
    mo.md(r"""
    ## 2. Data operations
    ### 2a. Filtering by column values
    We keep only the three columns tied to the research question, and filter to stays that
    are plausible for the `num_medications` distribution (the 99th percentile cutoff removes a
    handful of extreme outliers, e.g. 75 medications, that would dominate the scatter plot and
    correlation). We also show a filter on a categorical value (emergency admissions).
    """)
    return


@app.cell
def _(df):
    med_cutoff = df["num_medications"].quantile(0.99)
    core = df[["time_in_hospital", "num_medications", "readmitted"]]
    filtered = core[core["num_medications"] <= med_cutoff]
    print(f"99th percentile of num_medications: {med_cutoff:.0f}")
    print(f"Rows kept after filtering: {len(filtered)} of {len(df)}")

    emergency = df[df["admission_type"] == "Emergency"]
    print(f"Emergency admissions: {len(emergency)}")
    filtered.head()
    return core, filtered, med_cutoff


@app.cell
def _(mo):
    mo.md(r"""
    ### 2b. Sorting
    Sort by length of stay (longest first) to see which stays are the extremes and what
    their medication counts and outcomes look like.
    """)
    return


@app.cell
def _(filtered):
    filtered.sort_values(["time_in_hospital", "num_medications"], ascending=False).head(10)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 2c. Grouping by a categorical variable
    Group by `readmitted` to compare stay length and medication count across outcomes.
    """)
    return


@app.cell
def _(filtered):
    summary = (
        filtered.groupby("readmitted", observed=True)
        .agg(
            stays=("time_in_hospital", "size"),
            mean_days=("time_in_hospital", "mean"),
            median_days=("time_in_hospital", "median"),
            mean_meds=("num_medications", "mean"),
            median_meds=("num_medications", "median"),
        )
        .round(2)
    )
    summary
    return (summary,)


@app.cell
def _(mo):
    mo.md(r"""
    ### 2d. Adding a computed column
    `meds_per_day` = medications divided by days in hospital. It normalises medication
    burden by stay length, so we can tell whether longer stays simply mean more medications
    or whether patients are given medications at a higher *rate*.
    """)
    return


@app.cell
def _(filtered):
    data = filtered.copy()
    data["meds_per_day"] = data["num_medications"] / data["time_in_hospital"]
    print(data.groupby("readmitted", observed=True)["meds_per_day"].agg(["mean", "median"]).round(2))
    data.head()
    return (data,)


@app.cell
def _(mo):
    mo.md(r"""
    ## 3. Visualizations
    ### 3a. Histogram: distribution of length of stay
    A histogram shows the shape of `time_in_hospital`: whether it is symmetric or skewed,
    which tells us whether to prefer medians and rank-based tests.
    """)
    return


@app.cell
def _(data, plt):
    fig_hist, ax_hist = plt.subplots(figsize=(7, 4))
    ax_hist.hist(data["time_in_hospital"], bins=range(1, 16), color="#2a6f97", edgecolor="white")
    ax_hist.set_title("Distribution of Length of Hospital Stay")
    ax_hist.set_xlabel("Time in hospital (days)")
    ax_hist.set_ylabel("Number of stays")
    fig_hist.tight_layout()
    fig_hist.savefig("fig_hist.png", dpi=200)
    fig_hist
    return


@app.cell
def _(mo):
    mo.md(r"""
    The distribution is right-skewed: most stays are short (1-6 days) with a long tail up to
    14 days. Because of this skew, medians and the Kruskal-Wallis test are appropriate below.

    ### 3b. Boxplot: number of medications by readmission status
    A boxplot compares the spread and median of `num_medications` across the three outcomes.
    """)
    return


@app.cell
def _(data, plt, readmit_order):
    fig_box, ax_box = plt.subplots(figsize=(7, 4))
    _groups = [data.loc[data["readmitted"] == g, "num_medications"] for g in readmit_order]
    _bp = ax_box.boxplot(_groups, tick_labels=readmit_order, patch_artist=True, medianprops={"color": "black"})
    for _patch, _c in zip(_bp["boxes"], ["#8fb8d8", "#2a6f97", "#d1495b"]):
        _patch.set_facecolor(_c)
    ax_box.set_title("Number of Medications by Readmission Status")
    ax_box.set_xlabel("Readmission status")
    ax_box.set_ylabel("Number of medications")
    fig_box.tight_layout()
    fig_box.savefig("fig_box.png", dpi=200)
    fig_box
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 3c. Scatter plot: medications vs. length of stay
    A scatter plot with a fitted line shows the relationship between the two numeric
    variables. Points are jittered slightly horizontally because `time_in_hospital` is
    an integer and points would otherwise overlap.
    """)
    return


@app.cell
def _(data, np, plt, stats):
    _rng = np.random.default_rng(0)
    _x = data["time_in_hospital"].to_numpy()
    _y = data["num_medications"].to_numpy()
    fig_sc, ax_sc = plt.subplots(figsize=(7, 4.5))
    ax_sc.scatter(_x + _rng.uniform(-0.25, 0.25, len(_x)), _y, s=8, alpha=0.3, color="#2a6f97")
    _fit = stats.linregress(_x, _y)
    _xs = np.array([_x.min(), _x.max()])
    ax_sc.plot(_xs, _fit.intercept + _fit.slope * _xs, color="#d1495b", lw=2,
               label=f"Fit: +{_fit.slope:.2f} meds/day (r = {_fit.rvalue:.2f})")
    ax_sc.set_title("Medications vs. Length of Stay")
    ax_sc.set_xlabel("Time in hospital (days)")
    ax_sc.set_ylabel("Number of medications")
    ax_sc.legend()
    fig_sc.tight_layout()
    fig_sc.savefig("fig_scatter.png", dpi=200)
    print(f"Overall Pearson r = {_fit.rvalue:.3f}, p = {_fit.pvalue:.2e}, slope = {_fit.slope:.3f}")
    fig_sc
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 3d. Group differences: the stay-vs-medications relationship within each readmission group
    We fit a separate regression line for each readmission group to see whether the
    relationship changes across groups, and also compute each group's correlation and slope.
    """)
    return


@app.cell
def _(data, np, pd, plt, readmit_order, stats):
    _colors = {"Not readmitted": "#8fb8d8", "After 30 days": "#2a6f97", "Within 30 days": "#d1495b"}
    fig_grp, ax_grp = plt.subplots(figsize=(7, 4.5))
    _rows = []
    for _g in readmit_order:
        _sub = data[data["readmitted"] == _g]
        _fit = stats.linregress(_sub["time_in_hospital"], _sub["num_medications"])
        _rows.append({"group": _g, "n": len(_sub), "pearson_r": round(_fit.rvalue, 3),
                      "slope_meds_per_day": round(_fit.slope, 3), "p_value": _fit.pvalue})
        _xs = np.array([1, 14])
        ax_grp.plot(_xs, _fit.intercept + _fit.slope * _xs, color=_colors[_g], lw=2.5,
                    label=f"{_g} (r = {_fit.rvalue:.2f}, slope = {_fit.slope:.2f})")
    ax_grp.set_title("Medications vs. Length of Stay, by Readmission Status")
    ax_grp.set_xlabel("Time in hospital (days)")
    ax_grp.set_ylabel("Number of medications (fitted)")
    ax_grp.legend(fontsize=8)
    fig_grp.tight_layout()
    fig_grp.savefig("fig_groups.png", dpi=200)
    group_fits = pd.DataFrame(_rows)
    print(group_fits.to_string(index=False))
    fig_grp
    return (group_fits,)


@app.cell
def _(mo):
    mo.md(r"""
    ## 4. Statistical tests
    * **Spearman correlation** (robust to skew) for stay length vs. medications.
    * **Kruskal-Wallis** tests whether stay length / medications differ across readmission groups
      (non-parametric, since both are skewed).
    * **Fisher z-test** comparing the Pearson correlations of the readmitted-within-30-days and
      not-readmitted groups, to test whether the relationship strength differs.
    """)
    return


@app.cell
def _(data, np, stats):
    _rho, _p = stats.spearmanr(data["time_in_hospital"], data["num_medications"])
    print(f"Spearman rho = {_rho:.3f} (p = {_p:.2e})")

    for _col in ["time_in_hospital", "num_medications", "meds_per_day"]:
        _samples = [g[_col].to_numpy() for _, g in data.groupby("readmitted", observed=True)]
        _h, _kp = stats.kruskal(*_samples)
        print(f"Kruskal-Wallis {_col}: H = {_h:.2f}, p = {_kp:.2e}")

    _a = data[data["readmitted"] == "Not readmitted"]
    _b = data[data["readmitted"] == "Within 30 days"]
    _ra = stats.pearsonr(_a["time_in_hospital"], _a["num_medications"])[0]
    _rb = stats.pearsonr(_b["time_in_hospital"], _b["num_medications"])[0]
    _z = (np.arctanh(_ra) - np.arctanh(_rb)) / np.sqrt(1 / (len(_a) - 3) + 1 / (len(_b) - 3))
    _pz = 2 * (1 - stats.norm.cdf(abs(_z)))
    print(f"Fisher z (Not readmitted r={_ra:.3f} vs Within 30 days r={_rb:.3f}): z = {_z:.2f}, p = {_pz:.3f}")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 5. Conclusions
    * **Stay length and medications are positively related** (Pearson r = 0.45, Spearman
      rho = 0.45): each additional hospital day is associated with roughly 1.1 more medications.
    * **The relationship is similar in every readmission group** (comparable slopes and
      correlations; the Fisher z-test between groups finds no strong difference), so
      readmission status does not meaningfully change *how* stay length and medications relate.
    * **Level differs by group even though the relationship doesn't:** patients readmitted within
      30 days had longer stays and received more medications on average than those never readmitted
      (Kruskal-Wallis significant for both), consistent with sicker patients having both longer
      stays and more medications and a higher chance of quick return.
    * **Limitations:** observational data, a simplified 3,000-row sample, no severity/comorbidity
      information, and medication count is a count of drugs, not doses. These results show
      association, not causation.
    """)
    return


if __name__ == "__main__":
    app.run()
