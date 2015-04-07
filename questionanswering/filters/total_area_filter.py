from questionanswering import bidictionnary

def process(question, query_builder):
    mapped_question = next(question)
    if ('total' in mapped_question) & ('area' in mapped_question):
        total_area = extract_total_area(mapped_question)
        query_builder.with_category_data('area', 'total ' + total_area)
    yield mapped_question

def extract_total_area(mapped_question):
    reverse_dict = bidictionnary.Bidict(mapped_question)
    total_area = reverse_dict.key_with_value('CD')
    return format(int(total_area), ",d")
