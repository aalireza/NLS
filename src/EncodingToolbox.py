import NumericalToolbox
import MarkovToolbox

# Data from: https://en.wikipedia.org/wiki/Letter_frequency
FIRST_LETTER_FREQ = {
    "a": 11.62, "b": 4.7, "c": 3.51, "d": 2.67, "e": 2, "f": 3.78, "g": 1.95,
    "h": 7.23, "i": 6.29, "j": 0.597, "k": 0.59, "l": 2.705, "m": 4.383,
    "n": 2.365, "o": 6.264, "p": 2.545, "q": 0.173, "r": 1.653, "s": 7.755,
    "t": 16.671, "u": 1.487, "v": 0.649, "w": 6.753, "x": 0.017, "y": 1.62,
    "z": 0.034
}

FREQNT_WORDS = {
    "a": ["above", "afraid", "against", "agree", "allow", "answer", "apple",
          "arm", "art", "able", "act", "after", "age", "air", "among",
          "anger", "arrange", "atom", "about", "add", "again", "ago",
          "always", "animal", "appear", "area", "arrive", "ask"],
    "b": ["baby", "ball", "bar", "bat", "beat", "been", "begin", "bell",
          "blood", "board", "bone", "bot", "box", "bread", "bring",
          "brother", "build", "buy", "burn", "broad", "break", "boy",
          "bottom", "book", "boat", "blow", "black", "big", "best", "behind",
          "before", "beauty", "base", "band", "back", "bad", "bank", "basic",
          "bear", "bed", "began", "believe", "better", "bird", "block", "body",
          "born"],
    "c": ["call", "car", "carry", "catch", "cell", "chair", "character",
          "check", "child", "claim", "collect", "column", "cool", "corner",
          "cotton", "cow", "cry", "coat", "compare", "cross", "cold", "color",
          "common", "complete", "consider", "cook", "cost", "count", "crowd",
          "cold"],
    "d": ["dad", "dark", "deal", "decide", "develop", "direct", "divide",
          "dollar", "door", "draw", "drink", "dance", "discuss", "drive",
          "danger", "death", "difficult", "dog", "done", "down", "dress"],
    "e": ["each", "earth", "egg", "electric", "equal", "engine", "example",
          "exercise", "experiment", "ear", "edge", "element", "equate",
          "evening", "every", "effect", "energy", "especially", "exact",
          "excite", "experience"],
    "f": ["face", "famous", "father", "feet", "fig", "find", "first", "floor",
          "food", "form", "free", "fruit", "fact", "far", "favor", "fell",
          "fight", "fine", "fish", "flow", "foot", "forward", "fresh", "full",
          "fair", "farm", "fear", "felt", "figure", "finger", "fit", "flower",
          "for", "found", "friend", "fun", "fall", "fast", "feed", "finish",
          "fly", "family", "front"],
    "g": ["game", "general", "glad", "good", "gray", "group", "garden",
          "gentle", "glass", "got", "great", "grow", "gas", "get", "go",
          "green", "guess", "girl", "gold", "grand"],
    "h": ["had", "happy", "he", "heat", "here", "history", "hope", "how",
          "hurry", "hair", "hard", "head", "heavy", "high", "hit", "horse",
          "huge", "half", "has", "hear", "held", "hill", "hot", "human", "hand",
          "hat", "heard", "help", "hundred"],
    "i": ["i", "in", "insect", "iron", "ice", "inch", "instant", "is", "idea",
          "include", "instrument", "island", "if", "indicate", "interest"],
    "j": ["job", "join", "joy", "jump", "just"],
    "k": ["keep", "king", "kept", "key", "knew", "kill", "know", "kind"],
    "l": ["lady", "last", "lead", "left", "letter", "light", "listen", "lone",
          "loud", "lake", "late", "learn", "leg", "level", "like", "little",
          "long", "love", "land", "laugh"],
    "m": ["machine", "make", "market", "matter", "measure", "metal", "milk",
          "miss", "money", "most", "mouth", "must", "made", "man", "mass",
          "may", "meat", "method", "million", "mix", "mix", "month", "mother",
          "move", "magnet", "many", "Meet"],
    "n": ["name", "necessary", "new", "noise", "note", "number", "nation",
          "neck", "next", "noon", "nothing", "numeral", "natual", "need",
          "night", "notice", "nature", "neighbor", "nine", "north", "near",
          "now", "never"],
    "o": ["object", "oil", "only", "order", "out", "observe", "offer", "old",
          "open", "organ", "over", "occur", "office", "operate", "original",
          "own", "ocean", "often", "once", "opposite", "other", "one", "our"],
    "p": ["page", "paper", "paper", "pattern", "phrase", "piece", "planet",
          "point", "print", "process", "proper", "push", "person", "picture",
          "pair", "parent", "party", "people", "picture", "place", "plane",
          "play", "poem", "population", "position", "pound", "pretty",
          "problem", "product"],
    "q": ["question", "quick", "quite"],
    "r": ["race", "rain", "range", "read", "reason", "repeat", "rich", "ring",
          "road", "room", "rose", "radio", "rather", "receive", "reply",
          "region", "record", "remember", "represent", "result", "right",
          "rope", "run"],
    "s": ["safe", "salt", "sat", "say", "science", "seed", "second", "sentence",
          "several", "share", "same", "scale", "score", "season", "self",
          "sense", "settle", "shall", "sharp", "sail", "sand", "saw", "seat",
          "school", "sea", "see", "segment", "sell", "serve", "seven", "shape",
          "she", "show", "sing", "skill", "slave", "slow", "son", "star",
          "story", "subtract", "sudden", "suggest", "sun", "system"],
    "t": ["table", "talk", "temperature", "thin", "third", "though", "tail",
          "teeth", "thought", "tire", "told", "took", "track", "trip", "try",
          "thank", "teach", "there", "thousands", "time", "tool", "trade",
          "tree"],
    "u": ["under", "unit", "up", "usual"],
    "v": ["valley", "village", "value", "vowel", "view", "voice", "visit"],
    "w": ["want", "water", "week", "where", "what", "while", "window",
          "wire", "woman", "wonder", "write", "walk", "war", "wash", "wave",
          "wheel", "wish", "warm", "watch", "weather", "west", "wild", "word"],
    "y": ["yard", "yes", "young", "year", "yellow", "you", "yet"],
    "z": ["zebra"]
}

FILLERS = ["of", "to", "from", "was", "that", "which", "by", "about", "on"]


def limit_freq_threshold(num):
    freq_repo = dict(zip(FIRST_LETTER_FREQ.values(), FIRST_LETTER_FREQ.keys()))
    acceptable_freq = sorted(freq_repo.keys())[::-1][:num]
    acceptable_letters = [freq_repo[freq] for freq in acceptable_freq]
    return acceptable_letters


def first_letter_based_freq_rename(number, letters):
    # The base of the number must match the number of the provided letters.
    # Requires number in letter formatting
    renamed = ''.join(
        [letters[NumericalToolbox.letter_to_decimal(letter_digit)]
         for letter_digit in list(number)])
    return renamed


def revert_renamed_number(renamed, letters):
    number = ''.join(
        [NumericalToolbox.decimal_to_letter(letters.index(letter_digit))
         for letter_digit in renamed])
    return number


def encode(ciphertext, text_model, threshold=10):
    # Implement Grep
    freq_limit = limit_freq_threshold(threshold)
    renamed_ciphertext = first_letter_based_freq_rename(ciphertext, freq_limit)
    text = MarkovToolbox.generate_text_based_on_letter_list(renamed_ciphertext,
                                                            text_model)
    print text
