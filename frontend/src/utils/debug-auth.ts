/**
 * 인증 디버깅 유틸리티
 */

import { api } from "@/apis/api";

export const debugAuth = {
  /**
   * 토큰 확인 - Clerk에서 발급한 토큰 내용 디코딩
   */
  checkToken: async (getToken: () => Promise<string | null>) => {
    const token = await getToken();

    if (!token) {
      console.error("❌ 토큰이 없습니다. 로그인이 되어있는지 확인하세요.");
      return null;
    }

    console.log("🔑 토큰 발급됨:", token.substring(0, 50) + "...");

    // JWT 디코딩 (검증 없이 payload만 확인)
    try {
      const parts = token.split(".");
      if (parts.length !== 3) {
        console.error("❌ 유효하지 않은 JWT 형식");
        return null;
      }

      const payload = JSON.parse(atob(parts[1]));
      console.log("📋 토큰 Payload:", payload);
      console.log("📋 Issuer (iss):", payload.iss);
      console.log("📋 Audience (aud):", payload.aud);
      console.log("📋 Subject (sub):", payload.sub);
      console.log("📋 Expires (exp):", new Date(payload.exp * 1000).toLocaleString());

      return payload;
    } catch (error) {
      console.error("❌ 토큰 디코딩 실패:", error);
      return null;
    }
  },

  /**
   * 네트워크 요청 헤더 확인
   */
  checkRequestHeaders: async () => {
    console.log("🌐 실제 요청 보내기 (헤더 확인용)...");

    try {
      // 인터셉터를 통해 실제 요청 전송
      const response = await api.get("/test/me");
      console.log("✅ 요청 성공:", response.data);
    } catch (error: any) {
      console.error("❌ 요청 실패");
      console.error("상태 코드:", error.response?.status);
      console.error("에러 메시지:", error.response?.data);

      // 요청 설정 확인
      if (error.config) {
        console.log("📤 요청 헤더:", error.config.headers);
      }
    }
  },

  /**
   * 백엔드 설정 확인
   */
  checkBackendConfig: () => {
    console.log("⚙️ 백엔드 설정:");
    console.log("API_BASE_URL:", (window as any).API_BASE_URL || "확인 불가");
    console.log("현재 Origin:", window.location.origin);
  },
};

// 개발 환경에서만 window 객체에 노출
if (typeof window !== "undefined" && process.env.NODE_ENV === "development") {
  (window as any).debugAuth = debugAuth;

  console.log(`
🔍 Auth Debug Utils 사용 가능:
  - window.debugAuth.checkToken(getToken) : 토큰 내용 확인
  - window.debugAuth.checkRequestHeaders() : 요청 헤더 확인
  - window.debugAuth.checkBackendConfig() : 백엔드 설정 확인
  `);
}
