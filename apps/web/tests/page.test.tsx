import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { Sidebar } from "@/components/sidebar";
import HomePage from "@/app/page";

describe("Home page", () => {
  it("renders app title and sidebar navigation", () => {
    render(
      <div>
        <Sidebar />
        <HomePage />
      </div>
    );

    expect(screen.getByText("Life & Learn")).toBeInTheDocument();
    expect(screen.getByTestId("sidebar-nav")).toBeInTheDocument();
    expect(screen.getByText("Calendar")).toBeInTheDocument();
  });
});
