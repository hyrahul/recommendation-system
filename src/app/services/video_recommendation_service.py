from sqlalchemy.orm import Session
from app.db.models.video import Video
from app.db.models.video_student import VideoStudent


class VideoRecommendationService:
    @staticmethod
    def get_videos_for_lecture(
        db: Session,
        lecture_id: int,
        user_id: int,
    ) -> list[dict]:
        """
        Returns videos for a lecture with watch status,
        prioritizing unwatched videos.
        """

        videos = (
            db.query(Video)
            .filter(
                Video.lecture_id == lecture_id,
                Video.is_active.is_(True),
            )
            .all()
        )

        results = []

        for video in videos:
            progress = (
                db.query(VideoStudent)
                .filter(
                    VideoStudent.video_id == video.id,
                    VideoStudent.user_id == user_id,
                )
                .one_or_none()
            )

            status = (
                progress.watch_status
                if progress
                else "NotStarted"
            )

            results.append(
                {
                    "video_id": video.id,
                    "title": video.title,
                    "url": video.url,
                    "watch_status": status,
                }
            )

        # Sort: NotStarted → InProgress → Completed
        priority = {"NotStarted": 0, "InProgress": 1, "Completed": 2}
        results.sort(key=lambda v: priority.get(v["watch_status"], 3))

        return results
