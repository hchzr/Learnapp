import { isApiError, isHealthResponse, type ApiError, type HealthResponse } from "@life-learn/shared";

const DEFAULT_API_BASE_URL = "http://localhost:8000";

export class ApiClientError extends Error {
  readonly status: number;
  readonly endpoint: string;
  readonly payload?: ApiError;

  constructor(message: string, options: { status: number; endpoint: string; payload?: ApiError }) {
    super(message);
    this.name = "ApiClientError";
    this.status = options.status;
    this.endpoint = options.endpoint;
    this.payload = options.payload;
  }
}

export type TypedApiClientOptions = {
  baseUrl?: string;
  fetchImpl?: typeof fetch;
};

export function createTypedApiClient(options: TypedApiClientOptions = {}) {
  const baseUrl = options.baseUrl ?? process.env.NEXT_PUBLIC_API_BASE_URL ?? DEFAULT_API_BASE_URL;
  const fetchImpl = options.fetchImpl ?? fetch;

  async function parseApiError(response: Response): Promise<ApiError | undefined> {
    let payload: unknown;

    try {
      payload = await response.json();
    } catch {
      return undefined;
    }

    if (!isApiError(payload)) {
      return undefined;
    }

    return payload;
  }

  async function getHealth(): Promise<HealthResponse> {
    const endpoint = `${baseUrl}/v1/health`;
    const response = await fetchImpl(endpoint, {
      method: "GET",
      headers: { Accept: "application/json" },
      cache: "no-store"
    });

    if (!response.ok) {
      const payload = await parseApiError(response);
      const message = payload?.error.message ?? `Request failed with status ${response.status}`;
      throw new ApiClientError(message, {
        endpoint: "/v1/health",
        status: response.status,
        payload
      });
    }

    const body = await response.json();

    if (!isHealthResponse(body)) {
      throw new ApiClientError("Received invalid health response from API", {
        endpoint: "/v1/health",
        status: response.status
      });
    }

    return body;
  }

  return {
    getHealth
  };
}
