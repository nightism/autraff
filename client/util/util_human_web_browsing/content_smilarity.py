from nltk import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet as wn


def pps_tag_to_wn_tag(tag):
    if tag is None:
        return None

    if tag.startswith('N'):
        return 'n'

    if tag.startswith('V'):
        return 'v'

    if tag.startswith('J'):
        return 'a'

    if tag.startswith('R'):
        return 'r'

    return None


def word_tag_to_synset(word, tag):
    wn_tag = pps_tag_to_wn_tag(tag)
    # print(wn_tag)
    if wn_tag is None:
        return None

    try:
        # take the most common synset
        # print(wn.synsets(word, wn_tag)[0])
        return wn.synsets(word, wn_tag)[0]
    except Exception as e:
        return None


def preprocess(sen_one, sen_two):
    """
    compute the similarity between two contents using Wordnet
    """

    # Tokenize
    sen_one = word_tokenize(sen_one)
    sen_two = word_tokenize(sen_two)

    # Tag
    sen_one = pos_tag(sen_one)
    sen_two = pos_tag(sen_two)

    # Get synsets for each tagged word
    def map_tags_to_synsets(word_tag_pair):
        return word_tag_to_synset(word_tag_pair[0], word_tag_pair[1])
    synsets_one = list(map(map_tags_to_synsets, sen_one))
    synsets_two = list(map(map_tags_to_synsets, sen_two))
    # print(synsets_one)
    # print(synsets_two)

    # Eliminate None objects
    synsets_one = [synset for synset in synsets_one if synset]
    synsets_two = [synset for synset in synsets_two if synset]

    return synsets_one, synsets_two


def content_similarity_from_synsets(synsets_one, synsets_two):

    total_score = 0.0
    word_count = 0

    for synset in synsets_one:
        # Calculate similarity score of the most similar word
        all_scores = list(map(synset.path_similarity, synsets_two))
        all_scores = list(filter(lambda x: x is not None, all_scores))
        # print(synset)
        # print(all_scores)
        if all_scores:
            score = max(all_scores)
            total_score += score
            word_count += 1

    if word_count == 0:
        return 0
    else:
        return total_score / word_count


def calculate_content_similarity(sen1, sen2):
    synsets_one, synsets_two = preprocess(sen1, sen2)
    similarity_one = content_similarity_from_synsets(synsets_one, synsets_two)
    similarity_two = content_similarity_from_synsets(synsets_two, synsets_one)

    return (similarity_one + similarity_two) / 2.0


if __name__ == '__main__':
    sen1 = input()
    sen2 = input()
    print(calculate_content_similarity(sen1, sen2))
