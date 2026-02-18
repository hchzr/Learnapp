export interface paths {
  "/v1/health": {
    get: {
      responses: {
        200: {
          content: {
            "application/json": HealthResponse;
          };
        };
      };
    };
  };
  "/v1/me": {
    get: {
      responses: {
        401: {
          content: {
            "application/json": ApiError;
          };
        };
      };
    };
  };
}

export type HealthResponse = {
  status: "ok";
};

export type ApiError = {
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
  requestId?: string;
};

export function isHealthResponse(payload: unknown): payload is HealthResponse {
  if (!payload || typeof payload !== "object") {
    return false;
  }

  return (payload as { status?: unknown }).status === "ok";
}

export function isApiError(payload: unknown): payload is ApiError {
  if (!payload || typeof payload !== "object") {
    return false;
  }

  const maybeError = (payload as { error?: unknown }).error;

  if (!maybeError || typeof maybeError !== "object") {
    return false;
  }

  const code = (maybeError as { code?: unknown }).code;
  const message = (maybeError as { message?: unknown }).message;

  return typeof code === "string" && typeof message === "string";
}

export type ApiPaths = paths;
