import random

# Winter weather outcomes – cold, frost, and frequent snowfall.
winter_weather = {
    "morning": [
        ("clear with a light dusting of frost and a brisk, dry chill", 5),
        ("overcast with low gray clouds and a gentle, steady snowfall", 8),
        ("partly cloudy with scattered flurries and a sharp, invigorating cold", 6),
        ("cloudy with a light, steady snow shower and a crisp, biting chill", 7),
        ("clear with a pronounced frost and a piercing, refreshing cold", 4),
        ("mostly clear with subtle flurries and a clean, invigorating chill", 5),
        ("partly cloudy with intermittent flurries and a quiet, renewing chill", 6),
        ("overcast with a light snow shower and a steady, biting chill", 7),
        ("clear with an invigorating chill and a sparse scattering of flurries", 4),
        ("overcast with continuous light snowfall and a noticeably piercing chill", 8),
        ("partly cloudy with subtle snow flurries and a crisp, awakening chill", 6),
        ("cloudy with a delicate mix of light snow and a refreshing, piercing frost", 7),
        ("overcast with heavy snowfall and strong winds, creating near-whiteout conditions", 5),
        ("partly cloudy with icy patches and a biting wind that cuts through the air", 6),
        ("cloudy with freezing rain and a slick, icy glaze covering everything", 4)
    ],
    "afternoon": [
        ("clear with a dominant blue sky and an intense, biting cold", 4),
        ("partly cloudy with periodic bursts of snow flurries and gusty winds", 6),
        ("overcast with continuous moderate snowfall and a relentless, piercing chill", 8),
        ("cloudy with steady, light snow and a robust, unyielding cold", 7),
        ("clear with a harsh, unyielding cold and sporadic flurries", 5),
        ("overcast with persistent snow showers and a biting wind that intensifies the chill", 8),
        ("partly cloudy with isolated snow showers and a severe, cutting cold", 6),
        ("cloudy with a steady, drenching snow and gusts whipping the cold air", 7),
        ("clear with an icy calm punctuated by erratic snow bursts and a severe, raw cold", 5),
        ("overcast with relentless snowfall and powerful gusts that create a dramatically cold scene", 8),
        ("partly cloudy with intermittent snow and a sharp, stinging cold", 6),
        ("clear with a severe, dry cold and isolated, erratic flurries carried by biting winds", 5),
        ("overcast with sleet and freezing rain, making roads and sidewalks treacherous", 7),
        ("partly cloudy with a mix of snow and rain, creating slushy, messy conditions", 6)
    ],
    "evening": [
        ("partly cloudy with a soft drizzle and a gentle, fading chill leaving a delicate frost", 5),
        ("overcast with intermittent light snow and a moderate, receding cold hinting at thaw", 6),
        ("clear with a gradual easing of chill and sparse snowfall quietly settling", 4),
        ("cloudy with a light, steady drizzle and a soft, diminishing chill", 5),
        ("partly cloudy with a transient snow shower and a mild, soothing chill at dusk", 6),
        ("overcast with a soft drizzle and a slow, calming decline in cold intensity", 7),
        ("clear with a subtle easing of cold and occasional light flurries at twilight", 5),
        ("cloudy with intermittent flurries and a gradually fading chill", 6),
        ("partly cloudy with a light, intermittent drizzle that gently moderates the lingering cold", 5),
        ("overcast with a brief, light snowfall and a mild, calming chill", 7),
        ("clear with a delicate easing of cold and a trace of evaporating frost", 4),
        ("partly cloudy with a transient drizzle and a modest, diminishing chill", 6),
        ("overcast with freezing rain and a slick, icy coating on surfaces", 5)
    ],
    "night": [
        ("overcast with a heavy blanket of dark clouds, fierce winds, and a relentless, piercing cold", 7),
        ("partly cloudy with scattered, shifting clouds and intermittent intense icy gusts", 6),
        ("clear with a nearly cloudless expanse dominated by an overpowering, bone-chilling cold and shimmering frost", 5),
        ("cloudy with a thick blanket of clouds and a severe, piercing cold", 7),
        ("mostly overcast with turbulent winds and heavy snow creating a deeply penetrating, numbing cold", 8),
        ("partly cloudy with isolated breaks revealing an icy, starlit sky and a sharp chill", 6),
        ("overcast with a persistent, unyielding cold and a dense, gloomy cloud cover", 7),
        ("clear with a sudden drop in temperature, punctuated by a few wispy clouds in the freezing night", 5),
        ("cloudy with a full, dark sky and an intense, stinging cold that blankets the landscape in ice", 8),
        ("partly cloudy with a sparse scattering of thin clouds and a penetrating, frigid chill", 6),
        ("overcast with brooding, heavy clouds and a deep, numbing cold", 7),
        ("clear with an almost cloudless, starry sky yet ruled by an uncompromising, bone-deep cold", 5),
        ("overcast with freezing rain and a slick, icy glaze covering everything", 6)
    ]
}

