from app.services.recommendation_service import recommend
from app.services.video_recommendation_service import VideoRecommendationService


def handle_recommendation(
    db,
    user_id: int,
    user_message: str,
):
    result = recommend(db, user_id)

    enriched_lectures = []

    for lecture in result.lectures:
        videos = VideoRecommendationService.get_videos_for_lecture(
            db=db,
            lecture_id=lecture.id,
            user_id=user_id,
        )

        enriched_lectures.append(
            {
                "lecture_id": lecture.id,
                "title": lecture.title,
                "difficulty": lecture.difficulty,
                "videos": videos,
            }
        )

    return {
        "type": "recommendation",
        "status": result.status,
        "lectures": enriched_lectures,
        "reason": result.reason,
    }
