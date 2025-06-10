export default function Home() {
  const name = "Your Name" // Replace with your actual name

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center">
        <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">{name}</h1>
        <p className="mt-6 text-lg text-gray-600">Welcome to my personal webpage</p>
      </div>
    </main>
  )
}
