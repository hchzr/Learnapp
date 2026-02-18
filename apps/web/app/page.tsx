import { formatServiceName } from '@learnapp/shared';

export default function HomePage() {
  return (
    <main>
      <h1>{formatServiceName('web')}</h1>
      <p>Welcome to the Learnapp monorepo.</p>
    </main>
  );
}
