#!/usr/bin/env Rscript
# run_pipeline.R — default entry point (dev mode)
#
# For explicit tracks:
#   Rscript scripts/run_pipeline_dev.R
#   Rscript scripts/run_pipeline_real.R

root <- normalizePath(".", winslash = "/", mustWork = TRUE)
setwd(root)
source(file.path("scripts", "run_pipeline_dev.R"))
