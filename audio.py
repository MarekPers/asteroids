"""
audio.py

Odpowiada za inicjalizację silnika audio `pygame.mixer`,
wczytywanie plików dźwiękowych oraz
udostępnienie pomocniczych funkcji do odtwarzania
efektów dźwiękowych (SFX) i muzyki w tle.
Wszystkie ścieżki dźwiękowe trzymane są wewnątrz katalogu
`assets/sound` i ładowane są przy starcie modułu.
"""

from pathlib import Path
import pygame

pygame.mixer.init(frequency=44_100, size=-16, channels=2, buffer=512)
# Inicjalizacja miksera – częstotliwość 44,1 kHz, 16‑bit, stereo, bufor 512 próbek

SND_DIR = Path(__file__).resolve().parent / "assets" / "sound"
# Bazowy katalog z plikami .wav/.mp3

def _p(name: str) -> str:
    # Funkcja pomocnicza – konwertuje nazwę pliku audio na absolutną ścieżkę, aby Pygame mógł ją otworzyć
    return str(SND_DIR / name)

SFX = {
    "laser":     pygame.mixer.Sound(_p("laser.wav")),
    "explosion": pygame.mixer.Sound(_p("explosion.wav")),
    "game_over": pygame.mixer.Sound(_p("game_over.wav")),
    "powerup": pygame.mixer.Sound(_p("powerup.wav")),
}
# Słownik gotowych efektów dźwiękowych – kluczem jest opisowa nazwa używana w kodzie gry.

DEFAULT_SFX_VOL   = 0.5   # 0.0 – 1.0
DEFAULT_MUSIC_VOL = 1.0   # 0.0 – 1.0
# Domyślne poziomy głośności ustawiane tuż po załadowaniu wszystkich efektów.

for snd in SFX.values():
    snd.set_volume(DEFAULT_SFX_VOL)
# Ustaw jednakową głośność dla każdego załadowanego efektu.

pygame.mixer.music.set_volume(DEFAULT_MUSIC_VOL)
# Głośność muzyki w tle (ścieżki mp3) ustawiana niezależnie od SFX.

def play_sfx(name: str) -> None:
    # Odtwórz pojedynczy efekt dźwiękowy na podstawie jego klucza z słownika SFX.
    # Jeśli dźwięk nie istnieje (błędny klucz) funkcja nie robi nic.
    if snd := SFX.get(name):
        snd.play()

def _play_music(file: str, loop: int = -1) -> None:
    # Wewnętrzna funkcja przełączająca aktualny utwór w tle.
    # `loop=-1` oznacza nieskończone zapętlenie.
    pygame.mixer.music.stop()
    pygame.mixer.music.load(_p(file))
    pygame.mixer.music.play(loop)

# Poniższe jednolinijkowce ułatwiają zmianę aktualnej ścieżki poprzez jednoznacznie
# nazwane wywołania w pozostałych modułach gry.
def intro()      -> None: _play_music("intro.mp3")
def theme()      -> None: _play_music("theme.mp3")
def stop_music() -> None: pygame.mixer.music.stop()
