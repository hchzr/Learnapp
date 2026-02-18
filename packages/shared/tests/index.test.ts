import { describe, expect, it } from "vitest";
import { isApiError, isHealthResponse, type ApiPaths } from "../src";

describe("shared api contract", () => {
  it("validates the health response shape", () => {
    expect(isHealthResponse({ status: "ok" })).toBe(true);
    expect(isHealthResponse({ status: "bad" })).toBe(false);
  });

  it("validates api error payloads", () => {
    expect(
      isApiError({
        error: {
          code: "UNAUTHORIZED",
          message: "Missing auth"
        }
      })
    ).toBe(true);

    expect(isApiError({ error: { code: 401 } })).toBe(false);
  });

  it("defines canonical endpoint contracts", () => {
    const healthPath: keyof ApiPaths = "/v1/health";
    const mePath: keyof ApiPaths = "/v1/me";

    expect(healthPath).toBe("/v1/health");
    expect(mePath).toBe("/v1/me");
  });
});
