# from nltk.tokenize import sent_tokenize as split_sentences
import EncodingToolbox
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
    sentence = None
    while True:
        try:
            sentence = text_model.make_sentence_with_start(
                EncodingToolbox.produce_random_freq_filler(letter))
        except KeyError:
            pass
        if sentence is not None:
            if sentence.count('.') == 1:
                break
    return sentence

# while True:
    #     sentence = text_model.make_sentence()
    #     if sentence[0] in [letter.lower(), letter.upper()]:
    #         return sentence


def generate_text_based_on_letter_list(letters, text_model):
    text_list = []
    for i, letter in enumerate(letters):
        text_list.append(make_sentence_starting_with_letter(letter, text_model))
        print "sentence number {} found. Need {} more.".format(
            i + 1, len(letters) - i - 1)
    text = ' '.join(text_list)
    # text = ' '.join([make_sentence_starting_with_letter(letter, text_model)
    #                  for letter in letters])
    return text


def derive_first_letter_of_every_sentence(text):
    # sentences = split_sentences(text.decode('utf-8'))
    # To remove examples of P.A.
    # filtered_text = []
    # i = 0
    # while i < len(text) - 1:
    #     if text[i] == ".":
    #         if text[i + 1] != " ":
    #             pass
    #     filtered_text.append(text[i])
    #     i += 1
    # # To remove '.' singletons
    # extra_filtered_text = []
    # i = 1
    # while i < len(filtered_text):
    #     if filtered_text[i] == ".":
    #         if filtered_text[i + 1] == " " and filtered_text[i - 1] == " ":
    #             pass
    #     extra_filtered_text.append(filtered_text[i])
    #     i += 1
    #
    # text = ''.join(extra_filtered_text)

    sentences = [text[0]] + [text[j]
                             for j in xrange(2, len(text))
                             if text[j - 2] == '.' and text[j - 1] == ' ']
    # sentences = split_sentences(text)
    # sentences = filter(lambda x: len(x) > 7, text.split('. '))
    letters = [sentence[0].lower() for sentence in sentences]
    return letters
