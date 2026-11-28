import { useState } from 'react'
import {
  Star,
  Bookmark,
  FolderHeart,
  Sparkles,
  ChevronRight,
  Eye,
  EyeOff,
} from 'lucide-react'
import { Button } from '@/components/ui/button'

interface ActivityItem {
  id: number
  title: string
  category: string
  startDate: string
  lastActivity: string
  progress: number
  rating: number
  tags: string[]
  coverColor: string
  coverImage: string
}

interface LibraryList {
  id: string
  name: string
  count: number
  isCustom?: boolean
}

const RECENT_ACTIVITIES: ActivityItem[] = [
  {
    id: 1,
    title: 'Minecraft',
    category: 'Gra',
    startDate: '12.09.2026',
    lastActivity: 'Dzisiaj',
    progress: 80,
    rating: 5,
    tags: ['#sandbox', '#relaks', '#co-op', '#klasyk'],
    coverColor: 'from-emerald-900 to-stone-900',
    coverImage: 'https://cdn2.steamgriddb.com/grid/a73027901f88055aaa0fd1a9e25d36c7.png',
  },
  {
    id: 2,
    title: 'Madagaskar 2',
    category: 'Film',
    startDate: '18.11.2026',
    lastActivity: 'Wczoraj',
    progress: 100,
    rating: 4,
    tags: ['#animacja', '#komedia', '#nostalgia'],
    coverColor: 'from-amber-700 to-orange-950',
    coverImage: 'https://a.ltrbxd.com/resized/film-poster/4/6/1/4/5/46145-madagascar-escape-2-africa-0-1000-0-1500-crop.jpg?v=92f4a1b4a1',
  },
  {
    id: 3,
    title: 'Ballady i romanse',
    category: 'Książka',
    startDate: '02.11.2026',
    lastActivity: '3 dni temu',
    progress: 60,
    rating: 5,
    tags: ['#poezja', '#romantyzm', '#lektura'],
    coverColor: 'from-stone-700 to-amber-950',
    coverImage: 'https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1684074121i/154991868.jpg',
  },
  {
    id: 4,
    title: 'Thriller — Michael Jackson',
    category: 'Muzyka',
    startDate: '10.10.2026',
    lastActivity: 'Tydzień temu',
    progress: 60,
    rating: 5,
    tags: ['#pop', '#lata80', '#winyl'],
    coverColor: 'from-amber-900 to-neutral-950',
    coverImage: 'https://thumb.wikimedia.org/wikipedia/en/thumb/5/55/Michael_Jackson_-_Thriller.png/250px-Michael_Jackson_-_Thriller.png?utm_source=en.wikipedia.org&utm_campaign=parser&utm_content=thumbnail',
  },
]

const LIBRARY_LISTS: LibraryList[] = [
  { id: 'current', name: 'Aktualne', count: 4 },
  { id: 'next', name: 'Następne', count: 12 },
  { id: 'recommended', name: 'Polecane przez znajomych', count: 7, isCustom: true },
  { id: 'wishlist', name: 'Lista życzeń', count: 19 },
  { id: 'finished', name: 'Skończone', count: 84 },
  { id: 'favorites', name: 'Ulubione', count: 15, isCustom: true },
  { id: 'era-2023', name: '2023 era', count: 9, isCustom: true },
  { id: 'dropped', name: 'porzucone :(', count: 3, isCustom: true },
]

const RECOMMENDATIONS = [
  { id: 101, title: "Fire Emblem: Fortune's Weave", category: 'Gra', coverColor: 'from-amber-800 to-red-950', coverImage: 'https://cdn2.steamgriddb.com/grid/5b5e26b3ca72e2f8ea8bf8bdea28d048.jpg', },
  { id: 102, title: '007: First Light', category: 'Film', coverColor: 'from-stone-700 to-neutral-950', coverImage: 'https://shared.steamstatic.com/store_item_assets/steam/apps/3768760/1159a696d257cbeb3f4479be3466cfba2ae938a0/library_600x900_2x.jpg?t=1763663780', },
  { id: 103, title: 'Hollow Knight', category: 'Gra', coverColor: 'from-stone-800 to-neutral-950', coverImage: 'https://cdn2.steamgriddb.com/grid/d18c832e8c956b4ef8b92862e6bf470d.png', },
  { id: 104, title: 'Clair Obscur: Expedition 33', category: 'Gra', coverColor: 'from-amber-700 to-stone-900', coverImage: 'https://cdn2.steamgriddb.com/grid/51c271be14d470319cef0b8932a9edce.png', },
  { id: 105, title: 'Gears of War: E-Day', category: 'Gra', coverColor: 'from-red-950 to-stone-950', coverImage: 'https://cdn2.steamgriddb.com/grid/8edd89f0215f3c4ce93865895d2ff136.png', },
  { id: 106, title: 'Minecraft', category: 'Gra', coverColor: 'from-emerald-900 to-stone-900', coverImage: 'https://cdn2.steamgriddb.com/grid/a73027901f88055aaa0fd1a9e25d36c7.png', },
]

