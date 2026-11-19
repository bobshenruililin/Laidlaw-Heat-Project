"""Build the coauthor-review paper from the committed research-lab tables.

The Markdown is the editable source. Only the two delimited tables are generated.
See README.md for the plotting, Word and PDF commands.
"""

import argparse
import csv
import hashlib
from pathlib import Path
import posixpath
import re
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ARTICLE = HERE / "Manuscript.md"
NAMES = {
    "mean_temp": "Mean temperature", "mean_tmax": "Mean daily maximum",
    "mean_tmin": "Mean daily minimum", "hot_nights": "Hot nights",
    "cold_days": "Cold days", "very_hot_days": "Very hot days",
}
BRANCH = "research/recorded-burden-lab-2026-11"


def read_rows(results, name):
    with (results / f"{name}.csv").open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def md_table(headers, rows):
    return "\n".join("| " + " | ".join(map(str, row)) + " |" for row in
                     [headers, ["---"] * len(headers), *rows])


def with_tables(source, results):
    annual = read_rows(results, "service_context")
    designs = read_rows(results, "weather_design")
    if [int(r["year"]) for r in annual] != list(range(2013, 2024)):
        raise ValueError("Expected eleven consecutive annual rows")
    weather = {(r["exposure"], r["window"]): r for r in designs}
    periods = ["2013-2023", "2013-2019", "2020-2023"]
    if len(designs) != 18 or set(weather) != {(e, w) for e in NAMES for w in periods}:
        raise ValueError("Expected every combination of six exposures and three windows")
    count_cols = ["chd", "hf", "all_hospital_episodes", "circulatory_episodes", "ha_episodes"]
    counts = [[r["year"], *(f"{int(r[k]):,}" for k in count_cols)] for r in annual]
    weather_data = []
    for key, label in NAMES.items():
        residual_share = float(weather[key, periods[0]]["residual_share"])
        support = [weather[key, w]["months_for_half_ss"] for w in periods]
        weather_data.append([label, f"{100 * residual_share:.1f}%", *support])
    tables = {
        "annual": md_table(["Year", "CHD first stays", "HF first stays", "All episodes",
                            "Circulatory episodes", "HA episodes"], counts),
        "weather": md_table(["Exposure", "Variation remaining", "2013–23 (132)", "2013–19 (84)",
                             "2020–23 (48)"], weather_data),
    }
    for key, table in tables.items():
        start, end = f"<!-- {key}-table -->", f"<!-- /{key}-table -->"
        if source.count(start) != 1 or source.count(end) != 1:
            raise ValueError(f"Expected a single delimited {key} table")
        source = re.sub(re.escape(start) + ".*?" + re.escape(end),
                        lambda _: f"{start}\n\n{table}\n\n{end}", source, flags=re.DOTALL)
    return source


