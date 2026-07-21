#!/usr/bin/env Rscript
# 22_make_pathway_manuscript_tables.R
# Build manuscript-oriented wide tables from pathway_panel_estimates.csv

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)

est_path <- file.path(root, "outputs", "tables", "pathway_panel_estimates.csv")
if (!file.exists(est_path)) stop("Run pathway fit first: ", est_path)
est <- utils::read.csv(est_path, stringsAsFactors = FALSE)

est$rr_ci <- sprintf("%.3f (%.3f–%.3f)", est$rr, est$rr_low, est$rr_high)
est$synth <- grepl("SYNTHETIC", est$data_status)

# Prefer pollution_stage == none when present
est2 <- est[est$pollution_stage %in% c("none", "", NA) | is.na(est$pollution_stage) | est$pollution_stage == "none", ]

# Main panel table
tab <- est2[, c("pathway_id", "pathway_title", "term", "rr_ci", "p_value", "n_months", "data_status")]
names(tab) <- c("pathway_id", "title", "term", "RR_95CI", "p_value", "n_months", "data_status")

out <- file.path(root, "outputs", "tables", "manuscript_pathway_panel_table.csv")
write_csv_safe(tab, out)

# Headline subset
headline <- intersect(c("P02", "P04"), unique(tab$pathway_id))
tab_h <- tab[tab$pathway_id %in% headline, ]
write_csv_safe(tab_h, file.path(root, "outputs", "tables", "manuscript_headline_P02_P04.csv"))

note <- file.path(root, "outputs", "reports", "manuscript_tables_note.md")
writeLines(
  c(
    "# Manuscript tables from pathway panel",
    "",
    paste0("- Written: ", out),
    paste0("- Headline subset: outputs/tables/manuscript_headline_P02_P04.csv"),
    paste0("- Synthetic run: ", any(tab$data_status == "SYNTHETIC" | grepl("SYNTHETIC", tab$data_status))),
    "",
    "If SYNTHETIC, these tables are formatting checks only — not results."
  ),
  note
)
message("Manuscript tables written. Synthetic=", any(grepl("SYNTHETIC", tab$data_status)))
