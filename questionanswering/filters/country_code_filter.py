from questionanswering import bidictionnary

def process(question, query_builder):
    mappedQuestion = next(question)
    if ('internet' in mappedQuestion) & ('country' in mappedQuestion) & ('code' in mappedQuestion):
        country_code = extract_country_code(mappedQuestion)
        query_builder.with_category_data('country code', country_code)
    yield mappedQuestion

def extract_country_code(mappedQuestion):
    reverse_dict = bidictionnary.Bidict(mappedQuestion)
    return reverse_dict.key_with_value('JJ')