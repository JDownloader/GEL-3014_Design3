from questionanswering import bidictionnary

def process(question, query_builder):
    mapped_question = next(question)
    if ('telephone' in mapped_question) & ('lines' in mapped_question):
        telephones_lines = extract_total(mapped_question)
        query_builder.with_category_data('Telephones', telephones_lines)
    yield mapped_question

def extract_total(mapped_question):
    reverse_dict = bidictionnary.Bidict(mapped_question)
    return ' '.join(reverse_dict.keys_with_value('CD'))
