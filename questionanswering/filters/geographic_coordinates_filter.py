from questionanswering import bidictionnary
import nltk

def process(question, query_builder):
    mappedQuestion = next(question)
    if ('latitude' in mappedQuestion) | ('longitude' in mappedQuestion):
        geographic_coordinates = extract_geographic_coordinates(mappedQuestion)
        query_builder.with_category_data('geographic coordinates', ' '.join(geographic_coordinates))
    yield mappedQuestion

def extract_geographic_coordinates(mappedQuestion):
    sentence =  mappedQuestion.items()
    grammar = "NP: {<CD>*?<NNP>}"
    result = nltk.RegexpParser(grammar).parse(sentence)

    coordinates = []
    for subtree in result.subtrees():
        if subtree.label() == 'NP':
            reverse_dict = bidictionnary.Bidict(dict(subtree.leaves()))
            coordinates += reverse_dict.keys_with_values(['CD', 'NNP'])

    coordinates = [item.replace(".", " ").replace(",", " ") for item in coordinates]
    return coordinates
