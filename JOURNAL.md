# Module 3 Journal — PathReview Contribution

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/88

**Issue title:** `POST /reviews` endpoint has no test for when the profile has no ingested documents

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The `POST /reviews` endpoint (`api/routes/reviews.py`) creates a review record and kicks off ingestion plus agent processing in the background, but there's no test covering what happens when a profile exists yet has zero ingested documents attached to it. Right now it's an open question whether the endpoint returns a clean, expected error or crashes/hangs when downstream code (the agent orchestration or RAG retrieval) tries to work with empty content. A successful fix adds a unit test in `tests/unit/test_review_routes.py` (a new file — it doesn't exist yet) that creates a profile with no ingested documents, calls the endpoint, and asserts it returns an appropriate error response rather than an unhandled exception. This is scoped to the API layer's test coverage, not a behavior change, so it's a good entry point into how `api/routes/reviews.py` and `core/services/review_service.py` fit together.

**Scope/fit reasoning (issue checklist):** Picked this as a first issue because it's labeled both `tier-1` and `good first issue`, is unassigned with no linked PR yet (checked issue #88 directly — "No branches or pull requests"), and the maintainer's own estimate is 2–3 hours. It's isolated to one endpoint and one new test file, so it doesn't require understanding the RAG/agent internals in depth — just enough to know what "no ingested documents" should trigger. Several other tier-1 issues in the tracker (e.g. #149–#159) already have open PRs from other students, so I deliberately chose one that was still unclaimed.

**Branch name:** `test/88-post-reviews-no-documents-test`

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger

## Week 9 — Solution building & PR submission

### Check-in 1 (mid-week)

**Current progress:**
Implemented the fix from `PLAN.md`: added `profile_has_ingestable_content()` to
`core/services/review_service.py`, and wired a profile lookup + 404/400
validation into `create_review_endpoint` in `api/routes/reviews.py` (404 if
the profile doesn't exist/isn't owned by the caller, 400 if it has no
`github_username`/`portfolio_url`/`resume_text`). Wrote 9 unit tests in
`tests/unit/test_review_routes.py` covering the 400 case, the 404 case, two
happy-path regression cases (different content fields), and the
`profile_has_ingestable_content` helper directly — all passing locally.
Also cleaned up the type-annotation debt on the functions I touched so
`mypy` doesn't fail on missing annotations, and verified (via a clean-room
diff against the original files) that my change introduces zero new
`mypy`/`ruff` failures beyond what was already there — details in
`PLAN.md`'s "Pre-existing `make check` failures" section.

**Next steps:**
Run `make check` and `make test-unit` for real (Docker + the project's actual
Python 3.11 venv — my local iteration happened in a constrained sandbox
without Docker, so this is the authoritative check). Commit and push, open a
draft PR, request review in the cohort Slack channel, address feedback, then
mark ready for review and submit before the deadline.

**Blockers:**
None currently.

---

### Check-in 2 (end of week)

**PR link:** [pending — to be filled in once opened]

**Branch:** `test/88-post-reviews-no-documents-test`

**What you built:**
Added a `profile_has_ingestable_content()` check to `POST /reviews` so a
request for a profile with no GitHub username, portfolio URL, or resume text
gets a clear `400`, and a request for a nonexistent/not-owned profile gets a
`404` — instead of silently creating a review that later "completes" with
fabricated placeholder feedback (the bug documented in `PLAN.md`'s
reproduction section).

**Tests added or updated:**
New file `tests/unit/test_review_routes.py` (9 tests): the 400 case, the 404
case, two happy-path regression cases (different content fields populated),
and 5 direct tests of the `profile_has_ingestable_content` helper. Follows
the existing mock-based pattern from `tests/unit/test_review_service.py`.

**Self-review confirmation:** [x] make check passes  [x] make test-unit passes
(both in the "introduces no new failures beyond documented pre-existing
debt" sense described in the Week 9 instructions — see `PLAN.md`'s
"Pre-existing `make check` failures" section for the full verified numbers:
`ruff` 182/182 identical on `main` vs. this branch; `pytest tests/unit` 53
failed/384 passed here vs. 53 failed/375 passed on `main`, same 53 failures,
9 extra passing tests are this PR's; `mypy` scoped to the two files this PR
touches fixes several pre-existing errors and introduces none, verified via
clean-room diff)

**Draft PR feedback received from:** [pending]
