from questionanswering import bidictionnary

def process(question, query_builder):
    mappedQuestion = next(question)
    if ('national' in mappedQuestion) & ('anthem' in mappedQuestion) :
        national_anthem = extract_national_anthem(mappedQuestion)
        if ('by' in mappedQuestion) :
            query_builder.with_category_data('national anthem', (' '.join(national_anthem)))
        else:
           query_builder.with_category_data('national anthem', ( '\"' + ' '.join(national_anthem) + '\"'))
    yield mappedQuestion

def extract_national_anthem(mappedQuestion):
    reverse_dict = bidictionnary.Bidict(mappedQuestion)
    return reverse_dict.keys_with_value('NNP')