def check_claims(source, results, frozen_root):
    """Bind empirical sentences in the review paper to the complete result tables."""
    annual = {int(r["year"]): r for r in read_rows(results, "service_context")}
    records = read_rows(results, "hindcast")
    models = read_rows(results, "weather_models")
    designs = {(r["window"], r["exposure"]): r for r in read_rows(results, "weather_design")}
    thresholds = {r["series"]: float(r["break_even_person_time_vs_2019"])
                  for r in read_rows(results, "annual_changes")
                  if r["year"] == "2023" and r["series"] in ("chd", "hf")}
    evidence = {}

    def count(year, key):
        return int(annual[year][key])

    def change(start, end, key):
        return 100 * (count(end, key) / count(start, key) - 1)

    def check_direction(series, years, expected):
        for key in series:
            actual = tuple((count(y, key) > count(y-1, key)) - (count(y, key) < count(y-1, key))
                           for y in years)
            if actual != expected:
                raise ValueError(f"Annual directions differ for {key}: {actual}")

    check_direction(("chd", "hf"), range(2014, 2020), (-1,) * 6)
    check_direction(("all_hospital_episodes", "ha_episodes"), range(2014, 2020), (1,) * 6)
    check_direction(("chd", "hf", "all_hospital_episodes", "circulatory_episodes", "ha_episodes"),
                    range(2020, 2024), (-1, 1, -1, 1))
    for key in ("chd", "hf"):
        if [year for year in annual if count(year, key) == min(count(y, key) for y in annual)] != [2020]:
            raise ValueError(f"Unique 2020 minimum no longer holds for {key}")
    total_chd, total_hf = (sum(count(y, k) for y in annual) for k in ("chd", "hf"))
    evidence["event totals"] = f"{total_chd:,} CHD-associated stays and {total_hf:,} HF-associated stays"
    evidence["early contrast"] = (f"CHD and HF counts fell by {-change(2013,2019,'chd'):.1f}% and "
                                  f"{-change(2013,2019,'hf'):.1f}%, respectively, as total episodes rose "
                                  f"by {change(2013,2019,'all_hospital_episodes'):.1f}%")
    early = [100 * (count(2013, k)-count(2015, k)) / (count(2013, k)-count(2019, k)) for k in ("chd", "hf")]
    evidence["early concentration"] = f"{early[0]:.1f}% of the six-year decline in CHD counts and {early[1]:.1f}% in HF counts"
    evidence["early circulatory contrast"] = f"circulatory episodes rose by {change(2013,2019,'circulatory_episodes'):.1f}%"
    evidence["2020 episodes"] = (f"All-hospital episodes fell {-change(2019,2020,'all_hospital_episodes'):.1f}% "
                                f"and circulatory episodes fell {-change(2019,2020,'circulatory_episodes'):.1f}%")
    idx = {k: 100 + change(2019, 2023, k) for k in ("chd", "hf", "all_hospital_episodes", "circulatory_episodes", "ha_episodes")}
    evidence["2023 comparison"] = (f"{idx['chd']:.1f} for CHD first stays, {idx['hf']:.1f} for HF first stays, "
                                  f"{idx['all_hospital_episodes']:.1f} for all-hospital episodes and "
                                  f"{idx['circulatory_episodes']:.1f} for circulatory episodes")
    evidence["HA sensitivity"] = f"reached {idx['ha_episodes']:.1f} in 2023"
    evidence["conditional denominators"] = (f"{100*(1-thresholds['chd']):.2f}% for CHD or "
                                           f"{100*(1-thresholds['hf']):.2f}% for HF")
    lookup = {(r["outcome"], r["benchmark"], int(r["target_year"])):
              float(r["observed_minus_benchmark_pct"]) for r in records}
    rules = ["last_observation", "expanding_log_linear", "trailing_3_log_linear"]
    if set(lookup) != {(k, b, y) for k in ("chd","hf") for b in rules for y in range(2017, 2021)}:
        raise ValueError("Incomplete outcome, year or benchmark combinations")
    c = [-lookup["chd", rule, 2020] for rule in rules]
    h = [-lookup["hf", rule, 2020] for rule in rules]
    evidence["2020 CHD benchmarks"] = (f"{c[0]:.1f}% below the previous year's count, {c[1]:.1f}% below the "
                                       f"expanding-history trend and {c[2]:.1f}% below the recent three-year trend")
    evidence["2020 HF benchmarks"] = f"corresponding shortfalls were {h[0]:.1f}%, {h[1]:.1f}% and {h[2]:.1f}%"
    bounds = []
    for key in ("chd", "hf"):
        prior = [lookup[key, "expanding_log_linear", y] for y in (2017, 2018, 2019)]
        if min(prior) <= 0:
            raise ValueError("Every prior expanding-history benchmark must underpredict")
        bounds.append(f"{min(prior):.1f}–{max(prior):.1f}%")
    evidence["prior performance"] = f"underpredicted CHD by {bounds[0]} and HF by {bounds[1]}"
    metrics = ("hot_nights", "cold_days", "very_hot_days")
    percentages = [100 * float(designs["2013-2023", n]["residual_share"]) for n in metrics]
    evidence["residual variance shares"] = (f"{percentages[0]:.1f}%, {percentages[1]:.1f}% and "
                                            f"{percentages[2]:.1f}% of the corresponding unadjusted variation")
    # Exact integer anchors for the two prose spells of limited exposure variation.
    expected_counts = {"2013-2023": (7, 7, 8), "2020-2023": (3, 2, 3)}
    for window, expected in expected_counts.items():
        if tuple(int(designs[window, e]["months_for_half_ss"]) for e in metrics) != expected:
            raise ValueError(f"Weather concentration changed in {window}")
    evidence["full exposure concentration"] = "Seven, seven and eight of the 132 months"
    evidence["later exposure concentration"] = "those counts were three, two and three"
    nw = [r for r in models if r["se_method"] == "NeweyWest_lag6"]
    if len(nw) != 12 or {(r["outcome"], r["exposure"]) for r in nw} != {(k, e) for k in ("chd", "hf") for e in NAMES}:
        raise ValueError("The full two-outcome weather family is required")
    evidence["multiplicity"] = f"adjusted q-value among the twelve released full-series weather models was {min(float(r['q_value']) for r in nw):.3f}"
    cold = next(r for r in nw if r["outcome"] == "hf" and r["exposure"] == "cold_days")
    evidence["weather model"] = (f"{float(cold['rr']):.3f} (nominal 95% CI "
                                 f"{float(cold['rr_low']):.3f}–{float(cold['rr_high']):.3f})")
    sensitivity_file = frozen_root / "outputs/tables/cvd_trend_depletion_sensitivity.csv"
    if hashlib.sha256(sensitivity_file.read_bytes()).hexdigest() != "061158111bbc79478b8cb54f27687447c213fd1bfc13efe9cf3309996f348e5e":
        raise ValueError("Calendar sensitivity table differs from the October source")
    with sensitivity_file.open(newline="", encoding="utf-8") as stream:
        matches = [r for r in csv.DictReader(stream) if
                   (r["outcome"], r["exposure"], r["scenario"], r["n_months"]) ==
                   ("hf", "cold_days", "trend_ns8", "132")]
    if len(matches) != 1:
        raise ValueError("Expected exactly one eight-df full-window HF cold-day estimate")
    value = matches[0]
    evidence["calendar sensitivity"] = (f"eight-degree-of-freedom time spline was {float(value['rr']):.3f} "
                                        f"({float(value['rr_low']):.3f}–{float(value['rr_high']):.3f})")
    for label, phrase in evidence.items():
        if phrase not in source:
            raise ValueError(f"Article disagrees with {label}. Expected: {phrase}")
    hko = next((p for p in source.split("\n\n") if p.startswith("Meteorological data was obtained")), "")
    if hashlib.sha256(hko.encode()).hexdigest() != "0d93cc5cf8b8de733ddf75500541da98d6050ce2554bd81f2fcf77c4c663cf63":
        raise ValueError("The coauthor's source weather paragraph differs from the October revision")
    print(f"Verified {len(evidence)} source-to-text comparisons, annual directions, complete tables and weather wording")


