import { useState } from 'react'
import {
  Search,
  BookOpen,
  Film,
  Gamepad2,
  Music,
  Tv,
  BookMarked,
  Sparkles,
  Flame,
  Users,
  Feather,
  User,
  LogOut,
  Library,
  Mail,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
} from '@/components/ui/navigation-menu'

const BROWSE_CATEGORIES = [
  { label: 'Książki', href: '/books', icon: BookOpen },
  { label: 'Muzyka', href: '/music', icon: Music },
  { label: 'Gry', href: '/games', icon: Gamepad2 },
  { label: 'Filmy', href: '/films', icon: Film },
  { label: 'Seriale', href: '/series', icon: Tv },
  { label: 'Komiksy', href: '/comics', icon: BookMarked },
  { label: 'Mangi', href: '/manga', icon: Sparkles },
]

const COMMUNITY_LINKS = [
  { label: 'Popularne wśród społeczności', href: '/popular', icon: Flame },
  { label: 'Użytkownicy', href: '/users', icon: Users },
  { label: 'Autorzy', href: '/authors', icon: Feather },
]

interface HeaderProps {
  isAuthenticated: boolean
  username?: string
  onLoginClick?: () => void
  onLogoutClick?: () => void
  onHomeClick?: () => void
}

export function Header({
  isAuthenticated,
  username = 'Użytkownik',
  onLoginClick,
  onLogoutClick,
}: HeaderProps) {
  const [searchQuery, setSearchQuery] = useState('')

  return (
    <header className="sticky top-0 z-30 w-full border-b border-[#DFD3C3] bg-[#F3ECE1]/95 backdrop-blur-sm">
      <div className="mx-auto flex w-[92%] flex-wrap items-center justify-between gap-3 py-3 lg:w-[75%]">
        {/* Lewa strona: Logo + Wyszukiwarka */}
        <div className="flex min-w-0 flex-1 items-center gap-3">
          <a href="/" className="flex shrink-0 items-center gap-2.5">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[#6B4423] text-xs font-bold text-[#FAF6F0]">
              LOGO
            </div>
            <span className="text-xl font-bold text-[#4A3525]">Nerdiary</span>
          </a>

          <div className="relative ml-2 max-w-xs flex-1">
            <Search className="pointer-events-none absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2 text-[#8C6D53]" />
            <Input
              type="search"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Szukaj filmów, gier, książek..."
              className="h-9 border-[#D5C5B2] bg-[#FAF6F0] pl-9 text-sm text-[#3B2A1E] placeholder:text-[#9A7E66]"
            />
          </div>
        </div>

        {/* Środek: Rozwijane menu z dynamicznymi kategoriami */}
        <NavigationMenu className="hidden md:flex">
          <NavigationMenuList className="gap-1">
            {/* Zakładka: Przeglądaj */}
            <NavigationMenuItem>
              <NavigationMenuTrigger className="h-8 border border-[#D5C5B2] bg-[#FAF6F0] text-xs font-semibold text-[#4A3525] hover:bg-[#E8DEC8] hover:text-[#3B2A1E] data-[state=open]:bg-[#E8DEC8]">
                Przeglądaj
              </NavigationMenuTrigger>
              <NavigationMenuContent className="border-[#D5C5B2] bg-[#FAF6F0] p-2">
                <ul className="grid w-64 grid-cols-2 gap-1">
                  {BROWSE_CATEGORIES.map(({ label, href, icon: Icon }) => (
                    <li key={href}>
                      <NavigationMenuLink
                        href={href}
                        className="flex flex-row items-center gap-2 rounded-md px-3 py-2 text-xs font-medium text-[#3B2A1E] transition-colors hover:bg-[#E8DEC8] hover:text-[#6B4423]"
                      >
                        <Icon className="h-3.5 w-3.5 shrink-0 text-[#6B4423]" />
                        <span>{label}</span>
                      </NavigationMenuLink>
                    </li>
                  ))}
                </ul>
              </NavigationMenuContent>
            </NavigationMenuItem>

            {/* Zakładka: Społeczność */}
            <NavigationMenuItem>
              <NavigationMenuTrigger className="h-8 border border-[#D5C5B2] bg-[#FAF6F0] text-xs font-semibold text-[#4A3525] hover:bg-[#E8DEC8] hover:text-[#3B2A1E] data-[state=open]:bg-[#E8DEC8]">
                Społeczność
              </NavigationMenuTrigger>
              <NavigationMenuContent className="border-[#D5C5B2] bg-[#FAF6F0] p-2">
                <ul className="flex w-60 flex-col gap-1">
                  {COMMUNITY_LINKS.map(({ label, href, icon: Icon }) => (
                    <li key={href}>
                      <NavigationMenuLink
                        href={href}
                        className="flex flex-row items-center gap-2 rounded-md px-3 py-2 text-xs font-medium text-[#3B2A1E] transition-colors hover:bg-[#E8DEC8] hover:text-[#6B4423]"
                      >
                        <Icon className="h-3.5 w-3.5 shrink-0 text-[#6B4423]" />
                        <span>{label}</span>
                      </NavigationMenuLink>
                    </li>
                  ))}
                </ul>
              </NavigationMenuContent>
            </NavigationMenuItem>
          </NavigationMenuList>
        </NavigationMenu>

        {/* Prawa strona: Zależna od stanu zalogowania */}
        <div className="flex shrink-0 items-center gap-1.5">
          {isAuthenticated ? (
            <>
              <Button
                variant="ghost"
                size="sm"
                className="h-8 gap-1.5 text-xs font-semibold text-[#4A3525] hover:bg-[#E8DEC8]"
              >
                <Library className="h-3.5 w-3.5" />
                Biblioteka
              </Button>
              <Button
                variant="ghost"
                size="sm"
                className="h-8 gap-1.5 text-xs font-semibold text-[#4A3525] hover:bg-[#E8DEC8]"
              >
                <Mail className="h-3.5 w-3.5" />
                Inbox
              </Button>
              <Button
                variant="ghost"
                size="sm"
                className="h-8 gap-1.5 text-xs font-semibold text-[#4A3525] hover:bg-[#E8DEC8]"
              >
                <User className="h-3.5 w-3.5" />
                {username}
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={onLogoutClick}
                className="h-8 gap-1.5 border-[#D5C5B2] bg-[#FAF6F0] text-xs font-semibold text-[#4A3525] hover:bg-[#E8DEC8]"
              >
                <LogOut className="h-3.5 w-3.5" />
                Wyloguj
              </Button>
            </>
          ) : (
            <>
              <Button
                variant="ghost"
                size="sm"
                onClick={onLoginClick}
                className="h-8 text-xs font-semibold text-[#4A3525] hover:bg-[#E8DEC8]"
              >
                Zaloguj się
              </Button>
              <Button
                size="sm"
                className="h-8 bg-[#6B4423] text-xs font-semibold text-[#FAF6F0] hover:bg-[#54341A]"
              >
                Zarejestruj się
              </Button>
            </>
          )}
        </div>
      </div>
    </header>
  )
}