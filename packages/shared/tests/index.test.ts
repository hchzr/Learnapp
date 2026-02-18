import { describe, expect, it } from 'vitest';
import { formatServiceName } from '../src/index';

describe('formatServiceName', () => {
  it('formats known service labels', () => {
    expect(formatServiceName('api')).toBe('Learnapp Api');
  });
});