def plot_figures(results, rasters):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import colors

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 9, "axes.labelsize": 9,
        "axes.titlesize": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": "#879397", "axes.linewidth": 0.7, "xtick.color": "#34444b",
        "ytick.color": "#34444b", "axes.labelcolor": "#17272e", "text.color": "#17272e",
        "svg.fonttype": "none", "svg.hashsalt": "laidlaw-november-2026",
    })
    rasters.mkdir(parents=True, exist_ok=True)

    def save(figure, name, title):
        figure.savefig(HERE / f"{name}.svg", metadata={"Date": None, "Title": title})
        figure.savefig(rasters / f"{name}.png", dpi=230, facecolor="white")
        plt.close(figure)

    series = [
        ("chd_index", "CHD first stays", "#116c65", "o", "solid"),
        ("hf_index", "HF first stays", "#275785", "s", (0, (3, 1.4))),
        ("all_hospital_episodes_index", "All hospital episodes", "#783e1c", "D", "solid"),
        ("circulatory_episodes_index", "Circulatory episodes", "#9c5d12", "^", (0, (2, 1.3))),
    ]
    annual = read_rows(results, "service_context")
    figure, axes = plt.subplots(1, 2, figsize=(7.5, 3.22), gridspec_kw={"width_ratios": [1.24, 1]})
    figure.subplots_adjust(left=.088, right=.986, top=.73, bottom=.17, wspace=.28)
    panels = [
        (2013, 2019, "A   Before 2020", (74, 202), [80, 100, 125, 150, 175, 200]),
        (2019, 2023, "B   2019 to 2023", (79, 105), [80, 85, 90, 95, 100, 105]),
    ]
    for axis, (start, end, title, limits, ticks) in zip(axes, panels):
        rows = [r for r in annual if start <= int(r["year"]) <= end]
        years = [int(row["year"]) for row in rows]
        axis.grid(axis="y", color="#dee5e4", linewidth=.7)
        axis.axhline(100, color="#8b989a", linewidth=.9, zorder=1)
        axis.set_axisbelow(True)
        for key, label, colour, marker, line in series:
            axis.plot(years, [float(row[key]) for row in rows], label=label, color=colour,
                      linewidth=1.6, marker=marker, markersize=4.5, linestyle=line,
                      markeredgewidth=.85, markerfacecolor="white", zorder=3)
        axis.set(title=title, ylim=limits, yticks=ticks, xticks=years, xlim=(start - .18, end + .18))
        axis.set_title(title, loc="left", fontweight="bold", pad=8)
        axis.set_title("", loc="center")
        axis.tick_params(length=3, pad=3, labelsize=8)
    axes[0].set_ylabel("Index (2019 = 100)")
    handles, labels = axes[0].get_legend_handles_labels()
    figure.legend(handles, labels, loc="upper center", bbox_to_anchor=(.50, 1.01),
                  ncol=4, frameon=False, fontsize=8.4, handlelength=1.7,
                  handletextpad=.42, columnspacing=1.28)
    save(figure, "figure1_activity", "Annual first stays and hospital episodes, 2013–2023")

    comparisons = read_rows(results, "hindcast")
    values = {(r["outcome"], r["benchmark"], int(r["target_year"])):
              float(r["observed_minus_benchmark_pct"]) for r in comparisons}
    rules = ["last_observation", "expanding_log_linear", "trailing_3_log_linear"]
    years = list(range(2017, 2021))
    if len(comparisons) != 24 or set(values) != {(o, b, y) for o in ("chd", "hf") for b in rules for y in years}:
        raise ValueError("All 24 outcome, benchmark and target combinations are required")
    figure, axes = plt.subplots(1, 2, figsize=(7.5, 2.43))
    figure.subplots_adjust(left=.22, right=.996, top=.75, bottom=.14, wspace=.13)
    cmap = colors.LinearSegmentedColormap.from_list("deviation", ["#b77a51", "#fbfaf5", "#6baea5"])
    norm = colors.Normalize(vmin=-20, vmax=20)
    for index, (axis, outcome) in enumerate(zip(axes, ("chd", "hf"))):
        matrix = [[values[outcome, b, y] for y in years] for b in rules]
        axis.imshow(matrix, cmap=cmap, norm=norm, aspect="auto", interpolation="nearest")
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                label = f"{value:+.1f}".replace("-", "−")
                axis.text(j, i, label, ha="center", va="center", color="#0e2128", fontsize=9.4)
        for x in (.5, 1.5, 2.5):
            axis.axvline(x, color="white", linewidth=3 if x == 2.5 else 1)
        for y in (.5, 1.5):
            axis.axhline(y, color="white", linewidth=1)
        axis.axvline(2.5, color="#4c5659", linewidth=1.1)
        axis.set_xticks(range(4), years, fontsize=8)
        axis.set_yticks(range(3), ["Previous year", "Trend since 2013", "Latest 3-year trend"] if index == 0 else [""] * 3,
                        fontsize=9)
        axis.tick_params(length=0, pad=4)
        axis.set_title(f"{outcome.upper()} first stays", loc="left", fontweight="bold", pad=8)
        for spine in axis.spines.values():
            spine.set_visible(False)
    save(figure, "figure2_benchmarks", "Signed percentage difference between observed and projected annual counts")


