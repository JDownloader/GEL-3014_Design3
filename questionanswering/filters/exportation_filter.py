from questionanswering import bidictionnary
import nltk

def process(question, query_builder):
    mapped_question = next(question)
    if ('export' in mapped_question) :
        if ('partners' in mapped_question):
            partners = extract_importation_information(mapped_question)
            query_builder.with_category_data('Exports - partners', ' '.join(partners))
    yield mapped_question


def extract_importation_information(mappedSentence):
    sentence = mappedSentence.items()
    grammar = "NP: {<NNS>* <NNP>*}"
    result = nltk.RegexpParser(grammar).parse(sentence)

    partners = []
    for subtree in result.subtrees():
        if subtree.label() == 'NP':
            reverse_dict = bidictionnary.Bidict(dict(subtree.leaves()))
            partners += reverse_dict.keys_with_values(['NNP','NNS'])
    if 'partners' in partners:
        partners.remove('partners')
    return partners


