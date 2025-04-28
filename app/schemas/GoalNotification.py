from pydantic import BaseModel
class GoalNotificationCreate(BaseModel):
    goal_id: int
    notification_id: int

    class Config:
        orm_mode = True

class GoalNotificationRead(BaseModel):
    goal_id: int
    notification_id: int

    class Config:
        orm_mode = True
class GoalNotificationUpdate(BaseModel):
    goal_id: int
    notification_id: int

    class Config:
        orm_mode = True
