from pathlib import Path
import pygame

pygame.mixer.init(frequency=44_100, size=-16, channels=2, buffer=512)

SND_DIR = Path(__file__).resolve().parent / "assets" / "sound"

def _p(name: str) -> str:
    """Zamień nazwy plików na absolutne ścieżki w formacie str."""
    return str(SND_DIR / name)

SFX = {
    "laser":     pygame.mixer.Sound(_p("laser.wav")),
    "explosion": pygame.mixer.Sound(_p("explosion.wav")),
    "game_over": pygame.mixer.Sound(_p("game_over.wav")),
    "powerup": pygame.mixer.Sound(_p("powerup.wav")),
}

DEFAULT_SFX_VOL   = 0.5   # 0.0 – 1.0
DEFAULT_MUSIC_VOL = 1.0   # 0.0 – 1.0

for snd in SFX.values():
    snd.set_volume(DEFAULT_SFX_VOL)

pygame.mixer.music.set_volume(DEFAULT_MUSIC_VOL)

def play_sfx(name: str) -> None:
    if snd := SFX.get(name):
        snd.play()

# ---------- MUZYKA W TLE ---------- #
def _play_music(file: str, loop: int = -1) -> None:
    pygame.mixer.music.stop()
    pygame.mixer.music.load(_p(file))
    pygame.mixer.music.play(loop)

def intro()      -> None: _play_music("intro.mp3")
def theme()      -> None: _play_music("theme.mp3")
def stop_music() -> None: pygame.mixer.music.stop()
