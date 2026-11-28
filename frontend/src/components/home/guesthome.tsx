import { Star, Users, Tags, Library, Sparkles } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface MediaItem {
  id: number
  title: string
  category: string
  rating: string
  coverColor: string
  coverImage: string
}

const POPULAR_WORKS: MediaItem[] = [
  { id: 1, title: 'Diuna: Część druga', category: 'Film', rating: '9.1', coverColor: 'from-amber-800 to-stone-900', coverImage: 'https://fwcdn.pl/fpo/34/81/10003481/8115126_1.8.webp' },
  { id: 2, title: 'Wiedźmin 3: Dziki Gon', category: 'Gra', rating: '9.6', coverColor: 'from-stone-700 to-amber-950', coverImage: 'https://shared.steamstatic.com/store_item_assets/steam/apps/292030/ed3c01933d74aea0d54b38cef46fc387154bfdb7/library_600x900_polish_2x.jpg?t=1755527653' },
  { id: 3, title: 'Lalka', category: 'Książka', rating: '8.4', coverColor: 'from-amber-700 to-orange-950', coverImage: 'https://s.lubimyczytac.pl/upload/books/5256000/5256788/1388689-352x500.jpg' },
  { id: 4, title: 'Oppenheimer', category: 'Film', rating: '8.9', coverColor: 'from-orange-800 to-neutral-900', coverImage: 'https://fwcdn.pl/fpo/28/17/10002817/8072064_2.10.webp' },
  { id: 5, title: 'Cyberpunk 2077', category: 'Gra', rating: '8.8', coverColor: 'from-yellow-700 to-stone-900', coverImage: 'https://cdn2.steamgriddb.com/grid/4030e2eebb977639f8836aa25a293e40.png' },
  { id: 6, title: 'Szklany tron', category: 'Książka', rating: '8.7', coverColor: 'from-stone-600 to-stone-900', coverImage: 'https://s.lubimyczytac.pl/upload/books/5126000/5126665/1174004-352x500.jpg' },
  { id: 7, title: 'Blade Runner 2049', category: 'Film', rating: '9.0', coverColor: 'from-amber-900 to-neutral-950', coverImage: 'https://fwcdn.pl/fpo/07/98/630798/7801880_1.10.webp' },
  { id: 8, title: 'Hunting High and Low', category: 'Muzyka', rating: '9.3', coverColor: 'from-yellow-800 to-stone-950', coverImage: 'https://upload.wikimedia.org/wikipedia/en/8/8f/Hunting_High_and_Low.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=original' },
  { id: 9, title: 'Cień i kość', category: 'Książka', rating: '8.9', coverColor: 'from-orange-900 to-stone-900', coverImage: 'https://s.lubimyczytac.pl/upload/books/4858000/4858578/1113535-352x500.jpg' },
  { id: 10, title: 'Baldur’s Gate 3', category: 'Gra', rating: '9.7', coverColor: 'from-amber-800 to-red-950', coverImage: 'https://shared.steamstatic.com/store_item_assets/steam/apps/1086940/library_600x900_2x.jpg?t=1748345785' },
]

const RECENTLY_ADDED: MediaItem[] = [
  { id: 11, title: 'Hollow Knight', category: 'Gra', rating: '9.4', coverColor: 'from-stone-800 to-neutral-950', coverImage: 'https://cdn2.steamgriddb.com/grid/d18c832e8c956b4ef8b92862e6bf470d.png' },
  { id: 12, title: 'Elden Ring', category: 'Gra', rating: '9.5', coverColor: 'from-amber-700 to-stone-900', coverImage: 'https://cdn2.steamgriddb.com/grid/557fa68027943a8b0d3b66c4e72ff23b.png' },
  { id: 13, title: 'Minecraft', category: 'Gra', rating: '9.0', coverColor: 'from-emerald-900 to-stone-900', coverImage: 'https://cdn2.steamgriddb.com/grid/a73027901f88055aaa0fd1a9e25d36c7.png' },
  { id: 14, title: "Spider-Man: Całkiem nowy dzień", category: 'Film', rating: '8.6', coverColor: 'from-red-900 to-stone-950', coverImage: 'https://fwcdn.pl/fpo/80/64/10068064/8251872.10.webp' },
  { id: 15, title: 'God of War', category: 'Gra', rating: '9.3', coverColor: 'from-stone-700 to-amber-950', coverImage: 'https://cdn2.steamgriddb.com/grid/368b80128d9e529adf93f7ce84dfaca0.jpg' },
  { id: 16, title: 'Detroit: Become Human', category: 'Gra', rating: '8.8', coverColor: 'from-amber-800 to-neutral-900', coverImage: 'https://cdn2.steamgriddb.com/grid/2078750ea356ba9fd472655dec36c068.png' },
  { id: 17, title: 'Zbrodnia i kara', category: 'Książka', rating: '9.2', coverColor: 'from-stone-800 to-amber-950', coverImage: 'https://s.lubimyczytac.pl/upload/books/5191000/5191464/1274660-352x500.jpg' },
  { id: 18, title: 'Incepcja', category: 'Film', rating: '9.1', coverColor: 'from-orange-950 to-stone-900', coverImage: 'https://fwcdn.pl/fpo/08/91/500891/7354571_1.10.webp' },
]

