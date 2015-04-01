from questionanswering import bidictionnary
import nltk

def process(question, query_builder):
    mapped_question = next(question)
    if ('languages' in mapped_question) | ('language' in mapped_question):
        languages = extract_languages(mapped_question)
        query_builder.with_category_data('languages', ' '.join(languages))
    yield mapped_question

def extract_languages(mapped_question):
    sentence =  mapped_question.items()
    grammar = "NP: {<NN>|<NNP>}"
    result = nltk.RegexpParser(grammar).parse(sentence)

    languages = []
    for subtree in result.subtrees():
        if subtree.label() == 'NP':
            target_tree = dict(subtree.leaves())
            reverse_dict = bidictionnary.Bidict(target_tree)
            languages += (reverse_dict.keys_with_values(['NN', 'NNP']))
    return languages
