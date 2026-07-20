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

**Cohort ledger:** [ ] Issue added to cohort ledger