interface UserHomeProps {
  onSelectMedia?: (id: number) => void
}

export function UserHome({ onSelectMedia }: UserHomeProps) {
  // Przełącznik dla Twojej uwagi ze szkicu (pasek postępu vs sam wariant z gwiazdkami i tagami)
  const [showProgressBar, setShowProgressBar] = useState(true)

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
      {/* LEWA KOLUMNA: OSTATNIA AKTYWNOŚĆ + REKOMENDACJE */}
      <div className="flex flex-col gap-6 lg:col-span-8">
        {/* OSTATNIA AKTYWNOŚĆ */}
        <section className="rounded-xl border border-[#D5C5B2] bg-[#F3ECE1] p-5 shadow-xs">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
            <h1 className="text-xl font-bold text-[#3B2A1E]">
              Ostatnia aktywność
            </h1>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowProgressBar((prev) => !prev)}
              className="h-7 gap-1.5 text-xs text-[#6E543E] hover:bg-[#E8DEC8] hover:text-[#3B2A1E]"
            >
              {showProgressBar ? (
                <>
                  <EyeOff className="h-3.5 w-3.5" />
                  Ukryj pasek postępu
                </>
              ) : (
                <>
                  <Eye className="h-3.5 w-3.5" />
                  Pokaż pasek postępu
                </>
              )}
            </Button>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            {RECENT_ACTIVITIES.map((item) => (
              <article
                key={item.id}
                onClick={() => onSelectMedia?.(item.id)}
                className="group flex cursor-pointer gap-3.5 rounded-lg border border-[#D5C5B2] bg-[#FAF6F0] p-3 transition-all hover:border-[#8C5A3C] hover:shadow-xs"
              >

                {/* Miniatura okładki po lewej */}
                <div
                  className={`relative flex aspect-2/3 w-22 shrink-0 flex-col justify-between overflow-hidden rounded-md border border-[#CBB9A3] bg-gradient-to-b ${item.coverColor} p-1.5 text-[#FAF6F0]`}
                >
                <img src={item.coverImage} alt={item.title} loading="lazy" className="absolute inset-0 h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"></img>
                  <span className="w-fit rounded bg-[#FAF6F0]/20 px-1 py-0.5 text-[9px] font-semibold backdrop-blur-xs">
                    {item.category}
                  </span>
                  <span className="line-clamp-2 text-[10px] leading-tight font-bold">
                    {item.title}
                  </span>
                </div>

                {/* Szczegóły po prawej */}
                <div className="flex min-w-0 flex-1 flex-col justify-between">
                  <div>
                    <h2 className="truncate text-base font-bold text-[#3B2A1E] group-hover:text-[#6B4423]">
                      {item.title}
                    </h2>
                    <div className="mt-1 space-y-0.5 text-[11px] leading-tight text-[#7D6149]">
                      <p>Data rozpoczęcia: {item.startDate}</p>
                      <p>Ostatnia aktywność: {item.lastActivity}</p>
                    </div>
                  </div>

                  {/* Opcjonalny pasek postępu ze szkicu */}
                  {showProgressBar && (
                    <div className="my-2">
                      <div className="h-3.5 w-full overflow-hidden rounded-full border border-[#CBB9A3] bg-[#E8DEC8]">
                        <div
                          className="flex h-full items-center bg-[#6B4423] px-2 text-[9px] font-bold text-[#FAF6F0] transition-all"
                          style={{ width: `${item.progress}%` }}
                        >
                          {item.progress}%
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Gwiazdki + Tagi */}
                  <div className="mt-1 space-y-1.5">
                    <div className="flex items-center gap-0.5">
                      {Array.from({ length: 5 }).map((_, i) => (
                        <Star
                          key={i}
                          className={`h-3.5 w-3.5 ${
                            i < item.rating
                              ? 'fill-[#8C5A3C] text-[#8C5A3C]'
                              : 'text-[#D5C5B2]'
                          }`}
                        />
                      ))}
                    </div>

                    <div className="flex flex-wrap gap-1">
                      {item.tags.map((tag) => (
                        <span
                          key={tag}
                          className="rounded border border-[#D5C5B2] bg-[#F3ECE1] px-1.5 py-0.5 text-[10px] font-medium text-[#5C4534]"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </section>

        {/* MOŻE CI SIĘ SPODOBAĆ (REKOMENDACJE) */}
        <section className="rounded-xl border border-[#D5C5B2] bg-[#F3ECE1] p-5 shadow-xs">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-bold text-[#3B2A1E]">
              Może ci się spodobać (rekomendacje)
            </h2>
            <span className="text-xs font-medium text-[#7D6149]">
              Na podstawie Twojej biblioteki
            </span>
          </div>

          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-6">
            {RECOMMENDATIONS.map((item) => (
              <article
                key={item.id}
                onClick={() => onSelectMedia?.(item.id)}
                className="group relative flex aspect-2/3 cursor-pointer flex-col justify-between overflow-hidden rounded-lg border border-[#CBB9A3] p-2 text-[#FAF6F0] shadow-xs transition-transform hover:-translate-y-1"
              >
                <img src={item.coverImage} alt={item.title} loading="lazy" className="absolute inset-0 h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"></img>
                <div
                  className={`absolute inset-0 bg-gradient-to-b ${item.coverColor} opacity-65`}
                />
                <span className="relative z-10 w-fit rounded bg-[#FAF6F0]/20 px-1.5 py-0.5 text-[10px] font-semibold backdrop-blur-xs">
                  {item.category}
                </span>
                <h3 className="relative z-10 line-clamp-2 text-xs leading-tight font-semibold text-[#FAF6F0]">
                  {item.title}
                </h3>
              </article>
            ))}
          </div>
        </section>
      </div>

      {/* PRAWA KOLUMNA: BIBLIOTEKA */}
      <aside className="relative flex flex-col justify-between rounded-xl border border-[#D5C5B2] bg-[#F3ECE1] p-5 shadow-xs lg:col-span-4">
        <div>
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-xl font-bold text-[#3B2A1E]">Biblioteka</h2>
            <span className="rounded-full bg-[#E4D7C5] px-2.5 py-0.5 text-xs font-semibold text-[#6B4423]">
              {LIBRARY_LISTS.length} list
            </span>
          </div>

          <div className="max-h-[460px] space-y-2 overflow-y-auto pr-1">
            {LIBRARY_LISTS.map((list) => (
              <button
                key={list.id}
                type="button"
                className="group flex w-full cursor-pointer items-center justify-between rounded-lg border border-[#D5C5B2] bg-[#FAF6F0] px-3.5 py-2.5 text-left transition-colors hover:border-[#8C5A3C] hover:bg-[#EFE6D8]"
              >
                <div className="flex items-center gap-2.5">
                  {list.isCustom ? (
                    <FolderHeart className="h-4 w-4 shrink-0 text-[#8C5A3C]" />
                  ) : (
                    <Bookmark className="h-4 w-4 shrink-0 text-[#6B4423]" />
                  )}
                  <span className="text-sm font-medium text-[#3B2A1E]">
                    {list.name}
                  </span>
                  {list.isCustom && (
                    <span className="rounded bg-[#E8DEC8] px-1.5 py-0.5 text-[10px] font-medium text-[#6E543E]">
                      własna
                    </span>
                  )}
                </div>

                <div className="flex items-center gap-1.5 text-xs text-[#7D6149]">
                  <span>{list.count}</span>
                  <ChevronRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Subtelny ozdobnik maskotki w prawym dolnym rogu ze szkicu */}
        <div className="mt-5 flex items-center justify-between rounded-lg border border-dashed border-[#CBB9A3] bg-[#FAF6F0]/70 px-3 py-2 text-xs text-[#6E543E]">
          <span className="flex items-center gap-1.5">
            <Sparkles className="h-3.5 w-3.5 text-[#8C5A3C]" />
            Maskotka Nerdiary pilnuje Twoich półek
          </span>
          <span className="text-lg transition-transform duration-300 hover:scale-125 hover:rotate-12 select-none">
            🦔
          </span>
        </div>
      </aside>
    </div>
  )
}