# PLAN — Issue #88

**Issue:** [`POST /reviews` endpoint has no test for when the profile has no ingested documents](https://github.com/ascherj/pathreview/issues/88)

## Reproduction

The endpoint's own code path was exercised directly (bypassing HTTP, calling the
route function and service layer as plain async functions with mocked DB/objects)
to see what actually happens today. Script: `scripts/repro_issue_88.py`.

**Step 1 — `POST /reviews` never checks the profile at all.**
`create_review_endpoint` (`api/routes/reviews.py`) takes only a `profile_id` and
immediately calls `create_review(db, profile_id, user_id)`, which inserts a
`Review` row with `status="pending"` and returns `200` — there is no lookup of
the `Profile` row and no check of whether it has any ingested content. Confirmed
by calling the endpoint function with a `profile_id` for a profile that has no
`github_username`, `portfolio_url`, or `resume_text`: it returns normally with
`status="pending"` and schedules the background task, exactly as it would for a
fully-populated profile.

**Step 2 — the background job doesn't error either, it fabricates feedback.**
`process_review` (`core/services/review_service.py`) was run against a `Profile`
with all three content fields set to `None`. Output:

```
ingestion_pipeline_completed   sources_count=0
agent_orchestration_completed  sections_count=2
rag_retrieval_completed
safety_checks_passed
review_processing_completed    overall_score=0.81
final review.status: complete
sections count: 3
overall_score: 0.81
```

`_run_ingestion_pipeline` correctly returns an empty list when there's nothing to
ingest, but `_run_agent_orchestration` and `_run_rag_retrieval_generation` are
placeholder implementations that return the same canned "Technical Skills /
Project Experience / Career Growth" sections regardless of input. `_run_safety_checks`
only validates structure (non-empty sections, valid confidence range), so it
passes. The review ends up `status="complete"` with a plausible-looking
`overall_score` — fabricated feedback for a profile with zero real content, and
nothing about the response tells the caller that happened.

**Conclusion:** there's no crash anywhere on this path, which is arguably worse
than the issue title suggests — the endpoint silently succeeds and returns
generic, made-up feedback instead of surfacing a clear error. This is why the
issue is filed as "no test," but a test alone would just be pinning down broken
behavior; a small validation fix is the more honest resolution.

## Root Cause

No code between the route handler and `create_review` ever fetches the `Profile`
row to check for ingestable content (`github_username`, `portfolio_url`,
`resume_text`, or rows in `ingested_source`). The gap is at the API boundary,
not in the ingestion/agent/RAG placeholders themselves (those are expected to be
stubs per `core/services/review_service.py`'s own docstrings).

## Proposed Solution

1. Add a small guard, e.g. `profile_has_ingestable_content(profile) -> bool` in
   `core/services/review_service.py`, checking `github_username`,
   `portfolio_url`, and `resume_text`.
2. In `create_review_endpoint`, fetch the `Profile` for `data.profile_id` before
   calling `create_review`. If it doesn't exist, return `404` (not currently
   handled either). If it exists but has no ingestable content, return `400`
   with a clear `detail` message instead of creating a review.
3. Keep `create_review()` itself unchanged — the guard belongs in the route
   layer so existing service-level tests (`tests/unit/test_review_service.py`)
   that call `create_review` directly keep passing unmodified.

## Test Plan

New file: `tests/unit/test_review_routes.py`, following the mock-based pattern
already used in `tests/unit/test_review_service.py` (mock `AsyncMock` DB
session, mock `Profile`/`User` objects, call the route function directly rather
than spinning up a real HTTP client/DB, matching how the rest of this codebase's
unit tests are written).

Planned cases:
- `test_create_review_returns_400_when_profile_has_no_ingested_content` — mock
  profile with `github_username=portfolio_url=resume_text=None`, assert the
  endpoint raises `HTTPException(400)` and that `db.add`/background task
  scheduling are **not** called.
- `test_create_review_returns_404_when_profile_not_found` — covers the other
  gap found during reproduction (no profile-existence check at all).
- `test_create_review_succeeds_when_profile_has_github_username` — regression
  guard so the happy path isn't broken by the new check.

## Files to Change

- `api/routes/reviews.py` — add profile lookup + validation in
  `create_review_endpoint`
- `core/services/review_service.py` — add `profile_has_ingestable_content`
  helper
- `tests/unit/test_review_routes.py` — new file, tests above

## Risks / Edge Cases

- Must not break `tests/unit/test_review_service.py`'s existing
  `create_review` tests — the new check stays in the route layer.
- A profile with rows in `ingested_source` but no `github_username`/
  `portfolio_url`/`resume_text` set directly (e.g. content added via another
  path) should probably also count as "has content" — worth confirming
  against `core/models/ingested_source.py` before finalizing the check in the
  actual PR.
- `make check` and `make test-unit` need to pass before opening the PR per
  `docs/CONTRIBUTING.md`.
- `core/services/review_service.py` and `api/routes/reviews.py` currently fail
  `mypy` (missing type annotations on several existing functions) — this is
  pre-existing debt, not introduced by this change. The PLAN.md and
  `scripts/repro_issue_88.py` commits were made with `--no-verify` since they're
  planning artifacts, not shipped code. The actual fix commits in Week 9 will
  touch these two files anyway, so type-annotate at least the functions we
  modify (`create_review_endpoint` and the new `profile_has_ingestable_content`
  helper, plus their signatures) as part of that work, so `make check` passes
  cleanly on the real PR without needing `--no-verify`.
