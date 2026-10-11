"""Builds figures and Slides.pptx for the Group 8 presentation. Run from the slides/ folder."""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

NAMES = "Ryan Merlino, April Walter, Nikolas Platon"
NAVY = RGBColor(0x12, 0x2B, 0x55)
df = pd.read_csv("../diabetes_130.csv")
df["flag"] = (df["readmitted"] != "Not readmitted").astype(int)
df["dx_group"] = pd.cut(df["number_diagnoses"], [0, 4, 6, 8, 99], labels=["1-4", "5-6", "7-8", "9+"])
adm = ["Elective", "Urgent", "Emergency"]
out = ["Not readmitted", "After 30 days", "Within 30 days"]

def save(name):
    plt.tight_layout(); plt.savefig(name, dpi=200); plt.close()

plt.figure(figsize=(7, 4.2))
sns.histplot(data=df, x="number_diagnoses", discrete=True, color="#2a6f97")
plt.title("Distribution of Number of Diagnoses per Encounter")
plt.xlabel("Number of diagnoses"); plt.ylabel("Number of patients"); save("fig1.png")

plt.figure(figsize=(7, 4.2))
sns.boxplot(data=df, x="readmitted", y="number_diagnoses", order=out, palette=["#8fb8d8", "#2a6f97", "#d1495b"], hue="readmitted", legend=False)
plt.title("Number of Diagnoses by Readmission Outcome")
plt.xlabel("Readmission outcome"); plt.ylabel("Number of diagnoses"); save("fig2.png")

r = df.groupby("number_diagnoses")["flag"].mean().mul(100).reset_index()
r = r[r["number_diagnoses"].between(2, 9)]
plt.figure(figsize=(7, 4.2))
sns.scatterplot(data=r, x="number_diagnoses", y="flag", s=90, color="#2a6f97")
plt.title("Readmission Rate by Number of Diagnoses")
plt.xlabel("Number of diagnoses"); plt.ylabel("Readmission rate (%)"); plt.ylim(0, 60); save("fig3.png")

g = df.groupby(["admission_type", "dx_group"], observed=True)["flag"].mean().mul(100).reset_index()
plt.figure(figsize=(7, 4.2))
sns.lineplot(data=g, x="dx_group", y="flag", hue="admission_type", hue_order=adm, marker="o")
plt.title("Readmission Rate by Number of Diagnoses and Admission Type")
plt.xlabel("Number of diagnoses (grouped)"); plt.ylabel("Readmission rate (%)"); plt.ylim(0, 60)
plt.legend(title="Admission type"); save("fig4.png")

prs = Presentation(); prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]

def text(s, t, x, y, w, h, size=22, bold=False, color=None):
    tf = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
    tf.word_wrap = True
    for i, line in enumerate(t if isinstance(t, list) else [t]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line; p.font.size = Pt(size); p.font.bold = bold; p.space_after = Pt(10)
        if color: p.font.color.rgb = color

def slide(title):
    s = prs.slides.add_slide(blank)
    text(s, title, 0.6, 0.35, 12, 1, 32, True, NAVY)
    text(s, NAMES + "  |  CAI5735 Mid-Term  |  Group 8", 0.6, 6.95, 12, 0.4, 12)
    return s

def fig(title, img, bullets):
    s = slide(title)
    s.shapes.add_picture(img, Inches(0.5), Inches(1.6), width=Inches(7.4))
    text(s, bullets, 8.2, 1.8, 4.7, 5, 20)

s = slide("Diagnoses, Admission Type, and Readmission")
text(s, ["Diabetes 130-US Hospitals (1999-2008)", NAMES, "CAI5735: Applied Data Science in Health"], 0.6, 2.2, 12, 3, 26)
s = slide("Research Question")
text(s, ["How is the number of diagnoses related to hospital readmission, and does that relationship differ by admission type (Emergency, Urgent, Elective)?",
         "Columns: number_diagnoses, readmitted, admission_type"], 0.6, 1.8, 12, 4, 28)
s = slide("Dataset")
text(s, ["3,000 hospital stays of patients with diabetes (course sample, no missing values)",
         "Source: UCI Machine Learning Repository; Strack et al. (2014), doi:10.24432/C5230J",
         "number_diagnoses: diagnoses recorded for the stay",
         "readmitted: not readmitted (60%), after 30 days (31%), within 30 days (9%)",
         "admission_type: Emergency (57%), Elective (22%), Urgent (21%)"], 0.6, 1.5, 12, 5, 22)
s = slide("Analysis Process")
text(s, ["1. Kept the three relevant columns",
         "2. Computed columns: readmitted flag (0/1) and diagnosis group (1-4, 5-6, 7-8, 9+)",
         "3. Filtered to Emergency admissions as a check within one type",
         "4. Grouped by admission type and diagnosis group; sorted by readmission rate",
         "5. Visualized distribution, outcome differences, and group trends"], 0.6, 1.5, 12, 5, 24)
fig("Most stays have many diagnoses", "fig1.png", ["Most common value is 9 (1,376 of 3,000 stays)", "Likely a recording cap, so heavy cases may be undercounted"])
fig("Readmitted patients have more diagnoses", "fig2.png", ["Mean diagnoses: 7.0 not readmitted vs 7.7 readmitted (either timing)"])
fig("Readmission rises with diagnoses", "fig3.png", ["Rate climbs from 14-23% at 2-3 diagnoses to 46% at 9", "Overall: 40.0% readmitted"])
fig("Same pattern in every admission type", "fig4.png", ["1-4 dx: 24.6% overall; 9+ dx: 46.0%", "Elective is lowest in every group (34.1% overall vs 41.4% Urgent, 41.8% Emergency)", "Emergency-only check shows the same rise"])
s = slide("Key Takeaways")
text(s, ["More diagnoses means higher readmission, leveling off after about 7",
         "The pattern holds across Elective, Urgent, and Emergency admissions; Elective is consistently lower",
         "Limits: association not causation; many stays have exactly 9 diagnoses; small subgroups (Urgent 1-4 has 74 patients)"], 0.6, 1.6, 12, 5, 26)
s = slide("Questions?")
text(s, ["github.com/apriljwalter-lgtm/Group_8_Midterm_project"], 0.6, 3, 12, 2, 28)
prs.save("Slides.pptx")
