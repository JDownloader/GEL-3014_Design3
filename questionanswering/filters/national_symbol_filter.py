from questionanswering import bidictionnary
import nltk


def process(question, query_builder):
    mapped_question = next(question)
    if ('national' in mapped_question) & ('symbol' in mapped_question):
        national_symbols = extract_national_symbol(mapped_question)
        query_builder.with_category_data('national symbol', ' '.join(national_symbols))
    yield mapped_question


def extract_national_symbol(mappedSentence):
    sentence =  mappedSentence.items()
    grammar = "NP: {<DT> <NN>*<NN>}"
    parser = nltk.RegexpParser(grammar)
    result = parser.parse(sentence)

    for subtree in result.subtrees():
        if subtree.label() == 'NP':
            target_tree = dict(subtree.leaves())
            if ('The' in target_tree) | ('the' in target_tree):
                reverse_dict = bidictionnary.Bidict(target_tree)
                return reverse_dict.keys_with_value('NN')