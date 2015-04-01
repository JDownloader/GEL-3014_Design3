from questionanswering import bidictionnary

def process(question, query_builder):
    mapped_question = next(question)
    if ('public' in mapped_question) and ('debt' in mapped_question):
        public_dept = extract_public_dept(mapped_question)
        query_builder.with_category_data('public dept', (public_dept + '%'))
    yield mapped_question

def extract_public_dept(mapped_question):
    reverse_dict = bidictionnary.Bidict(mapped_question)
    print reverse_dict
    return reverse_dict.key_with_value('CD')
