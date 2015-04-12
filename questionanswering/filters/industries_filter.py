from questionanswering import bidictionnary
import nltk

def process(question, query_builder):
    mapped_question = next(question)
    if 'industries' in mapped_question:
        industries = extract_industries(mapped_question)
        query_builder.with_nested_query('industries', ' '.join(industries))
    yield mapped_question


def extract_industries(mapped_question):
    sentence =  mapped_question.items()
    grammar = "NP: {<VBG>|<VBP>*}"
    result = nltk.RegexpParser(grammar).parse(sentence)

    key_word = ''
    for subtree in result.subtrees():
        if subtree.label() == 'NP':
            reverse_dict = bidictionnary.Bidict(dict(subtree.leaves()))
            key_word = reverse_dict.key_with_value('VBG')
            if key_word is None:
                key_word = reverse_dict.key_with_value('VBP')
    return truncate_sentence_from_key_word(key_word, mapped_question)


def truncate_sentence_from_key_word(key_word, sentence):
    statement = sentence.items()[sentence.keys().index(key_word):len(sentence.items())]
    statement_map = [key for key,value in statement]
    return statement_map