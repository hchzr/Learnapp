import { describe, expect, it } from 'vitest';
import { runWorkerTick } from '../src/index';

describe('worker runtime', () => {
  it('returns a deterministic tick message', () => {
    expect(runWorkerTick()).toContain('Learnapp Workers');
  });
});
