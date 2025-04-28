from fastapi import Depends, HTTPException, APIRouter
from typing import List
from app.connection import get_session
from app.schemas.GoalNotification import GoalNotificationCreate, GoalNotificationRead, GoalNotificationUpdate
from app.repositories.goal_notification import GoalNotificationRepository

router = APIRouter()

@router.post("/goal_notification", response_model=GoalNotificationRead)
def create_goal_notification(goal_notification_data: GoalNotificationCreate, session=Depends(get_session)):
    return GoalNotificationRepository.create_goal_notification(session, goal_notification_data)

@router.get("/goal_notification_list", response_model=List[GoalNotificationRead])
def get_goal_notifications(session=Depends(get_session)):
    return GoalNotificationRepository.get_all_goal_notifications(session)

@router.get("/goal_notification/{goal_notification_id}", response_model=GoalNotificationRead)
def get_goal_notification_by_id(goal_notification_id: int, session=Depends(get_session)):
    return GoalNotificationRepository.get_goal_notification_by_id(session, goal_notification_id)

@router.put("/goal_notification/{goal_notification_id}", response_model=GoalNotificationRead)
def update_goal_notification(goal_notification_id: int, goal_notification_data: GoalNotificationUpdate, session=Depends(get_session)):
    return GoalNotificationRepository.update_goal_notification(session, goal_notification_id, goal_notification_data)

@router.delete("/goal_notification/delete/{goal_notification_id}")
def delete_goal_notification(goal_notification_id: int, session=Depends(get_session)):
    GoalNotificationRepository.delete_goal_notification(session, goal_notification_id)
    return {"status": "OK"}
