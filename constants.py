"""
constants.py

Zestaw stałych konfiguracyjnych wykorzystywanych przez wszystkie moduły gry.
Dzięki zcentralizowaniu wartości łatwo dostosować poziom trudności oraz
sparametryzować zachowanie poszczególnych obiektów - bez konieczności
przepisywania kodu w wielu miejscach.

Konwencje:
- nazwy pisane **CAPSLOCKIEM** wskazują na niezmienność w trakcie działania gry,
- sekcje oddzielone #- przegrodami dzielą stałe logicznie (ekran, gracz, UFO…),
- jednostki: jeśli nie zaznaczono inaczej → _piksele_ lub _sekundy_.

Wartości UFO_MIN/MAX_SPAWN_TIME oraz POWERUP_SPAWN_INTERVAL zostaly "podkrecone"
na potrzeby testow - mozliwosci napotkania kazdego power-upa w kilka minut.
"""

# --- USTAWIENIA EKRANU ------------------------------------------------------ #
SCREEN_WIDTH  = 1280      # szerokość okna gry
SCREEN_HEIGHT =  768      # wysokość okna gry

# --- ASTEROIDY -------------------------------------------------------------- #
ASTEROID_MIN_RADIUS = 20          # promień najmniejszego fragmentu
ASTEROID_KINDS      = 3           # ile „pokoleń” rozpadu (large→medium→small)
ASTEROID_SPAWN_RATE = 1.5         # średni odstęp między nowymi asteroidami [s]
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS  # 60 px dla large

# --- GRACZ / STATEK --------------------------------------------------------- #
PLAYER_RADIUS     = 45   # rozmiar okręgu kolizji statku
PLAYER_TURN_SPEED = 300  # °/s – prędkość obrotu
PLAYER_SPEED      = 400  # px/s – prędkość liniowa przy pełnym ciągu

# --- POCISKI --------------------------------------------------------------- #
SHOT_RADIUS          = 5     # hit‑box zwykłego pocisku
PLAYER_SHOOT_SPEED   = 500   # px/s – prędkość wylotu
PLAYER_SHOOT_COOLDOWN = 0.3  # s – minimalny odstęp między strzałami

# --- UFO ------------------------------------------------------------------- #
UFO_RADIUS        = 30   # rozmiar kolizji małego UFO (większych brak)
UFO_SPEED         = 150  # px/s – prędkość liniowa
UFO_MIN_SPAWN_TIME = 10  # s – minimalny czas do pojawienia
UFO_MAX_SPAWN_TIME = 30  # s – maksymalny czas do kolejnego pojawienia

# --- POWER‑UPY ------------------------------------------------------------- #
PU_SHIELD     = "shield"       # nieśmiertelność na czas trwania
PU_FAST_FIRE  = "fast_fire"    # szybsze strzelanie
PU_SPREAD     = "spread_shot"  # trzy pociski w rozrzucie
PU_NOVA       = "bullet_nova"  # pierścień pocisków dookoła
PU_THREAT     = "threat"       # więcej asteroid (dla punktów)

POWERUP_SPAWN_INTERVAL = 5.0   # s – losowanie co X sekund

# Prawdopodobieństwo wylosowania danego power‑upu (suma = 1.0)
POWERUP_RARITY = {
    PU_SPREAD:    0.30,
    PU_SHIELD:    0.25,
    PU_FAST_FIRE: 0.20,
    PU_NOVA:      0.15,
    PU_THREAT:    0.10,
}

# Długość trwania efektów czasowych [s]; 0 → efekt natychmiastowy
PU_DURATION = {
    PU_SHIELD:    10,
    PU_FAST_FIRE: 15,
    PU_SPREAD:    30,
    PU_THREAT:    10,
    PU_NOVA:       0,
}

FAST_FIRE_MULT     = 2.0  # × – mnożnik szybkości strzału podczas FAST_FIRE
SPREAD_ANGLE       = 30   # ° – maks. odchylenie bocznych pocisków
ASTEROID_SPAWN_BOOST = 2.0  # × – przy THREAT: asteroid dwa razy więcej