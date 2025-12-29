# tests/test_recommendation_service.py

from app.services.recommendation_service import recommend
from app.services.dto import RecommendationResult
from tests.conftest import seed_base_data


def test_beginner_gets_basic(db_session):
    data = seed_base_data(db_session)

    result = recommend(db_session, user_id=data["lee"].id)

    assert result.status == "OK"
    assert len(result.lectures) == 1
    assert result.lectures[0].title == "Introduction to Battery Basics"


def test_prerequisite_required(db_session):
    data = seed_base_data(db_session)

    # Lee has completed nothing
    result = recommend(db_session, user_id=data["lee"].id)

    assert result.status == "OK"
    assert result.lectures[0].difficulty == "Basic"


def test_intermediate_after_basic(db_session):
    data = seed_base_data(db_session)

    result = recommend(db_session, user_id=data["kim"].id)

    assert result.status == "OK"
    assert result.lectures[0].difficulty in ["Intermediate", "Basic"]


def test_blocked_user(db_session):
    data = seed_base_data(db_session)

    # Change USA user to China with no categories
    data["usa"].affiliation = "China"
    db_session.commit()

    result = recommend(db_session, user_id=data["usa"].id)

    assert result.status == "BLOCKED"


def test_overseas_category_visible(db_session):
    data = seed_base_data(db_session)

    result = recommend(db_session, user_id=data["usa"].id)

    titles = [l.title for l in result.lectures]
    assert "International Battery Standards" in titles
