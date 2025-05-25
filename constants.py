# Screen def
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 768

# Asteroids
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 1.5  # seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

# Player size
PLAYER_RADIUS = 45
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 400

# Bullets
SHOT_RADIUS = 5
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN = 0.3

# UFO settings
UFO_RADIUS = 30
UFO_SPEED = 150
UFO_MIN_SPAWN_TIME = 10   # seconds
UFO_MAX_SPAWN_TIME = 30   # seconds

# --- POWER-UPS -------------------------------------------------------------- #
PU_SHIELD        = "shield"
PU_FAST_FIRE     = "fast_fire"
PU_SPREAD        = "spread_shot"
PU_NOVA          = "bullet_nova"
PU_THREAT        = "threat"

POWERUP_SPAWN_INTERVAL = 5.0        # s
POWERUP_RARITY = {
    PU_SPREAD: 0.30,
    PU_SHIELD: 0.25,
    PU_FAST_FIRE: 0.20,
    PU_NOVA:   0.15,
    PU_THREAT: 0.10,
}

PU_DURATION = {                     # sekundy dla efektów czasowych
    PU_SHIELD: 10,
    PU_FAST_FIRE: 15,
    PU_SPREAD: 30,
    PU_THREAT: 10,
}
FAST_FIRE_MULT   = 2.0              # × szybszy fire-rate
SPREAD_ANGLE     = 30               # ±° od osi statku
ASTEROID_SPAWN_BOOST = 2.0          # × częściej przy zagrożeniu