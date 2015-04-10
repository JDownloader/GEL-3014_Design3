from questionanswering import bidictionnary
import nltk

def process(question, query_builder):
    mapped_question = next(question)
    if 'industries' in mapped_question:
        industries = extract_industries(mapped_question)
        query_builder.with_nested_query('industries', ' '.join(industries))
    yield mapped_question


def extract_industries(mappedSentence):
    sentence =  mappedSentence.items()
    grammar = "NP: {<NN>*<JJ>*}"
    result = nltk.RegexpParser(grammar).parse(sentence)

    industries = []
    for subtree in result.subtrees():
        if subtree.label() == 'NP':
            reverse_dict = bidictionnary.Bidict(dict(subtree.leaves()))
            industries = reverse_dict.keys_with_values(['JJ','NN'])
    return industries
