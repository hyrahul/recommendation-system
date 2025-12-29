# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.models import (
    User,
    Category,
    Lecture,
    LecturePrerequisite,
    LectureStudent,
)

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    yield db

    db.close()


def seed_base_data(db):
    # Users
    lee = User(username="lee.dohyun", full_name="Lee Dohyun", affiliation="Korea")
    kim = User(username="kim.minseo", full_name="Kim Minseo", affiliation="Korea")
    usa = User(username="john.smith", full_name="John Smith", affiliation="USA")

    db.add_all([lee, kim, usa])
    db.flush()

    # Categories
    battery = Category(name="Battery Basics", visibility="Korea")
    advanced = Category(name="Advanced Battery Systems", visibility="Korea")
    overseas = Category(name="Global Standards for Overseas", visibility="OverseasCommon")

    db.add_all([battery, advanced, overseas])
    db.flush()

    # Lectures
    basic = Lecture(
        title="Introduction to Battery Basics",
        category_id=battery.id,
        difficulty="Basic",
        is_searchable=True,
    )

    intermediate = Lecture(
        title="Battery Materials and Chemistry",
        category_id=battery.id,
        difficulty="Intermediate",
        is_searchable=True,
    )

    advanced_lecture = Lecture(
        title="Advanced Battery Design",
        category_id=advanced.id,
        difficulty="Advanced",
        is_searchable=True,
    )

    overseas_lecture = Lecture(
        title="International Battery Standards",
        category_id=overseas.id,
        difficulty="Basic",
        is_searchable=True,
    )

    db.add_all([basic, intermediate, advanced_lecture, overseas_lecture])
    db.flush()

    # Prerequisites
    db.add(LecturePrerequisite(
        lecture_id=intermediate.id,
        prerequisite_lecture_id=basic.id
    ))

    db.add(LecturePrerequisite(
        lecture_id=advanced_lecture.id,
        prerequisite_lecture_id=intermediate.id
    ))

    # Progress
    db.add(LectureStudent(
        user_id=kim.id,
        lecture_id=basic.id,
        study_status="Completed"
    ))

    db.commit()

    return {
        "lee": lee,
        "kim": kim,
        "usa": usa,
        "basic": basic,
        "intermediate": intermediate,
        "advanced": advanced_lecture,
        "overseas": overseas_lecture,
    }