const INFO_SECTIONS = [
  {
    title: 'Czym jest Nerdiary?',
    description:
      'Nerdiary to Twoje osobiste centrum kultury i rozrywki. Jedno spójne miejsce, w którym zbierzesz wszystkie obejrzane filmy, ograne tytuły, przeczytane książki oraz przesłuchane albumy muzyczne.',
    icon: Sparkles,
  },
  {
    title: 'Uzupełniaj swoją kolekcję dzieł',
    description:
      'Oznaczaj tytuły jako ukończone, w trakcie lub planowane. Śledź swoje postępy i miej zawsze pod ręką pełną historię tego, co już poznałeś i po co zamierzasz sięgnąć w najbliższym czasie.',
    icon: Library,
  },
  {
    title: 'Pisz recenzje',
    description:
      'Wystawiaj oceny w skali od 1 do 10, zapisuj własne przemyślenia po seansie lub lekturze i dziel się dłuższymi recenzjami ze społecznością Nerdiary.',
    icon: Star,
  },
  {
    title: 'Dodawaj znajomych i polecaj im dzieła',
    description:
      'Obserwuj aktywność znajomych, sprawdzaj, co ostatnio ocenili i wysyłaj im bezpośrednie rekomendacje tytułów, które koniecznie muszą poznać.',
    icon: Users,
  },
  {
    title: 'Twórz własne listy i tagi — Segreguj jak lubisz',
    description:
      'Buduj autorskie zestawienia tematyczne (np. „Najlepsze sci-fi lat 90.” albo „Książki na urlop”), oznaczaj dzieła własnymi tagami i filtruj swoją bibliotekę dokładnie według własnych zasad.',
    icon: Tags,
  },
]

interface GuestHomeProps {
  onLoginClick?: () => void
  onRegisterClick?: () => void
  onSelectMedia?: (id: number) => void // <-- dodaj ten prop
}

export function GuestHome({ onLoginClick, onRegisterClick }: GuestHomeProps) {
  return (
    <div className="flex flex-col gap-6">
      {/* BANER POWITALNY (CTA) */}
      <section className="rounded-xl border border-[#D5C5B2] bg-[#F3ECE1] px-6 py-5 shadow-xs">
        <h1 className="text-center text-lg font-bold text-[#3B2A1E] sm:text-xl">
          Załóż swoją wirtualną bibliotekę z Nerdiary już dzisiaj!
        </h1>
        <div className="mt-3 flex flex-wrap items-center justify-between gap-2 border-t border-[#E2D6C5] pt-3 text-sm">
          <button
            type="button"
            onClick={onLoginClick}
            className="cursor-pointer font-semibold text-[#6B4423] underline-offset-4 hover:underline"
          >
            Zaloguj się.
          </button>
          <span className="text-[#6E543E]">
            Nie masz konta?{' '}
            <button
              type="button"
              onClick={onRegisterClick}
              className="cursor-pointer font-semibold text-[#6B4423] underline-offset-4 hover:underline"
            >
              Zarejestruj się
            </button>
          </span>
        </div>
      </section>

      {/* SEKCJA 1: POPULARNE DZIEŁA */}
      <section className="rounded-xl border border-[#D5C5B2] bg-[#F3ECE1] p-5 shadow-xs">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-xl font-bold text-[#3B2A1E]">
            Popularne dzieła
          </h2>
          <span className="text-xs font-medium text-[#7D6149]">
            Top 10 w tym tygodniu
          </span>
        </div>

        <div className="grid grid-cols-2 gap-3 sm:grid-cols-5 lg:grid-cols-10">
          {POPULAR_WORKS.map((item, index) => (
            <article
              key={item.id}
              className="group relative flex aspect-2/3 cursor-pointer flex-col justify-between overflow-hidden rounded-lg border border-[#CBB9A3] p-2 text-[#FAF6F0] shadow-xs transition-transform hover:-translate-y-1"
            >
              <img src={item.coverImage} alt={item.title} loading="lazy" className="absolute inset-0 h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"></img>
              <div
                className={`absolute inset-0 bg-gradient-to-b ${item.coverColor} opacity-65`}
              />
              {/* Odznaka oceny */}
              <div className="relative z-10 flex items-center justify-between">
                <span className="rounded bg-[#FAF6F0]/20 px-1.5 py-0.5 text-[10px] font-semibold backdrop-blur-xs">
                  {item.category}
                </span>
                <span className="rounded bg-amber-500/90 px-1 text-[10px] font-bold text-stone-950">
                  {item.rating}
                </span>
              </div>

              {/* Numer rankingu i tytuł */}
              <div className="relative z-10">
                <span className="block text-lg leading-none font-black text-[#FAF6F0]/90 drop-shadow">
                  {index + 1}
                </span>
                <h3 className="mt-1 line-clamp-2 text-[11px] leading-tight font-medium text-[#FAF6F0]">
                  {item.title}
                </h3>
              </div>
            </article>
          ))}
        </div>
      </section>

      {/* SEKCJA 2: OSTATNIO DODANE */}
      <section className="rounded-xl border border-[#D5C5B2] bg-[#F3ECE1] p-5 shadow-xs">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-xl font-bold text-[#3B2A1E]">
            Ostatnio dodane
          </h2>
          <span className="text-xs font-medium text-[#7D6149]">
            Nowości w katalogu
          </span>
        </div>

        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-8">
          {RECENTLY_ADDED.map((item) => (
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

      {/* SEKCJE INFORMACYJNE (5 KART Z MAKIETY) */}
      <div className="flex flex-col gap-4">
        {INFO_SECTIONS.map(({ title, description, icon: Icon }) => (
          <Card
            key={title}
            className="border-[#D5C5B2] bg-[#F3ECE1] text-[#3B2A1E] shadow-xs transition-colors hover:border-[#B69D82]"
          >
            <CardHeader className="pb-2">
              <CardTitle className="flex items-center gap-2.5 text-xl font-bold text-[#3B2A1E]">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-[#E4D7C5] text-[#6B4423]">
                  <Icon className="h-4 w-4" />
                </div>
                {title}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm leading-relaxed text-[#5C4534] sm:text-base">
                {description}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}