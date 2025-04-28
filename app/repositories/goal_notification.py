from sqlalchemy.orm import Session
from app.models import GoalNotification
from app.schemas.GoalNotification import GoalNotificationCreate, GoalNotificationUpdate
from fastapi import HTTPException

class GoalNotificationRepository:

    @staticmethod
    def create_goal_notification(session: Session, goal_notification_data: GoalNotificationCreate):
        try:
            goal_notification = GoalNotification(**goal_notification_data.dict())
            session.add(goal_notification)
            session.commit()
            session.refresh(goal_notification)
            return goal_notification
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=f"Error creating GoalNotification: {str(e)}")

    @staticmethod
    def get_goal_notification(session: Session, goal_id: int, notification_id: int):
        goal_notification = session.query(GoalNotification).filter(
            GoalNotification.goal_id == goal_id,
            GoalNotification.notification_id == notification_id
        ).first()
        if not goal_notification:
            raise HTTPException(status_code=404, detail="GoalNotification not found")
        return goal_notification

    @staticmethod
    def get_all_goal_notifications(session: Session):
        goal_notifications = session.query(GoalNotification).all()
        return goal_notifications

    @staticmethod
    def update_goal_notification(session: Session, goal_id: int, notification_id: int, goal_notification_data: GoalNotificationUpdate):
        goal_notification = GoalNotificationRepository.get_goal_notification(session, goal_id, notification_id)
        try:
            for key, value in goal_notification_data.dict(exclude_unset=True).items():
                setattr(goal_notification, key, value)
            session.commit()
            session.refresh(goal_notification)
            return goal_notification
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=f"Error updating GoalNotification: {str(e)}")

    @staticmethod
    def delete_goal_notification(session: Session, goal_id: int, notification_id: int):
        goal_notification = GoalNotificationRepository.get_goal_notification(session, goal_id, notification_id)
        try:
            session.delete(goal_notification)
            session.commit()
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=f"Error deleting GoalNotification: {str(e)}")
        return {"status": "OK"}