# Spring weather outcomes – mild with moderate rainfall.
spring_weather = {
    "morning": [
        ("mostly clear with a light drizzle and a refreshing, cool dampness that softens the air", 7),
        ("clear with a soft mist and a gentle, awakening cool moisture", 8),
        ("partly cloudy with intermittent showers and a crisp, invigorating coolness", 6),
        ("overcast with a delicate shower and a subtle, enlivening moist air", 5),
        ("mostly clear with a transient drizzle and a brisk, rejuvenating coolness", 7),
        ("clear with a brief mist imparting soft, refreshing cool dampness", 8),
        ("partly cloudy with a whisper of rain that gently imbues the morning with fresh moisture", 6),
        ("overcast with steady light drizzle and a calm, refreshing cool moisture", 5),
        ("mostly clear with a soft, fleeting drizzle that awakens gentle, crisp coolness", 7),
        ("clear with intermittent light showers that lend subtle, invigorating cool dampness", 8),
        ("partly cloudy with delicate raindrops that provide a quiet, refreshing cool air", 6),
        ("overcast with a modest, persistent drizzle that softly revives the cool morning moisture", 5),
        ("partly cloudy with a mix of sun and rain, creating a vibrant, refreshing atmosphere", 7),
        ("overcast with steady rain and a cool, damp breeze", 6)
    ],
    "afternoon": [
        ("clear with intermittent moderate rain and a balanced, refreshing moistness", 7),
        ("mostly clear with steady light showers and a vibrant, refreshing dampness", 8),
        ("partly cloudy with regular rain bursts that infuse the air with a crisp, invigorating moisture", 6),
        ("overcast with periodic rain bursts that evenly refresh the atmosphere", 5),
        ("clear with rhythmic moderate showers that evenly rejuvenate the air", 7),
        ("mostly clear with a sequence of light rain episodes sustaining a steady, cooling dampness", 8),
        ("partly cloudy with consistent moderate rain that quietly energizes the air", 6),
        ("clear with sporadic bursts of refreshing rain that subtly elevate the moist ambiance", 5),
        ("mostly clear with a refreshing cadence of showers gently imbued with cool moisture", 7),
        ("clear with periodic light showers steadily infusing the air with fresh, cool moisture", 8),
        ("partly cloudy with intermittent rain providing a crisp, refreshing moist feel", 6),
        ("overcast with recurring gentle showers consistently enlivening the moist atmosphere", 5),
        ("partly cloudy with a mix of sun and rain, creating a vibrant, refreshing atmosphere", 7),
        ("overcast with steady rain and a cool, damp breeze", 6)
    ],
    "evening": [
        ("partly cloudy with a soft drizzle and a gentle, receding cool moisture that eases dusk", 7),
        ("overcast with intermittent light showers and a quiet, gradually fading moist air", 6),
        ("clear with a brief rain and a mild, soothing moisture at dusk", 8),
        ("cloudy with a light shower and a subtle, diminishing cool dampness", 7),
        ("mostly clear with a transient rain gradually yielding gentle, soothing cool moistness", 8),
        ("partly cloudy with quiet, intermittent drizzle softly diminishing the residual warmth", 6),
        ("overcast with a brief, tender shower that smoothly transitions into delicate, receding moisture", 7),
        ("clear with a fleeting rain gently subsiding into soft, refreshing moistness", 8),
        ("partly cloudy with soft, scattered showers slowly easing the fading heat with gentle moisture", 6),
        ("overcast with a modest drizzle gradually mellowing into soft, quiet cool dampness", 7),
        ("clear with a subtle drizzle gently retreating, leaving delicate, refreshing cool moisture", 8),
        ("partly cloudy with a light, sporadic drizzle gradually diminishing the evening’s moist air", 6),
        ("overcast with steady rain and a cool, damp breeze", 7)
    ],
    "night": [
        ("overcast with steady, light rain and a cool, persistent dampness blanketing the night", 7),
        ("cloudy with continuous drizzle and a lingering, cool moisture softly pervading the dark", 8),
        ("mostly overcast with gentle, ongoing rain and a calm, cool damp air settling quietly", 6),
        ("overcast with consistent drizzle and a steady, refreshing cool moisture that endures", 7),
        ("overcast with a quiet, unwavering drizzle sustaining a cool, mellow dampness", 8),
        ("cloudy with soft, continuous rain gently upholding a cool, enduring moisture", 6),
        ("mostly overcast with subtle, persistent drizzle preserving a cool, refreshing dampness", 7),
        ("overcast with steady, soft rain gently maintaining a calm, refreshing cool moisture", 8),
        ("cloudy with restrained, ongoing drizzle subtly preserving the cool dampness", 6),
        ("mostly overcast with low-key, continuous rain quietly refreshing the cool night", 7),
        ("overcast with gentle, persistent showers delicately maintaining a cool, soft moisture", 8),
        ("cloudy with a faint, ongoing drizzle softly holding refreshing cool dampness", 6),
        ("overcast with steady rain and a cool, damp breeze", 7)
    ]
}

