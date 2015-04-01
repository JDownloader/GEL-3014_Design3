from questionanswering import bidictionnary

def process(question, query_builder):
    mapped_question = next(question)
    if 'capital' in mapped_question:
        capital_name = extract_capital_name(mapped_question)
        query_builder.with_category_data('capital', capital_name)
    yield mapped_question


def extract_capital_name(mappedSentence):
    reverse_dict = bidictionnary.Bidict(mappedSentence)

    if ("starts" in mappedSentence) & ("with" in mappedSentence) & ("ends" in mappedSentence):
        return reverse_dict.key_with_value('NNP') + reverse_dict.key_with_value('NNS')

    elif ("starts" in mappedSentence) & ("with" in mappedSentence):
        return reverse_dict.key_with_value('NNP') + "*"
    else:
        return reverse_dict.key_with_value('NNP')
