from nltk.tokenize import sent_tokenize as split_sentences
import cPickle as pickle
import markovify
import os


def make_text_model(text_file_abs_path):
    with open(text_file_abs_path, "r") as f:
        text = f.read()
    text_model = markovify.Text(text)
    return text_model


def save_text_model(text_model, model_dump_abs_path):
    if not os.path.exists(model_dump_abs_path):
        with open(model_dump_abs_path, "wb") as f:
            pickle.dump(text_model, f, protocol=2)
    if os.path.exists(model_dump_abs_path):
        return model_dump_abs_path
    return None


def load_text_model(model_pickle_abs_path):
    if os.path.exists(model_pickle_abs_path):
        with open(model_pickle_abs_path, "rb") as f:
            text_model = pickle.load(f)
            return text_model
    return None


def make_sentence_starting_with_letter(letter, text_model):
    while True:
        sentence = text_model.make_sentence()
        if sentence[0] in [letter.lower(), letter.upper()]:
            return sentence


def generate_text_based_on_letter_list(letters, text_model):
    text = ' '.join([make_sentence_starting_with_letter(letter, text_model)
                     for letter in letters])
    return text


def derive_first_letter_of_every_sentence(text):
    sentences = split_sentences(text)
    letters = [sentence[0].lower() for sentence in sentences]
    return letters
