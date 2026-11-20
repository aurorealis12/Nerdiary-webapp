import { useState } from 'react'
import {
  Film,
  Star,
  Plus,
  Send,
  MessageSquarePlus,
  ThumbsUp,
  MessageSquare,
  UserPlus,
  Check,
  Award,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface MetadataRow {
  label: string
  value: string
  isLink?: boolean
}

interface ReviewItem {
  id: number
  author: string
  badge?: string
  rating: number
  category: 'Popularne' | 'Nowe'
  content: string
  likes: number
  commentsCount: number
  timeAgo: string
}

const METADATA: MetadataRow[] = [
  { label: 'reżyseria', value: 'Phil Lord, Christopher Miller', isLink: true },
  { label: 'scenariusz', value: 'Drew Goddard', isLink: true },
  { label: 'produkcja', value: 'USA', isLink: true },
  { label: 'nagrody', value: 'Film otrzymał 2 nagrody oraz 5 nominacji' },
]

const REVIEWS: ReviewItem[] = [
  {
    id: 1,
    author: 'Maja Lis',
    rating: 8,
    category: 'Popularne',
    content: 'stary: "nie chce kamienia" stary i kamień po tygodniu:',
    likes: 915,
    commentsCount: 6,
    timeAgo: '8 mies.',
  },
  {
    id: 2,
    author: 'Marta Pyka',
    rating: 8,
    category: 'Nowe',
    content: 'daj kamienia',
    likes: 8,
    commentsCount: 1,
    timeAgo: '16 godz.',
  },
  {
    id: 3,
    author: 'Jan Tracz',
    badge: 'krytyk niezależny',
    rating: 7,
    category: 'Popularne',
    content:
      'Zadowalająca i nawet ujmująca ekranizacja badziewnej powieści. Normalnie byłaby szóstka, ale szacun za to, że udało im się wznieść tę historię na jeszcze wyższy poziom. Casting ekstraklasowy — Goslinga nie da się nie lubić!',
    likes: 187,
    commentsCount: 121,
    timeAgo: '8 mies.',
  },
]

const SIMILAR_WORKS = [
  { id: 1, title: 'Yakuza 6: The Song of Life', category: 'Gra', coverColor: 'from-amber-800 to-red-950', coverImage: 'https://shared.steamstatic.com/store_item_assets/steam/apps/1388590/library_600x900_2x.jpg?t=1718191689' },
  { id: 2, title: '007: First Light', category: 'Film', coverColor: 'from-stone-700 to-neutral-950', coverImage: 'https://shared.steamstatic.com/store_item_assets/steam/apps/3768760/1159a696d257cbeb3f4479be3466cfba2ae938a0/library_600x900_2x.jpg?t=1763663780' },
  { id: 3, title: 'Blade Runner: 2049', category: 'Film', coverColor: 'from-stone-800 to-neutral-950', coverImage: 'https://fwcdn.pl/fpo/07/98/630798/7801880_1.10.webp' },
  { id: 4, title: 'Clair Obscur: Expedition 33', category: 'Gra', coverColor: 'from-amber-700 to-stone-900', coverImage: 'https://cdn2.steamgriddb.com/grid/51c271be14d470319cef0b8932a9edce.png', },
  { id: 5, title: 'Gears of War: E-Day', category: 'Gra', coverColor: 'from-red-950 to-stone-950', coverImage: 'https://cdn2.steamgriddb.com/grid/8edd89f0215f3c4ce93865895d2ff136.png', },
  { id: 6, title: 'Project Hail Mary', category: 'Książka', coverColor: 'from-emerald-900 to-stone-900', coverImage: 'https://s.lubimyczytac.pl/upload/books/5230000/5230343/1380924-352x500.jpg', },
  { id: 7, title: 'Interstellar', category: 'Film', coverColor: 'from-stone-800 to-amber-950', coverImage: 'https://fwcdn.pl/fpo/56/29/375629/7670122_2.10.webp', },
  { id: 8, title: 'Marsjanin', category: 'Książka', coverColor: 'from-orange-900 to-stone-900', coverImage: 'https://s.lubimyczytac.pl/upload/books/235000/235716/324070-352x500.jpg', },
]

export function MediaPage() {
  const [userRating, setUserRating] = useState(5)
  const [hoveredRating, setHoveredRating] = useState<number | null>(null)
  const [addedToList, setAddedToList] = useState(false)
  const [followedAuthors, setFollowedAuthors] = useState<number[]>([])
  const [likedReviews, setLikedReviews] = useState<number[]>([])

  const toggleFollow = (id: number) => {
    setFollowedAuthors((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id],
    )
  }

  const toggleLike = (id: number) => {
    setLikedReviews((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id],
    )
  }

  return (
    <div className="flex flex-col gap-6">
      {/* GÓRNA SEKCJA: OKŁADKA + DANE DZIEŁA + PANEL AKCJI */}
      <section className="rounded-xl border border-[#D5C5B2] bg-[#F3ECE1] p-6 shadow-xs">
        <div className="grid grid-cols-1 gap-6 md:grid-cols-12">
          {/* LEWA: PLAKAT / OKŁADKA */}
          <div className="md:col-span-4 lg:col-span-3">
            <div className="relative flex aspect-2/3 w-full flex-col justify-between overflow-hidden rounded-xl border border-[#CBB9A3] bg-gradient-to-b from-stone-800 via-amber-950 to-neutral-950 p-4 text-[#FAF6F0] shadow-sm">
            <img src="https://a.ltrbxd.com/resized/film-poster/6/1/1/2/8/8/611288-project-hail-mary-0-1000-0-1500-crop.jpg?v=ac31b6ec03" alt="Project Hail Mary" loading="lazy" className="absolute inset-0 h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"></img>
              <span className="w-fit rounded bg-[#FAF6F0]/15 px-2 py-0.5 text-xs font-semibold backdrop-blur-xs">
                SCI-FI / PRZYGODOWY
              </span>
              <div>
                <p className="text-xs tracking-widest text-amber-300/90 uppercase">
                  Ryan Gosling
                </p>
                <h2 className="mt-1 text-2xl leading-tight font-black tracking-tight">
                  PROJEKT HAIL MARY
                </h2>
                <p className="mt-2 text-xs text-[#E2D6C5]">W kinach od 20 marca</p>
              </div>
            </div>
          </div>

          {/* ŚRODEK: TYTUŁ, ROK, AUTOR, METADANE */}
          <div className="flex flex-col justify-between md:col-span-5 lg:col-span-6">
            <div>
              <div className="flex flex-wrap items-center gap-3">
                <h1 className="text-3xl font-extrabold tracking-tight text-[#3B2A1E]">
                  Projekt Hail Mary
                </h1>
                <span className="inline-flex items-center gap-1 rounded-lg border border-[#CBB9A3] bg-[#FAF6F0] px-2.5 py-1 text-xs font-semibold text-[#6B4423]">
                  <Film className="h-4 w-4" />
                  Film
                </span>
              </div>

              <div className="mt-2 space-y-0.5 text-base font-medium text-[#5C4534]">
                <p>2026</p>
                <p className="text-sm text-[#7D6149]">
                  Na podstawie powieści: <span className="font-semibold text-[#3B2A1E]">Andy Weir</span>
                </p>
              </div>

              {/* Tabela szczegółów (reżyseria, scenariusz, produkcja, nagrody) */}
              <dl className="mt-6 space-y-2.5 border-t border-[#E2D6C5] pt-4 text-sm">
                {METADATA.map((row) => (
                  <div
                    key={row.label}
                    className="grid grid-cols-1 gap-1 sm:grid-cols-3"
                  >
                    <dt className="font-medium text-[#7D6149]">{row.label}</dt>
                    <dd className="sm:col-span-2">
                      {row.label === 'nagrody' ? (
                        <span className="inline-flex items-center gap-1.5 font-medium text-[#4A3525]">
                          <Award className="h-4 w-4 text-[#8C5A3C]" />
                          {row.value}
                        </span>
                      ) : (
                        <span
                          className={
                            row.isLink
                              ? 'cursor-pointer font-medium text-[#4A3525] underline decoration-[#CBB9A3] underline-offset-4 hover:text-[#6B4423]'
                              : 'text-[#3B2A1E]'
                          }
                        >
                          {row.value}
                        </span>
                      )}
                    </dd>
                  </div>
                ))}
              </dl>
            </div>
          </div>

          {/* PRAWA: GWIAZDKI, TAGI I PRZYCISKI AKCJI */}
          <div className="flex flex-col items-stretch justify-between rounded-xl border border-[#D5C5B2] bg-[#FAF6F0] p-4 md:col-span-3">
            <div>
              {/* Interaktywna ocena gwiazdkowa */}
              <p className="text-center text-xs font-semibold tracking-wide text-[#7D6149] uppercase">
                Twoja ocena
              </p>
              <div className="mt-2 flex items-center justify-center gap-1">
                {Array.from({ length: 5 }).map((_, idx) => {
                  const starValue = idx + 1
                  const active = (hoveredRating ?? userRating) >= starValue
                  return (
                    <button
                      key={starValue}
                      type="button"
                      onMouseEnter={() => setHoveredRating(starValue)}
                      onMouseLeave={() => setHoveredRating(null)}
                      onClick={() => setUserRating(starValue)}
                      className="cursor-pointer p-0.5 transition-transform hover:scale-110"
                    >
                      <Star
                        className={`h-6 w-6 ${
                          active
                            ? 'fill-[#8C5A3C] text-[#8C5A3C]'
                            : 'text-[#D5C5B2]'
                        }`}
                      />
                    </button>
                  )
                })}
              </div>

              {/* Tagi */}
              <div className="mt-4 flex flex-wrap justify-center gap-1.5">
                {['#sci-fi', '#kosmos', '#ekranizacja'].map((tag) => (
                  <span
                    key={tag}
                    className="rounded-md border border-[#D5C5B2] bg-[#F3ECE1] px-2 py-0.5 text-xs font-medium text-[#5C4534]"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>

            {/* 3 przyciski akcji ze szkicu */}
            <div className="mt-6 flex flex-col gap-2">
              <Button
                onClick={() => setAddedToList((prev) => !prev)}
                className={`w-full justify-center gap-2 text-xs font-semibold ${
                  addedToList
                    ? 'bg-[#4A3525] text-[#FAF6F0] hover:bg-[#3B2A1E]'
                    : 'bg-[#6B4423] text-[#FAF6F0] hover:bg-[#54341A]'
                }`}
              >
                {addedToList ? (
                  <>
                    <Check className="h-4 w-4" />
                    Dodano do listy
                  </>
                ) : (
                  <>
                    <Plus className="h-4 w-4" />
                    Dodaj do listy
                  </>
                )}
              </Button>

              <Button
                variant="outline"
                className="w-full justify-center gap-2 border-[#D5C5B2] bg-[#FAF6F0] text-xs font-semibold text-[#4A3525] hover:bg-[#E8DEC8]"
              >
                <Send className="h-3.5 w-3.5" />
                Wyślij znajomym
              </Button>

              <Button
                variant="outline"
                className="w-full justify-center gap-2 border-[#D5C5B2] bg-[#FAF6F0] text-xs font-semibold text-[#4A3525] hover:bg-[#E8DEC8]"
              >
                <MessageSquarePlus className="h-3.5 w-3.5" />
                Dodaj ocenę
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* ŚRODKOWA SEKCJA: OPIS DZIEŁA + OPINIE */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        {/* LEWA: OPIS FILMU / DZIEŁA */}
        <Card className="border-[#D5C5B2] bg-[#F3ECE1] text-[#3B2A1E] shadow-xs lg:col-span-5">
          <CardHeader>
            <CardTitle className="text-xl font-bold text-[#3B2A1E]">
              Opis filmu Projekt Hail Mary
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm leading-relaxed text-[#4A3525] sm:text-base">
              Nauczyciel nauk ścisłych Ryland Grace (Ryan Gosling) budzi się na
              statku kosmicznym lata świetlne od domu, nie pamiętając, kim jest
              ani jak się tam znalazł. Gdy wraca mu pamięć, zaczyna odkrywać
              swoją misję: rozwiązać zagadkę tajemniczej substancji powodującej
              wygaśnięcie słońca. Musi wykorzystać swoją wiedzę naukową i
              niekonwencjonalne pomysły, aby ocalić wszystko na Ziemi przed
              zagładą, ale nieoczekiwana przyjaźń oznacza, że być może nie będzie
              musiał robić tego sam.
            </p>
          </CardContent>
        </Card>

        {/* PRAWA: OPINIE O FILMIE */}
        <Card className="border-[#D5C5B2] bg-[#F3ECE1] text-[#3B2A1E] shadow-xs lg:col-span-7">
          <CardHeader className="pb-3">
            <CardTitle className="text-xl font-bold text-[#3B2A1E]">
              Opinie o filmie Projekt Hail Mary
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {REVIEWS.map((review) => {
              const isFollowed = followedAuthors.includes(review.id)
              const isLiked = likedReviews.includes(review.id)
              return (
                <div
                  key={review.id}
                  className="rounded-lg border border-[#D5C5B2] bg-[#FAF6F0] p-3.5"
                >
                  <span className="mb-1.5 block text-[11px] font-semibold tracking-wide text-[#8C6D53] uppercase">
                    {review.category}
                  </span>

                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div className="flex items-center gap-2">
                      <div className="flex h-7 w-7 items-center justify-center rounded-full bg-[#6B4423] text-xs font-bold text-[#FAF6F0]">
                        {review.author.charAt(0)}
                      </div>
                      <div>
                        <div className="flex items-center gap-1.5">
                          <span className="text-sm font-bold text-[#3B2A1E]">
                            {review.author}
                          </span>
                          <span className="inline-flex items-center gap-0.5 rounded bg-[#E8DEC8] px-1.5 py-0.5 text-xs font-bold text-[#6B4423]">
                            {review.rating}
                            <Star className="h-3 w-3 fill-[#8C5A3C] text-[#8C5A3C]" />
                          </span>
                        </div>
                        {review.badge && (
                          <span className="block text-[11px] text-[#7D6149]">
                            {review.badge}
                          </span>
                        )}
                      </div>
                    </div>

                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => toggleFollow(review.id)}
                      className={`h-7 gap-1 border-[#D5C5B2] text-xs ${
                        isFollowed
                          ? 'bg-[#6B4423] text-[#FAF6F0] hover:bg-[#54341A] hover:text-[#FAF6F0]'
                          : 'bg-[#F3ECE1] text-[#4A3525] hover:bg-[#E8DEC8]'
                      }`}
                    >
                      <UserPlus className="h-3 w-3" />
                      {isFollowed ? 'Obserwujesz' : 'Obserwuj'}
                    </Button>
                  </div>

                  <p className="mt-2.5 text-sm leading-relaxed text-[#3B2A1E]">
                    {review.content}
                  </p>

                  <div className="mt-3 flex items-center justify-between border-t border-[#E8DEC8] pt-2 text-xs text-[#7D6149]">
                    <div className="flex items-center gap-4">
                      <button
                        type="button"
                        onClick={() => toggleLike(review.id)}
                        className={`flex cursor-pointer items-center gap-1 font-medium transition-colors ${
                          isLiked ? 'text-[#6B4423]' : 'hover:text-[#3B2A1E]'
                        }`}
                      >
                        <ThumbsUp className="h-3.5 w-3.5" />
                        Lubię to! {review.likes + (isLiked ? 1 : 0)}
                      </button>
                      <span className="flex items-center gap-1">
                        <MessageSquare className="h-3.5 w-3.5" />
                        {review.commentsCount}
                      </span>
                    </div>
                    <span>{review.timeAgo}</span>
                  </div>
                </div>
              )
            })}
          </CardContent>
        </Card>
      </div>

      {/* DOLNA SEKCJA: MOŻE CI SIĘ SPODOBAĆ (REKOMENDACJE) */}
      <section className="rounded-xl border border-[#D5C5B2] bg-[#F3ECE1] p-5 shadow-xs">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-xl font-bold text-[#3B2A1E]">
            Może ci się spodobać (rekomendacje)
          </h2>
          <span className="text-xs font-medium text-[#7D6149]">
            Podobne tytuły
          </span>
        </div>

        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-8">
          {SIMILAR_WORKS.map((item) => (
            <article
              key={item.id}
              className="group relative flex aspect-2/3 cursor-pointer flex-col justify-between overflow-hidden rounded-lg border border-[#CBB9A3] p-2.5 text-[#FAF6F0] shadow-xs transition-transform hover:-translate-y-1"
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
  )
}