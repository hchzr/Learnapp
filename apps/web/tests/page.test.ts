import { describe, expect, it } from 'vitest';
import { formatServiceName } from '@learnapp/shared';

describe('web shared usage', () => {
  it('formats service name', () => {
    expect(formatServiceName('web')).toBe('Learnapp Web');
  });
});
