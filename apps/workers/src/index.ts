import { formatServiceName } from '@learnapp/shared';

export function runWorkerTick(): string {
  return `${formatServiceName('workers')} tick executed`;
}