def word(rasters):
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Inches, Pt, RGBColor

    source = ARTICLE.read_text()
    for file in ("figure1_activity", "figure2_benchmarks"):
        png = (rasters / (file + ".png")).resolve()
        if not png.is_file():
            raise ValueError("Render raster and SVG figures with the figures command first")
        source = source.replace(f"({file}.svg)", f"(<{png}>){{width=6.45in}}")
    # Absolute URLs keep the tables accessible from downloaded copies.
    def external_link(match):
        path = posixpath.normpath(posixpath.join("manuscript/covid_period/november", match.group(1)))
        kind = "tree" if match.group(1).endswith("/") else "blob"
        return f"](https://github.com/bobshenruililin/Laidlaw-Heat-Project/{kind}/{BRANCH}/{path})"

    source = re.sub(r"\]\((\.\./[^)]+)\)", external_link, source)
    # Set page breaks on the next heading instead of adding a blank paragraph.
    break_before = []
    for following in source.split("<!-- newpage -->")[1:]:
        break_before.append(following.strip().splitlines()[0].lstrip("# "))
    source = source.replace("<!-- newpage -->", "")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "paper.md").write_text(source)
        subprocess.run(["pandoc", "-f", "markdown-implicit_figures", str(tmp / "paper.md"),
                        "-o", str(tmp / "body.docx")], check=True)
        doc = Document(tmp / "body.docx")
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.left_margin, sec.right_margin = Inches(.91), Inches(.91)
    sec.top_margin, sec.bottom_margin = Inches(.79), Inches(.70)
    sec.header_distance, sec.footer_distance = Inches(.34), Inches(.31)
    for name in ("Normal", "Body Text", "First Paragraph", "Compact"):
        style = doc.styles[name]
        style.font.name, style.font.size = "Georgia", Pt(11)
        style.font.color.rgb = RGBColor.from_string("11191C")
        fmt = style.paragraph_format
        fmt.space_before, fmt.space_after, fmt.line_spacing = Pt(0), Pt(6), 1.15
        fmt.widow_control = True
    for name, size, before, after in [("Title", 24, 6, 7), ("Heading 2", 18, 8, 6), ("Heading 3", 12.7, 9, 4)]:
        style = doc.styles[name]
        style.font.name, style.font.size = "Georgia", Pt(size)
        style.font.bold, style.font.color.rgb = True, RGBColor.from_string("101619")
        fmt = style.paragraph_format
        fmt.space_before, fmt.space_after, fmt.line_spacing = Pt(before), Pt(after), 1.06
        fmt.keep_with_next = True
        props = style.element.get_or_add_pPr()
        border = props.find(qn("w:pBdr"))
        if border is not None:
            props.remove(border)
    doc.paragraphs[0].style = "Title"
    doc.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
    # Word stores a raster fallback and an SVG part for every plot. Modern Word
    # and LibreOffice can render the vectors at the reader's chosen zoom.
    from docx.opc.constants import RELATIONSHIP_TYPE
    from docx.opc.packuri import PackURI
    from docx.opc.part import Part
    from lxml import etree
    for shape, stem in zip(doc.inline_shapes, ("figure1_activity", "figure2_benchmarks")):
        ratio = shape.height / shape.width
        shape.width, shape.height = Inches(6.42), Inches(6.42 * ratio)
        svg_part = Part(PackURI(f"/word/media/{stem}.svg"), "image/svg+xml",
                        (HERE / f"{stem}.svg").read_bytes(), doc.part.package)
        rid = doc.part.relate_to(svg_part, RELATIONSHIP_TYPE.IMAGE)
        blip = shape._inline.xpath(".//a:blip")[0]
        extensions = blip.find(qn("a:extLst"))
        if extensions is None:
            extensions = OxmlElement("a:extLst")
            blip.append(extensions)
        ext = OxmlElement("a:ext")
        ext.set("uri", "{96DAC541-7B7A-43D3-8B79-37D633B846F1}")
        ns = "http://schemas.microsoft.com/office/drawing/2016/SVG/main"
        vector = etree.SubElement(ext, f"{{{ns}}}svgBlip", nsmap={"asvg": ns})
        vector.set(qn("r:embed"), rid)
        extensions.append(ext)
    references = False
    for p in doc.paragraphs:
        if p.text == "References":
            references = True
        elif p.text == "Numerical appendix":
            references = False
        elif references:
            p.paragraph_format.keep_together = True
            p.paragraph_format.space_after = Pt(3.5)
            p.paragraph_format.line_spacing = 1.06
            for run in p.runs:
                run.font.size = Pt(9.3)
        if p.text in break_before:
            p.paragraph_format.page_break_before = True
        if p.text.startswith("Coauthor-review manuscript"):
            for r in p.runs:
                r.font.name, r.font.size = "Arial", Pt(9)
                r.font.color.rgb = RGBColor.from_string("45565C")
        if p.text.startswith(("Figure 1.", "Figure 2.", "Table 1.", "Table 2.")):
            p.paragraph_format.line_spacing = 1.09
            p.paragraph_format.space_after = Pt(7)
            for r in p.runs:
                r.font.name, r.font.size = "Arial", Pt(9)
        if p._p.xpath(".//w:drawing"):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.space_after = Pt(0)
    for table in doc.tables:
        table.autofit = False
        widths = ([.50, .96, .89, 1.32, 1.44, 1.32] if len(table.columns) == 6 else [1.68, 1.17, 1.19, 1.19, 1.19])
        for col, width in zip(table.columns, widths):
            col.width = Inches(width)
        for row_index, row in enumerate(table.rows):
            if row_index == 0:
                row._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))
            for column_index, cell in enumerate(row.cells):
                cell.width = Inches(widths[column_index])
                if row_index == 0 or row_index % 2 == 0:
                    shade = OxmlElement("w:shd")
                    shade.set(qn("w:fill"), "DCE6E5" if row_index == 0 else "F2F5F4")
                    cell._tc.get_or_add_tcPr().append(shade)
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT if column_index == 0 else WD_ALIGN_PARAGRAPH.RIGHT
                    p.paragraph_format.space_before, p.paragraph_format.space_after = Pt(2), Pt(2)
                    p.paragraph_format.line_spacing = 1.02
                    for r in p.runs:
                        r.font.name, r.font.size, r.bold = "Arial", Pt(8.8), row_index == 0
    header = sec.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    header.add_run("Hong Kong first hospitalisations  /  2013–2023")
    footer = sec.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    footer.add_run("Coauthor review   ·   19 November 2026       |       ")
    page = OxmlElement("w:fldSimple")
    page.set(qn("w:instr"), "PAGE")
    footer._p.append(page)
    for p in (header, footer):
        for run in p.runs:
            run.font.name, run.font.size = "Arial", Pt(8)
            run.font.color.rgb = RGBColor.from_string("525F64")
    doc.core_properties.title = doc.paragraphs[0].text
    doc.core_properties.subject = "Ecological analysis of released annual hospitalisation counts"
    doc.core_properties.author = "Laidlaw Heat Project"
    # A new file prevents a reader from seeing a half-written zip on regeneration.
    with tempfile.TemporaryDirectory(dir=HERE) as staging:
        output = Path(staging) / "Manuscript.docx"
        doc.save(output)
        output.replace(HERE / "Manuscript.docx")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["tables", "check", "figures", "word", "pdf"])
    parser.add_argument("--results", type=Path, default=ROOT / "research_lab/results")
    parser.add_argument("--frozen-root", type=Path, default=ROOT,
                        help="Repository root containing the frozen model sensitivity table")
    parser.add_argument("--rasters", type=Path, default=Path(tempfile.gettempdir()) / "laidlaw-paper-figures")
    args = parser.parse_args()
    if args.action in ("tables", "check"):
        source = ARTICLE.read_text()
        canonical = with_tables(source, args.results)
        if args.action == "tables":
            ARTICLE.write_text(canonical)
        elif source != canonical:
            raise SystemExit("Article tables differ from the research outputs")
        if args.action == "check":
            check_claims(canonical, args.results, args.frozen_root)
    elif args.action == "figures":
        plot_figures(args.results, args.rasters)
    elif args.action == "word":
        word(args.rasters)
    else:
        with tempfile.TemporaryDirectory() as tmp:
            temp = Path(tmp)
            profile = (temp / "profile").resolve().as_uri()
            subprocess.run(["soffice", f"-env:UserInstallation={profile}", "--headless",
                            "--convert-to", "pdf", "--outdir", str(temp), str(HERE / "Manuscript.docx")],
                           check=True)
            rendered = temp / "Manuscript.pdf"
            if not rendered.is_file():
                raise SystemExit("LibreOffice did not export the PDF")
            (HERE / "Manuscript.pdf").write_bytes(rendered.read_bytes())


if __name__ == "__main__":
    main()