# Summer weather outcomes – warm and humid with occasional thunderstorms.
summer_weather = {
    "morning": [
        ("mostly clear with sparse high clouds and a refreshing, cool breeze gently awakening the day", 8),
        ("clear with a light scattering of wispy clouds and a mild, soothing coolness invigorating the morning", 9),
        ("partly cloudy with a few thin, drifting clouds and a crisp, refreshing coolness setting a lively tone", 7),
        ("overcast with diffused light and a gentle, moderate coolness offering brief respite", 5),
        ("mostly clear with intermittent wisps of cloud providing subtle, cooling modulation to the crisp air", 7),
        ("clear with an almost pristine sky punctuated by delicate, transient clouds lightly cooling the morning", 9),
        ("partly cloudy with a faint layer of high clouds subtly tempering the early brightness", 7),
        ("overcast with soft, diffuse cloud cover gently moderating a refreshing, cool start", 5),
        ("mostly clear with a gentle interplay of light clouds imbuing the morning with invigorating coolness", 7),
        ("clear with a modest scattering of high clouds enhancing a refreshing, clean coolness", 9),
        ("partly cloudy with a delicate mist of clouds softly augmenting the refreshing cool ambiance", 7),
        ("overcast with an airy cloud cover subtly infusing the morning with a soothing cool breeze", 5)
    ],
    "afternoon": [
        ("clear with a vivid blue sky and an intense, searing heat dominating the scene", 5),
        ("mostly clear with an almost unbroken blue expanse and a blazing, relentless sun scorching the day", 5),
        ("a brilliant blue sky with strong, direct sunlight and overpowering, searing heat", 5),
        ("overcast with a thin, wispy layer of clouds barely softening the severe, unyielding heat", 4),
        ("clear with a stark blue expanse intensifying the extreme, burning heat of the afternoon", 5),
        ("mostly clear with sporadic delicate clouds offering little relief from oppressive, sweltering heat", 4),
        ("clear with an unclouded sky magnifying the fierce, unrelenting sun and its scorching heat", 5),
        ("mostly clear with a pristine blue dome failing to mitigate the overwhelming, intense heat", 5),
        ("clear with a dominant blue sky accentuating the harsh, persistent, scorching warmth", 5),
        ("mostly clear with an expansive, vivid blue underscoring the searing, unremitting heat", 5),
        ("clear with a pure blue canopy amplifying the relentless, burning heat", 5),
        ("mostly clear with an immaculate blue sky and unyielding, intense burning heat", 5),
        ("partly cloudy with building cumulus clouds and a chance of scattered thunderstorms later in the day", 6),
        ("overcast with thick, gray clouds and a humid, oppressive feel, signaling an approaching thunderstorm", 7),
        ("partly cloudy with occasional rain showers and a muggy, sticky atmosphere", 6),
        ("overcast with steady, light rain and a cool, refreshing break from the heat", 5),
        ("partly cloudy with sudden, intense thunderstorms and gusty winds, followed by a cooler breeze", 6),
        ("overcast with a steady drizzle and a noticeable drop in temperature, offering relief from the heat", 5),
        ("partly cloudy with isolated thunderstorms and a mix of sun and rain throughout the afternoon", 6),
        ("overcast with heavy rain and occasional thunder, creating a dramatic, cooling effect", 5)
    ],
    "evening": [
        ("partly cloudy with shifting clouds intermittently easing the residual warmth as dusk approaches", 7),
        ("mostly sunny with occasional, fleeting clouds offering brief relief from lingering heat", 7),
        ("a warm evening with a dynamic mix of sun and transient clouds gently cooling the air", 7),
        ("overcast with a gradual increase in cloud cover softly moderating the fading heat", 6),
        ("partly cloudy with ephemeral cloud patches providing intermittent cooling in the afterglow", 7),
        ("mostly sunny with transient clouds offering sporadic relief from persistent warmth", 7),
        ("partly cloudy with gentle modulation of sun and clouds slowly easing the residual heat", 7),
        ("overcast with soft, gradually building cloud cover steadily cooling the lingering day", 6),
        ("a warm evening with modest cloud cover softly cooling the air", 7),
        ("mostly sunny with ephemeral cloud formations briefly easing the afterglow", 7),
        ("partly cloudy with gradual softening of sunlight as intermittent clouds bring cooling relief", 7),
        ("overcast with steady, modest cloud cover gradually diminishing the remaining warmth", 6)
    ],
    "night": [
        ("clear with a refreshing drop in temperature and an almost cloudless, starry sky that cools rapidly", 8),
        ("mostly clear with a delicate scattering of high clouds providing subtle intermittent relief from residual heat", 7),
        ("partly cloudy with intermittent patches of cloud gently moderating lingering warmth to yield a cool night", 7),
        ("overcast with soft, uniform cloud cover significantly cooling the atmosphere as night falls", 6),
        ("clear with an abrupt cooling revealing a sparse scattering of wispy clouds under a starry sky", 8),
        ("mostly cloudy with dynamic cloud cover intermittently breaking up to offer refreshing, cool relief", 7),
        ("partly cloudy with varied shifting clouds intermittently softening the intense coolness", 7),
        ("overcast with continuous gentle cloud cover transforming the night into a cool, subdued scene", 6),
        ("clear with a marked cooling and occasional fleeting clouds subtly enhancing the coolness", 8),
        ("mostly clear with a light, ever-changing cloud pattern softly supporting the cooling night", 7),
        ("partly cloudy with delicate shifting clouds intermittently providing relief from the crisp, cool night", 7),
        ("overcast with persistent soft cloud layer maintaining consistent, refreshing coolness throughout the night", 6)
    ]
}

