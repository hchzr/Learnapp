import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { Sidebar } from "@/components/sidebar";
import HomePage from "@/app/page";
import { DEFAULT_FEATURE_FLAGS } from "@/lib/feature-flags";

describe("Home page", () => {
  it("renders app title and sidebar navigation", () => {
    render(
      <div>
        <Sidebar featureFlags={{ ...DEFAULT_FEATURE_FLAGS, anki: true, exercises: true, planner: true }} />
        <HomePage />
      </div>
    );

    expect(screen.getByText("Life & Learn")).toBeInTheDocument();
    expect(screen.getByTestId("sidebar-nav")).toBeInTheDocument();
    expect(screen.getByText("Calendar")).toBeInTheDocument();
  });

  it("hides flagged modules from navigation when disabled", () => {
    render(<Sidebar featureFlags={DEFAULT_FEATURE_FLAGS} />);

    expect(screen.queryByText("Anki")).not.toBeInTheDocument();
    expect(screen.queryByText("Exercises")).not.toBeInTheDocument();
    expect(screen.queryByText("Study Plan")).not.toBeInTheDocument();
  });
});
