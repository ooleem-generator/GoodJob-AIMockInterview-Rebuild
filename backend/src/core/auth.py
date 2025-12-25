from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWKClient
from functools import lru_cache
from typing import Dict, Optional
from config import settings

security = HTTPBearer()

CLERK_DOMAIN = settings.CLERK_FRONTEND_URL
JWKS_URL = f"{CLERK_DOMAIN}/.well-known/jwks.json"


@lru_cache(maxsize=1)
def get_jwks_client() -> PyJWKClient:
    # PyJWKClient 싱글톤 인스턴스
    # - 자동 키 로테이션 지원, 1시간 캐싱
    return PyJWKClient(
        JWKS_URL,
        cache_keys=True,
        max_cached_keys=16,
        cache_jwk_set=True,
        lifespan=3600,  # 1시간
    )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict:
    # Clerk JWT 검증 및 사용자 정보 반환
    token = credentials.credentials

    try:
        jwks_client = get_jwks_client()
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,  # Authorization 헤더에서 받은 JWT 문자열
            signing_key.key,  # JWT 서명을 검증하기 위한 공개키, Clerk가 개인키로 서명, JWKS에서 받은 공개키로 검증
            algorithms=["RS256"],  # 허용할 서명 알고리즘 목록, Clerk는 RS256 사용
            audience=CLERK_DOMAIN,  # 누구를 위해 발급되었는가, JWT의 aud 클레임과 대응
            issuer=CLERK_DOMAIN,  # 토큰 발급자, JWT의 iss 클레임과 대응
            options={
                "require": [
                    "exp",
                    "iat",
                    "sub",
                ],  # JWT payload에 반드시 존재해야 하는 클레임, 일반적으로 exp: 만료 시간, iat: 발급 시간, sub: 유저 고유 id
                "verify_exp": True,
                "verify_aud": True,
                "verify_iss": True,
            },
        )

        return {
            "id": payload["sub"],  # 이걸 DB에서 user_id(PK)로 매핑
            "email": payload.get("email"),
            "email_verified": payload.get("email_verified", False),
            "name": payload.get("name"),
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidAudienceError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token audience",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidIssuerError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token issuer",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        # 예상치 못한 오류 로깅 (프로덕션에서는 logger 사용)
        print(f"Authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal authentication error",
        )


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    ),
) -> Optional[Dict]:
    if credentials is None:
        return None

    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None
