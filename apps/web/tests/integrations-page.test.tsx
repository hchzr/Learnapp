import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import IntegrationsPage from "@/app/settings/integrations/page";

afterEach(() => {
  vi.restoreAllMocks();
});

describe("Integrations page", () => {
  it("renders integration cards with not connected statuses", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      ok: true,
      json: async () => ({
        providers: [
          { provider: "notion", connected: false },
          { provider: "todoist", connected: false },
          { provider: "google_drive", connected: false },
          { provider: "habitica", connected: false },
          { provider: "anki", connected: false }
        ]
      })
    } as Response);

    render(await IntegrationsPage());

    expect(screen.getByRole("heading", { name: "Integrations" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Notion" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Todoist" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Google Drive" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Habitica" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Anki" })).toBeInTheDocument();

    const statuses = screen.getAllByText("Status: Not Connected");
    expect(statuses).toHaveLength(5);

    const buttons = screen.getAllByRole("button", { name: "Connect" });
    expect(buttons).toHaveLength(5);
    buttons.forEach((button) => {
      expect(button).toBeDisabled();
    });
  });
});
