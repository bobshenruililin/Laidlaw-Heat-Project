# Playbook 07 — Pull-request board

## Trigger

Run when Bob (or an agent under `/playbook-07-pr-board`) wants the open-PR stack classified, superseded science PRs closed with a written reason, and unique work left alone. This is **hygiene**, not a merge.

Do **not** run this playbook as a licence to merge, to freeze Gate 3, or to discard unique files.

## Preconditions

- [`knowledge/CONTEXT_BOOTSTRAP.md`](../../knowledge/CONTEXT_BOOTSTRAP.md) has been read.
- Policy file [`analysis_plan/pr_board_policy.yml`](../pr_board_policy.yml) has been read.
- `gh` is authenticated **read-only** for listing. Closing a PR is allowed only for rows whose policy action is `CLOSE_SUPERSEDED` **and** whose unique files versus the living science tip are empty.
- The living science tip is `living_science_ref` in the policy (currently **`origin/main`**, PR **#82** merged). Do not open a parallel science PR.

## Steps

1. Run `python3 scripts/69_pr_board.py` from the repository root. It writes `reports/pr_board_YYYY-MM-DD.md` and `reports/pr_board_latest.md`.
2. Inspect the **unique-vs-living-tip** column. If a `CLOSE_SUPERSEDED` row has unique files, **do not close** it. Port or keep.
3. For each remaining `CLOSE_SUPERSEDED` row with zero unique files: post a comment naming the successor PR, then close (do not merge).
4. Leave `KEEP_*` rows open. Unique form-2a packs, Playbook 06, Fukuda, blogs, airfare, and the identification crucible stay open until a human merges or ports them.
5. Do not `gh pr merge`. Do not force-push. Do not close Gate 3.

## Close rule (machine-checkable)

Close only if **all** hold:

1. Policy action is `CLOSE_SUPERSEDED`.
2. `gh` reports the PR still open.
3. `git ls-tree` of that head vs the living science tip (`living_science_ref`) has **zero unique paths**.
4. The comment names the successor (`superseded_by`) and the board file.

## Done when

- A dated board exists under `reports/`.
- Superseded zero-unique science PRs are closed **or** the board explains why they were not.
- Unique PRs remain open with a recommended action.
- Gate 3 is still OPEN in `analysis_plan/decision_gates.md`.
- No new science PR was opened.

## Failure modes

- Closing PR 68 (Playbook 06) because the number is inconvenient. It conflicts with `main` and is still unique.
- Closing PR 80 (Fukuda), 62 (airfare), 46 (blogs), 53 (crucible), 61 (Guo TV climate) without a human port.
- Merging the living science PR without Bob asking.
- Treating a closed PR as deleted science: GitHub keeps the branch until someone deletes it.

## Which files to update

- `reports/pr_board_YYYY-MM-DD.md`
- `reports/pr_board_latest.md`
- `analysis_plan/pr_board_policy.yml` when a new standing classification is decided
- `analysis_plan/context_compound_log.md`
- `knowledge/CONTEXT_BOOTSTRAP.md` / `knowledge/INDEX.md` when the living science PR number changes

## Claim boundaries

This playbook organises GitHub objects. It does not change Table 2, fit Model 2/3, or freeze Gate 3.
