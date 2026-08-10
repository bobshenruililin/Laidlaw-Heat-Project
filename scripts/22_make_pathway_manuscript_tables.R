#!/usr/bin/env Rscript
# 22_make_pathway_manuscript_tables.R
# Build manuscript-oriented wide tables from pathway_panel_estimates.csv

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
outcome <- tolower(Sys.getenv("OUTCOME", unset = "stroke"))
mode <- tolower(Sys.getenv("PATHWAY_MODE", unset = "dev"))

est_path <- file.path(root, "outputs", "tables", paste0(outcome, "_pathway_panel_estimates.csv"))
if (!file.exists(est_path)) stop("Run pathway fit first: ", est_path)
est <- utils::read.csv(est_path, stringsAsFactors = FALSE)
if (identical(mode, "real") && any(grepl("SYNTHETIC", est$data_status, ignore.case = TRUE))) {
  stop("Real manuscript table refused SYNTHETIC rows for ", outcome)
}

est$rr_ci <- sprintf("%.3f (%.3f–%.3f)", est$rr, est$rr_low, est$rr_high)
est$synth <- grepl("SYNTHETIC", est$data_status)

# Prefer pollution_stage == none when present
est2 <- est[est$pollution_stage %in% c("none", "", NA) | is.na(est$pollution_stage) | est$pollution_stage == "none", ]

# Main panel table
tab <- est2[, c("pathway_id", "pathway_title", "term", "rr_ci", "p_value", "n_months", "data_status")]
names(tab) <- c("pathway_id", "title", "term", "RR_95CI", "p_value", "n_months", "data_status")

out <- file.path(root, "outputs", "tables", paste0(outcome, "_manuscript_pathway_panel_table.csv"))
write_csv_safe(tab, out)

# Amended core candidates; Gate 3 remains open.
core_ids <- c("P01A", "P02A", "P02B", "P04A", "P04B", "P04C")
tab_h <- tab[tab$pathway_id %in% core_ids, ]
write_csv_safe(tab_h, file.path(root, "outputs", "tables", paste0(outcome, "_manuscript_amended_core.csv")))

note <- file.path(root, "outputs", "reports", paste0(outcome, "_manuscript_tables_note.md"))
writeLines(
  c(
    paste0("# Manuscript tables from pathway panel — ", toupper(outcome)),
    "",
    paste0("- Written: ", out),
    paste0("- Amended core (not Gate 3-frozen): outputs/tables/", outcome, "_manuscript_amended_core.csv"),
    paste0("- Synthetic run: ", any(tab$data_status == "SYNTHETIC" | grepl("SYNTHETIC", tab$data_status))),
    "",
    "If SYNTHETIC, these tables are formatting checks only — not results."
  ),
  note
)
message("Manuscript tables written. Synthetic=", any(grepl("SYNTHETIC", tab$data_status)))
