from fastapi import APIRouter, HTTPException, status,Depends
from typing import Any, List, Union
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import datetime
from models import (Users,Achievements,User_achievement)
from schemas import (
    achievements as achievements_schema
)
from modules import (
    auth as auth_module
)
from pony.orm import db_session, commit

router = APIRouter(
    prefix="/achievements",
    responses={404: {"description": "Not found"}},
)

points = 10

@router.post("/create",status_code=status.HTTP_201_CREATED)
@db_session
def create_achievement(current_user: Annotated[str, Depends(auth_module.get_current_user_id)],achievement: achievements_schema.achievement_in):
    user = Users.get(ID=current_user)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    achievement = Achievements(image=achievement.image,points=points,created_at=datetime.datetime.today())
    achievement.flush()
    
    achievement_id = int(achievement.ID)
    
    user_achievement = User_achievement(user_ID=user,achievement_ID=achievement_id)

    user.points += points
    
    commit()
    
    return {
        "message": "Achievement created"
    }

@router.delete("/delete/{achievement_id}",status_code=status.HTTP_200_OK)
@db_session
def delete_achievement(current_user: Annotated[str, Depends(auth_module.get_current_user_id)],achievement_id: int):
    user = Users.get(ID=current_user)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    achievement = Achievements.get(ID=achievement_id)
    
    if not achievement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Achievement not found",
        )
    
    user_achievement = User_achievement.get(user_ID=user,achievement_ID=achievement)
    
    if not user_achievement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Achievement not found",
        )
    
    user.points -= achievement.points
    
    user_achievement.delete()
    achievement.delete()
    
    commit()
    
    return {
        "message": "Achievement deleted"
    }
    
@router.get("",status_code=status.HTTP_200_OK)
@db_session
def get_achievements(current_user: Annotated[str, Depends(auth_module.get_current_user_id)]):
    achievements_data = []
    user = Users.get(ID=current_user)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    user_achievement = User_achievement.select(lambda ua: ua.user_ID == user)
    
    for ua in user_achievement:
       
        achievements_data.append({
            "image": ua.achievement_ID.image,
            "points": ua.achievement_ID.points,
            "created_at": ua.achievement_ID.created_at,
            "ID": ua.achievement_ID.ID,
        })
        
        
    return achievements_data
    
    