# Fall weather outcomes – cool with variable precipitation.
fall_weather = {
    "morning": [
        ("mostly clear with a subtle hint of overcast and a crisp, cool air that feels dry", 8),
        ("clear with minimal cloud cover and a refreshing, cool, dry atmosphere that awakens the senses", 9),
        ("partly cloudy with a modest scattering of clouds and a distinct, cool dryness that energizes the morning", 8),
        ("overcast with a gentle cloud layer and a refreshing, dry coolness that softens the early light", 7),
        ("mostly clear with a fleeting overcast subtly enhancing the dry, crisp coolness", 8),
        ("clear with a delicate accumulation of clouds and a bright, invigorating dry coolness", 9),
        ("partly cloudy with intermittent clouds creating a balanced dry cool atmosphere", 8),
        ("overcast with soft, diffused clouds delivering a steady, crisp, dry coolness", 7),
        ("mostly clear with very light cloud presence accentuating refreshing, dry cool clarity", 8),
        ("clear with subtle overcast gently underscoring vivid, dry coolness in the morning", 9),
        ("partly cloudy with a gentle interplay of clouds softly supporting a bright, dry cool air", 8),
        ("overcast with a light, ephemeral cloud cover quietly enhancing a crisp, dry coolness", 7),
        ("partly cloudy with a mix of sun and rain, creating a vibrant, refreshing atmosphere", 7),
        ("overcast with steady rain and a cool, damp breeze", 6)
    ],
    "afternoon": [
        ("clear with a modest rise in cloud cover and pronounced dry coolness pervading the air", 8),
        ("mostly clear with a gentle increase in clouds and noticeably refreshing, dry cool atmosphere", 9),
        ("partly cloudy with emerging clouds offering a defined dry cool feel", 8),
        ("overcast with subtle, persistent clouds reinforcing steady, dry coolness", 7),
        ("clear with a gentle scattering of clouds modestly sustaining a vivid, dry cool environment", 8),
        ("mostly clear with sporadic clouds intermittently boosting distinct dry cool air", 9),
        ("partly cloudy with rhythmic cloud interplay gently supporting refreshing, dry coolness", 8),
        ("overcast with soft, intermittent cloud cover sustaining a defined dry cool ambiance", 7),
        ("clear with a barely perceptible cloud rise accentuating crisp, dry cool atmosphere", 8),
        ("mostly clear with occasional cloud drifts subtly maintaining pronounced dry cool tone", 9),
        ("partly cloudy with a steady cloud pattern reinforcing clear, dry cool atmosphere", 8),
        ("overcast with light, rhythmic cloud cover quietly upholding steady, refreshing dry coolness", 7),
        ("partly cloudy with a mix of sun and rain, creating a vibrant, refreshing atmosphere", 7),
        ("overcast with steady rain and a cool, damp breeze", 6)
    ],
    "evening": [
        ("mostly clear with a gentle overcast and soft, fading dry coolness easing the day", 8),
        ("clear with subtle cloud rise and mild, receding dry coolness softening the twilight", 9),
        ("partly cloudy with transient overcast and delicate, diminishing dry coolness", 8),
        ("overcast with faint, continuous clouds gently moderating residual dry cool air", 7),
        ("partly cloudy with intermittent clouds gradually reducing lingering dry coolness", 8),
        ("clear with soft, ephemeral overcast slowly diminishing residual dry cool feel", 9),
        ("partly cloudy with modest cloud buildup softly alleviating fading dry cool atmosphere", 8),
        ("overcast with steady, gentle clouds quietly tempering evening dry coolness", 7),
        ("mostly clear with delicate sun-cloud interplay gradually easing dry cool air", 8),
        ("clear with gradual cloud emergence softly reducing remaining dry coolness", 9),
        ("partly cloudy with subtle cloud modulation gently lessening dry cool tone", 8),
        ("overcast with measured cloud return quietly tempering lingering dry coolness", 7),
        ("partly cloudy with a mix of sun and rain, creating a vibrant, refreshing atmosphere", 7),
        ("overcast with steady rain and a cool, damp breeze", 6)
    ],
    "night": [
        ("clear with an abrupt cooling revealing a nearly cloudless, starry sky and a strong, biting dry chill", 8),
        ("mostly clear with dynamic, shifting clouds intermittently breaking intense dry cold", 9),
        ("partly cloudy with occasional fleeting clouds gently moderating severe, piercing dry chill", 8),
        ("overcast with a thick, persistent cloud layer taming the intensity of biting dry cold", 7),
        ("clear with noticeable cooling and scattered delicate clouds accentuating profound dry chill", 8),
        ("mostly cloudy with robust, evolving clouds intermittently relieving harsh dry cold", 9),
        ("partly cloudy with a varied mix of transient clouds subtly easing unyielding dry chill", 8),
        ("overcast with dense, enveloping clouds gently diminishing raw, intense dry cold", 7),
        ("clear with marked cooling and occasional delicate clouds enhancing piercing dry chill", 8),
        ("mostly clear with slight, shifting cloud patterns softly supporting deep, biting dry cold", 9),
        ("partly cloudy with dynamic cloud formations intermittently alleviating harsh, sharp dry chill", 8),
        ("overcast with a dense, constant cloud cover quietly tempering overwhelming, burning dry cold", 7),
        ("partly cloudy with a mix of sun and rain, creating a vibrant, refreshing atmosphere", 7),
        ("overcast with steady rain and a cool, damp breeze", 6)
    ]
}

