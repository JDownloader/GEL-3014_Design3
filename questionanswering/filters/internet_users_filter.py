from questionanswering import bidictionnary

def process(question, query_builder):
    mapped_question = next(question)
    if ('internet' in mapped_question) & ('users' in mapped_question):
        internet_users = extract_total(mapped_question)
        query_builder.with_nested_query('internet users', internet_users)
    yield mapped_question

def extract_total(mapped_question):
    reverse_dict = bidictionnary.Bidict(mapped_question)
    if 'million' in reverse_dict:
        reverse_dict.pop('million')
    return ' '.join(reverse_dict.keys_with_value('CD'))
