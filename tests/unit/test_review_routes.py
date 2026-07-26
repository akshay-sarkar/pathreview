"""Tests for api/routes/reviews.py.

Starter skeleton for issue #88. See PLAN.md at the repo root for the
reproduction notes and the reasoning behind these cases. Follows the
mock-based pattern already used in tests/unit/test_review_service.py --
no live DB/HTTP client needed, the route function is called directly.

TODO (Week 9 build phase):
- Implement the profile-content guard in api/routes/reviews.py /
  core/services/review_service.py described in PLAN.md.
- Fill in the assertions below once the guard exists.
"""

import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, Mock

from api.routes.reviews import create_review_endpoint
from api.schemas.review import ReviewCreate


@pytest.mark.unit
class TestCreateReviewEndpointContentValidation:
    """Test suite for POST /reviews validating profile content before processing."""

    @pytest.fixture
    def mock_db_session(self):
        session = AsyncMock()
        session.add = Mock()
        session.commit = AsyncMock()
        session.refresh = AsyncMock()
        session.execute = AsyncMock()
        return session

    @pytest.fixture
    def mock_background_tasks(self):
        bg = Mock()
        bg.add_task = Mock()
        return bg

    @pytest.fixture
    def mock_current_user(self):
        user = Mock()
        user.id = uuid4()
        return user

    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Guard not implemented yet -- see PLAN.md, tracked for Week 9")
    async def test_create_review_returns_400_when_profile_has_no_ingested_content(
        self, mock_db_session, mock_background_tasks, mock_current_user
    ):
        """A profile with no github_username/portfolio_url/resume_text should
        get a 400 instead of a silently-created review that will later
        fabricate placeholder feedback (see PLAN.md reproduction notes)."""
        data = ReviewCreate(profile_id=uuid4())

        # TODO: mock Profile lookup returning a profile with all content
        # fields set to None, once create_review_endpoint fetches the
        # profile. Currently it doesn't, which is exactly the bug.
        raise NotImplementedError

    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Guard not implemented yet -- see PLAN.md, tracked for Week 9")
    async def test_create_review_returns_404_when_profile_not_found(
        self, mock_db_session, mock_background_tasks, mock_current_user
    ):
        """Also uncovered today: there's no existence check on profile_id at all."""
        raise NotImplementedError

    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Guard not implemented yet -- see PLAN.md, tracked for Week 9")
    async def test_create_review_succeeds_when_profile_has_github_username(
        self, mock_db_session, mock_background_tasks, mock_current_user
    ):
        """Regression guard: the happy path must keep working once the
        content check is added."""
        raise NotImplementedError
