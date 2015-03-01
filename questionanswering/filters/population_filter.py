from questionanswering import bidictionnary
import  nltk

def process(question, query_builder):
    mapped_question = next(question)
    if ('population' in mapped_question) & ('growth' not in mapped_question):
        population = extract_population(mapped_question)
        query_builder.with_category_data('population', population)
    yield mapped_question

def extract_population(mapped_question):
    reverse_dict = bidictionnary.Bidict(mapped_question)
    number = reverse_dict.keys_with_value('CD')

    if len(number) > 1:
        return extract_population_from_spaced_number(mapped_question)
    elif "," in number[0]:
        return ' '.join(number)
    else:
        return format(int(' '.join(number)), ",d")

def extract_population_from_spaced_number(mapped_question):
    sentence =  mapped_question.items()
    grammar = "NP: {<CD>*<CD>}"
    parser = nltk.RegexpParser(grammar)
    result = parser.parse(sentence)

    numbers = []
    for subtree in result.subtrees():
        if subtree.label() == 'NP':
            numbers = [key for key in dict(subtree.leaves())]

    return ','.join(numbers)