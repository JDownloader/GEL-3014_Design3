from questionanswering import bidictionnary

def process(question, query_builder):
    mapped_question = next(question)
    if 'independence' in mapped_question:
        independence_date_parts = extract_independence_date_parts(mapped_question)
        query_builder.with_independence_date(independence_date_parts)
    yield mapped_question

def extract_independence_date_parts(mappedSentence):
    reverse_dict = bidictionnary.Bidict(mappedSentence)
    return reverse_dict.keys_with_values(['CD', 'NNP'])
