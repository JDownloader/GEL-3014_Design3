from questionanswering import bidictionnary
import nltk

def process(question, query_builder):
    mapped_question = next(question)
    if 'climate' in mapped_question:
        climate = extract_climate(mapped_question)
        query_builder.with_nested_query('climate', ' '.join(climate))
    yield mapped_question


def extract_climate(mappedSentence):
    sentence =  mappedSentence.items()
    grammar = "NP: {<JJ> <NN>}"
    result = nltk.RegexpParser(grammar).parse(sentence)

    languages = []
    for subtree in result.subtrees():
        if subtree.label() == 'NP':
            reverse_dict = bidictionnary.Bidict(dict(subtree.leaves()))
            languages = reverse_dict.keys_with_value('JJ')
    return languages