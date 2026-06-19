from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_admin
from app.models.channel import Channel
from app.models.upload_queue import UploadQueue
from app.models.user import User, UserPlan
from app.models.video import Video
from app.schemas.common import UserOut, UserPlanUpdate, UserStatusUpdate
from app.services.worker_health import get_worker_health

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserOut])
def get_users(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    return db.query(User).order_by(User.created_at.desc()).all()


@router.get("/videos")
def get_videos(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    count = db.query(func.count(Video.id)).scalar()
    return {"total_videos": count}


@router.get("/channels")
def get_channels(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    count = db.query(func.count(Channel.id)).scalar()
    return {"total_channels": count}


@router.get("/system-status")
def system_status(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    queue_pending = db.query(func.count(UploadQueue.id)).scalar()
    return {
        "status": "ok",
        "queue_jobs": queue_pending,
        "analytics": {"uptime": "unknown", **get_worker_health()},
    }


@router.patch("/users/{user_id}/status", response_model=UserOut)
def toggle_user(
    user_id: int,
    payload: UserStatusUpdate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user.is_active = payload.is_active
    db.commit()
    db.refresh(user)
    return user


@router.patch("/users/{user_id}/plan", response_model=UserOut)
def change_plan(
    user_id: int,
    payload: UserPlanUpdate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user.plan = UserPlan(payload.plan)
    db.commit()
    db.refresh(user)
    return user
