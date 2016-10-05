"""
 Copyright 2016 Alireza Rafiei

 Licensed under the Apache License, Version 2.0 (the "License"); you may
 not use this file except in compliance with the License. You may obtain
 a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

# Below are the frequency of the letters at the start of a word in English.
# Data from: https://en.wikipedia.org/wiki/Letter_frequency
FIRST_LETTER_WORD_FREQ = {
    "a": 11.62, "b": 4.7, "c": 3.51, "d": 2.67, "e": 2, "f": 3.78, "g": 1.95,
    "h": 7.23, "i": 6.29, "j": 0.597, "k": 0.59, "l": 2.705, "m": 4.383,
    "n": 2.365, "o": 6.264, "p": 2.545, "q": 0.173, "r": 1.653, "s": 7.755,
    "t": 16.671, "u": 1.487, "v": 0.649, "w": 6.753, "x": 0.017, "y": 1.62,
    "z": 0.034
}

# Below are the order of the words that start an English sentence.
# https://glossarch.wordpress.com/2014/01/14/the-most-common-letter-to-start-a-sentence-with-in-english/
# It's at the form of a dictionary to match the structures between
# `first_letter_freq` and `first_letter_word_freq`. These two would be used in
# EncodingToolbox.
# For the dict below, keys are letters and values are occurrences in brown
# corpus.
FIRST_LETTER_FREQ = {"t": 11928, "i": 7006, "a": 4830, "h": 4653, "s": 3225,
                     "w": 3100, "b": 2412, "m": 1836, "o": 1735, "f": 1462,
                     "n": 1314, "p": 1034, "c": 981, "d": 941,
                     "e": 868, "y": 859, "l": 713, "r": 666, "g": 517, "j": 354,
                     "u": 299, "v": 143, "k": 143, "q": 41, "z": 10, "x": 2}


# The word below would be randomly chosen to be at the start of the init state
# of the markovify text model in order to start a sentence.
# Data from:
# https://www.usingenglish.com/resources/wordcheck/list-common+words.html
FREQUENT_WORDS = {
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
