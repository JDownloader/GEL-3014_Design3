from questionanswering import bidictionnary
import nltk

def process(question, query_builder):
    mapped_question = next(question)
    if ('illicit' in mapped_question) and (('drug' in mapped_question)|('drugs' in mapped_question)):
        illicit_drugs_statement = extract_illicit_drugs_statement(mapped_question)
        query_builder.with_category_data('illicit drugs', ' '.join(illicit_drugs_statement))
    yield mapped_question

def extract_illicit_drugs_statement(mapped_question):
    sentence = mapped_question.items()
    grammar = "NP: {<DT>*}"
    result = nltk.RegexpParser(grammar).parse(sentence)

    key_word = ''
    for subtree in result.subtrees():
        if subtree.label() == 'NP':
            reverse_dict = bidictionnary.Bidict(dict(subtree.leaves()))
            key_word = reverse_dict.key_with_value('DT')

    return truncate_sentence_from_key_word(key_word, mapped_question)

def truncate_sentence_from_key_word(key_word, sentence):

    statement = sentence.items()[sentence.keys().index(key_word):len(sentence.items())]
    statement_map = [key for key,value in statement]
    return statement_map

