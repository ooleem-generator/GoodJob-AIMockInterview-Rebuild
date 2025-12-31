"use client";

import { useEffect } from "react";

/**
 * 개발 환경에서만 dev-test 유틸리티를 로드하는 컴포넌트
 */
export function DevTestLoader() {
  useEffect(() => {
    if (process.env.NODE_ENV === "development") {
      import("@/utils/dev-test");
      import("@/utils/debug-auth");
    }
  }, []);

  return null;
}
