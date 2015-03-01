from questionanswering import bidictionnary

def process(question, query_builder):
    mappedQuestion = next(question)
    if ('urban' in mappedQuestion) & (('area' in mappedQuestion) | ('areas' in mappedQuestion)):
        urban_areas = extract_urban_areas(mappedQuestion)
        query_builder.with_category_data('major urban areas', ' '.join(urban_areas))
    yield mappedQuestion

def extract_urban_areas(mappedQuestion):
    reverse_dict = bidictionnary.Bidict(mappedQuestion)
    return reverse_dict.keys_with_value('NNP')
