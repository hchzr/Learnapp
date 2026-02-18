import { describe, expect, it } from "vitest";
import type { ApiError, HealthResponse } from "../src";

describe("shared types", () => {
  it("supports health response shape", () => {
    const response: HealthResponse = { status: "ok" };
    expect(response.status).toBe("ok");
  });

  it("supports api error shape", () => {
    const error: ApiError = { error: { code: "UNAUTHORIZED", message: "Missing auth" } };
    expect(error.error.code).toBe("UNAUTHORIZED");
  });
});
