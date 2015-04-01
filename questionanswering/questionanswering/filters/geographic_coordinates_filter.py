from questionanswering import bidictionnary
import nltk

def process(question, query_builder):
    mapped_question = next(question)
    if ('latitude' in mapped_question) | ('longitude' in mapped_question):
        geographic_coordinates = extract_geographic_coordinates(mapped_question)
        query_builder.with_category_data('geographic coordinates', ' '.join(geographic_coordinates))
    yield mapped_question

def extract_geographic_coordinates(mapped_question):
    sentence = mapped_question.items()
    grammar = "NP: {<CD>*?<NNP>}"
    result = nltk.RegexpParser(grammar).parse(sentence)

    coordinates = []
    for subtree in result.subtrees():
        if subtree.label() == 'NP':
            reverse_dict = bidictionnary.Bidict(dict(subtree.leaves()))
            coordinates += reverse_dict.keys_with_values(['CD', 'NNP'])

    coordinates = [item.replace(".", " ").replace(",", " ") for item in coordinates]
    return coordinates
