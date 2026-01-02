from fastapi import APIRouter, Request, HTTPException, status
from svix.webhooks import Webhook, WebhookVerificationError
from sqlmodel import Session, select
from src.config import settings
from src.database import engine
from src.models.user import User
import json

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


@router.post("/clerk")
async def clerk_webhook(request: Request):
    # Clerk와 Supabase의 유저 데이터를 연동하기 위한 웹훅 엔드포인트
    # 유저 생성, 수정, 삭제 시 이벤트 수신

    # 1. Clerk webhook secret 가져오기 (환경변수)
    webhook_secret = settings.CLERK_WEBHOOK_SECRET
    if not webhook_secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Clerk webhook secret not configured",
        )

    # 2. Svix 헤더 가져오기 (웹훅 검증용)
    svix_id = request.headers.get("svix-id")
    svix_timestamp = request.headers.get("svix-timestamp")
    svix_signature = request.headers.get("svix-signature")

    if not svix_id or not svix_timestamp or not svix_signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing svix headers"
        )

    # 3. Request body 가져오기
    body = await request.body()

    # 4. 웹훅 서명 검증 (Clerk가 정말 보낸 요청인지 확인)
    wh = Webhook(webhook_secret)
    try:
        payload = wh.verify(
            body,
            {
                "svix-id": svix_id,
                "svix-timestamp": svix_timestamp,
                "svix-signature": svix_signature,
            },
        )
    except WebhookVerificationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Webhook verification failed: {str(e)}",
        )

    # 5. 이벤트 타입과 데이터 추출
    event_type = payload.get("type")
    data = payload.get("data")

    if not event_type or not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid webhook payload"
        )

    # 6. 이벤트 타입별 처리
    with Session(engine) as session:
        if event_type == "user.created":
            # 새 사용자 생성
            user = User(
                id=data["id"],
                email=data["email_addresses"][0]["email_address"],
                name=f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()
                or None,
                email_verified=data["email_addresses"][0]["verification"]["status"]
                == "verified",
                image_url=data.get("image_url"),
            )
            session.add(user)
            session.commit()
            return {"status": "success", "message": "User created"}

        elif event_type == "user.updated":
            # 기존 사용자 업데이트
            statement = select(User).where(User.id == data["id"])
            user = session.exec(statement).first()

            if user:
                user.email = data["email_addresses"][0]["email_address"]  # ✅ 문자열
                user.name = (
                    f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()
                    or None
                )
                user.email_verified = (
                    data["email_addresses"][0]["verification"]["status"] == "verified"
                )
                user.image_url = data.get("image_url")  # ✅

                session.add(user)
                session.commit()
                return {"status": "success", "message": "User updated"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )

        elif event_type == "user.deleted":
            # 기존 사용자 업데이트
            statement = select(User).where(User.id == data["id"])
            user = session.exec(statement).first()

            if user:
                session.delete(user)
                session.commit()
                return {"status": "success", "message": "User deleted"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )

        else:
            # 처리하지 않는 이벤트 타입
            return {"status": "ignored", "message": f"Unhandled event: {event_type}"}
