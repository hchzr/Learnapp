# AGENTS Instructions

These rules apply to the entire repository.

1. **No secrets in code**
   - Never commit API keys, passwords, tokens, or credentials.
   - Use environment variables and keep examples only in `.env.example`.
2. **Never log tokens or secrets**
   - Do not print auth tokens, session IDs, refresh tokens, or private keys in logs.
   - Redact sensitive values in all debug and error output.
3. **Every PR must include quality checks**
   - Run and report lint, typecheck, and tests for changed areas.
   - If a check cannot run in the environment, document why.
4. **Every PR must include commands run**
   - Include exact verification commands in the PR description.
5. **Every PR must update docs when behavior or architecture changes**
   - Update files under `docs/` (especially architecture and decisions) to reflect new or changed behavior.

When in doubt, prioritize security, testability, and clear documentation.
