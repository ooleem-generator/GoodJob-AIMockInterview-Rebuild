/**
 * 개발 환경에서 브라우저 콘솔로 API 테스트하기 위한 유틸리티
 *
 * 사용법:
 * 1. 브라우저 콘솔을 열고
 * 2. window.testAuth() 실행
 */

import { api } from "@/apis/api";

export const devTestUtils = {
  /**
   * 인증 테스트 - 백엔드 /api/test/me 엔드포인트 호출
   */
  testAuth: async () => {
    console.log("🔐 인증 테스트 시작...");
    try {
      const response = await api.get("/test/me");
      console.log("✅ 인증 성공!", response.data);
      return response.data;
    } catch (error: any) {
      console.error("❌ 인증 실패:", error.response?.data || error.message);
      throw error;
    }
  },

  /**
   * 일반 API 테스트
   */
  testApi: async (endpoint: string) => {
    console.log(`🌐 API 테스트: ${endpoint}`);
    try {
      const response = await api.get(endpoint);
      console.log("✅ 응답:", response.data);
      return response.data;
    } catch (error: any) {
      console.error("❌ 에러:", error.response?.data || error.message);
      throw error;
    }
  },

  /**
   * Health check 테스트
   */
  testHealthCheck: async () => {
    console.log("💚 Health check...");
    try {
      const response = await api.get("/health");
      console.log("✅ 서버 상태:", response.data);
      return response.data;
    } catch (error: any) {
      console.error("❌ 서버 연결 실패:", error.response?.data || error.message);
      throw error;
    }
  },
};

// 개발 환경에서만 window 객체에 노출
if (typeof window !== "undefined" && process.env.NODE_ENV === "development") {
  (window as any).testAuth = devTestUtils.testAuth;
  (window as any).testApi = devTestUtils.testApi;
  (window as any).testHealthCheck = devTestUtils.testHealthCheck;

  console.log(`
🛠️ Dev Test Utils 사용 가능:
  - window.testAuth() : 인증 테스트
  - window.testApi(endpoint) : 커스텀 API 테스트
  - window.testHealthCheck() : Health check
  `);
}
