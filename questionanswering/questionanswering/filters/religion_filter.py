from questionanswering import bidictionnary
import nltk


def process(question, query_builder):
    mappedSentence = next(question)
    if ('religions' in mappedSentence) | ('religion' in mappedSentence):
        religions = extract_religions(mappedSentence)
        query_builder.with_category_data('religions', ' '.join(religions))
    yield mappedSentence

def extract_religions(mappedSentence):
    sentence =  mappedSentence.items()
    grammar = "NP: {<NN>|<NNP>}"
    parser = nltk.RegexpParser(grammar)
    result = parser.parse(sentence)

    religions = []
    for subtree in result.subtrees():
        if subtree.label() == 'NP':
            target_tree = dict(subtree.leaves())
            if 'country' in target_tree:
                del target_tree['country']
            reverse_dict = bidictionnary.Bidict(target_tree)
            religions += (reverse_dict.keys_with_values(['NN', 'NNP']))
    return religions


