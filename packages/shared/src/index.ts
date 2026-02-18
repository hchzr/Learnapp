export function formatServiceName(service: string): string {
  const normalized = service.trim();
  const capitalized = normalized.charAt(0).toUpperCase() + normalized.slice(1);
  return `Learnapp ${capitalized}`;
}
