import { useState } from 'react'
import { Header } from '@/components/layout/header'
import { Footer } from '@/components/layout/footer'
import { GuestHome } from '@/components/home/guesthome'
import { UserHome } from '@/components/home/userhome'
import { MediaPage } from '@/components/media/mediapage'

export function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [selectedMediaId, setSelectedMediaId] = useState<number | null>(null)

  return (
    <div className="flex min-h-screen flex-col overflow-hidden bg-[#FAF6F0] text-[#3B2A1E]">
      <Header
        isAuthenticated={isAuthenticated}
        username="JanKowalski"
        onLoginClick={() => setIsAuthenticated(true)}
        onLogoutClick={() => setIsAuthenticated(false)}
        onHomeClick={() => setSelectedMediaId(null)} // powrót na stronę główną po kliknięciu logo
      />

      <main className="flex-1 overflow-y-auto pt-6">
        <div className="mx-auto w-[92%] lg:w-[75%] pb-6">
          {selectedMediaId !== null ? (
            <MediaPage
              mediaId={selectedMediaId}
              onBack={() => setSelectedMediaId(null)}
              onSelectMedia={(id) => setSelectedMediaId(id)}
            />
          ) : isAuthenticated ? (
            <UserHome onSelectMedia={(id) => setSelectedMediaId(id)} />
          ) : (
            <GuestHome
              onLoginClick={() => setIsAuthenticated(true)}
              onSelectMedia={(id) => setSelectedMediaId(id)}
            />
          )}
        </div>
      </main>

      <Footer />
    </div>
  )
}