def generate_weather_description(abstract_datetime_str):
    """
    Generates a detailed, singular weather description based on an abstract datetime string.
    The abstract_datetime_str should include keywords indicating the season ("winter", "spring",
    "summer", "fall") and a time-of-day keyword ("morning", "afternoon", "evening", or "night").
    This function selects the corresponding weather outcomes from the appropriate season's dictionary
    using weighted random selection, and returns a random atmospheric description that focuses on cloud cover,
    precipitation, moisture, and overall conditions.
    Returns:
        A weather description string.
    """
    # Determine the season.
    if "winter" in abstract_datetime_str:
        season = "winter"
    elif "spring" in abstract_datetime_str:
        season = "spring"
    elif "summer" in abstract_datetime_str:
        season = "summer"
    elif "fall" in abstract_datetime_str:
        season = "fall"
    else:
        return "unpredictable weather"
    # Determine the time of day.
    if "morning" in abstract_datetime_str:
        tod = "morning"
    elif "afternoon" in abstract_datetime_str:
        tod = "afternoon"
    elif "evening" in abstract_datetime_str or "dusk" in abstract_datetime_str:
        tod = "evening"
    elif "night" in abstract_datetime_str:
        tod = "night"
    else:
        tod = "morning"  # Default to morning if not found.
    # Select the appropriate weather options.
    if season == "winter":
        options = winter_weather[tod]
    elif season == "spring":
        options = spring_weather[tod]
    elif season == "summer":
        options = summer_weather[tod]
    elif season == "fall":
        options = fall_weather[tod]
    else:
        options = [("unpredictable weather", 1)]
    # Use weighted random selection.
    descriptions = [opt[0] for opt in options]
    weights = [opt[1] for opt in options]
    return random.choices(descriptions, weights=weights, k=1)[0]
