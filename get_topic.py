import modules
import random

# Load visited subreddits from file (if it exists)
SUBREDDITS_CHECKED = []

SUBREDDITS = [
    "pics", "EarthPorn", "CityPorn", "SkyPorn", "WaterPorn", "ExposurePorn",
    "MacroPorn", "AnimalPorn", "ArchitecturePorn", "NatureIsFuckingLit",
    "AbandonedPorn", "ITookAPicture", "GeologyPorn", "spaceporn",
    "astrophotography", "AccidentalRenaissance", "CozyPlaces", "RoomPorn",
    "DesignPorn", "ImaginaryLandscapes", "Illustration", "PixelArt",
    "wholesomememes", "BeAmazed", "interestingasfuck", "MostBeautiful",
    "BirdPics", "LongExposurePorn", "WeatherPorn", "MountainPorn", "ForestPorn",
    "SunsetPorn", "CloudPorn", "StormPorn", "AuroraPorn", "MilkyWayPorn",
    "DronePorn", "AerialPorn", "HDRPorn", "PanoramaPorn",
    "oddlysatisfying", "mildlyinteresting", "nextfuckinglevel", "woahdude",
    "Damnthatsinteresting", "submechanophobia", "MicroPorn", "Pareidolia",
    "UrbanHell", "LiminalSpace", "ruralporn", "AbsoluteUnits", "glitch_art",
    "ImaginaryNetwork", "ImaginaryCharacters", "ImaginaryMonsters",
    "ImaginarySliceOfLife", "wildlifephotography", "naturephotography",
    "landscapephotography", "BlackAndWhitePhotos", "analog", "wallpaper",
    "oldschoolcool", "foodporn"
]

def get_topic():
    global SUBREDDITS_CHECKED

    # Load visited from file
    try:
        with open('Day 52 - Reddit Bot/visited.txt', 'r') as f:
            SUBREDDITS_CHECKED = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        SUBREDDITS_CHECKED = []

    now = modules.datetime.now()
    print("📜 Already explored:", SUBREDDITS_CHECKED)

    # Filter available subreddits (ensure no duplicates, only valid ones)
    available_subreddits = [f"r/{s}" for s in SUBREDDITS if f"r/{s}" not in SUBREDDITS_CHECKED]

    if not available_subreddits:
        print("⚠️ No available subreddits left. Resetting visited list.")
        SUBREDDITS_CHECKED = []
        available_subreddits = [f"r/{s}" for s in SUBREDDITS]

    #valid response from LLM (max 3 attempts)
    response = None
    for attempt in range(3):
        topic = modules.ollama.generate(
            model='llava:13b',
            prompt=f"""
            You are a strict subreddit selector. Follow these rules exactly:

            1. Output ONLY the subreddit name with "r/" at the beginning.
            2. Do NOT include any explanations, greetings, or extra words.
            3. Your entire response must be exactly one line from the list below.

            Current time: {now.strftime("%A, %B %d %Y, %I:%M %p")}
            Current hour: {now.hour}
            Day of week: {now.strftime("%A")}

            Available subreddits (choose exactly one):
            {", ".join(available_subreddits)}

            Examples of correct output:
            r/CozyPlaces
            r/naturephotography

            Now output ONLY the subreddit name from the list above. No other text.
            """,
            options={'temperature': 0.0}
        )
        candidate = topic['response'].strip()

        if candidate in available_subreddits:
            response = candidate
            break
        else:
            print(f"⚠️ LLM gave invalid response: '{candidate}'. Retrying ({attempt+1}/3)...")

    # Fallback: pick a random available subreddit if LLM fails
    if response is None:
        response = random.choice(available_subreddits)
        print(f"⚠️ Using random fallback: {response}")

    # Append to memory and file (only if not already there, but file read ensures that)
    if response not in SUBREDDITS_CHECKED:
        SUBREDDITS_CHECKED.append(response)
        with open('Day 52 - Reddit Bot/visited.txt', 'a') as f:
            f.write(response + '\n')

    print("🤖 AI chose :", response)
    print(f"✅ Added {response} to visited list")
    return response