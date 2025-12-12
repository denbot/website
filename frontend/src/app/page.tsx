import Link from 'next/link';

export default function HomePage() {
  return (
    <div>
      This is the homepage...
      <Link href="/login">Log in here!</Link>
    </div>
  );
}
