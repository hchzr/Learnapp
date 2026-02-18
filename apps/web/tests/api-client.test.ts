import { describe, expect, it } from "vitest";
import { ApiClientError, createTypedApiClient } from "@/lib/api-client";

describe("typed api client", () => {
  it("returns a typed health payload for successful responses", async () => {
    const client = createTypedApiClient({
      baseUrl: "http://api.local",
      fetchImpl: async () =>
        new Response(JSON.stringify({ status: "ok" }), {
          status: 200,
          headers: { "content-type": "application/json" }
        })
    });

    const response = await client.getHealth();
    expect(response.status).toBe("ok");
  });

  it("throws ApiClientError with parsed api error payload", async () => {
    const client = createTypedApiClient({
      baseUrl: "http://api.local",
      fetchImpl: async () =>
        new Response(
          JSON.stringify({
            error: {
              code: "UNAUTHORIZED",
              message: "Authentication stub: endpoint not yet implemented."
            },
            requestId: "req-22"
          }),
          {
            status: 401,
            headers: { "content-type": "application/json" }
          }
        )
    });

    await expect(client.getHealth()).rejects.toMatchObject<ApiClientError>({
      status: 401,
      payload: {
        error: {
          code: "UNAUTHORIZED",
          message: "Authentication stub: endpoint not yet implemented."
        },
        requestId: "req-22"
      }
    });
  });

  it("throws ApiClientError when response payload does not match contract", async () => {
    const client = createTypedApiClient({
      baseUrl: "http://api.local",
      fetchImpl: async () =>
        new Response(JSON.stringify({ status: "unexpected" }), {
          status: 200,
          headers: { "content-type": "application/json" }
        })
    });

    await expect(client.getHealth()).rejects.toMatchObject<ApiClientError>({
      message: "Received invalid health response from API",
      status: 200
    });
  });
});
