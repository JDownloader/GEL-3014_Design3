from collections import OrderedDict
from questionanswering import bidictionnary
import nltk

def process(question, query_builder):
    mapped_question = next(question)
    if ('electricity' in mapped_question) & ('production' in mapped_question):
        electricity_production_regex = extract_electricity_production_regex(mapped_question)
        query_builder.with_category_data("electricity - production",  "billion kWh")
        query_builder.with_regex_query(electricity_production_regex[1])
    yield mapped_question

def extract_electricity_production_regex(mapped_question):
    reverse_dict = bidictionnary.Bidict(mapped_question)
    numbers = reverse_dict.keys_with_value('CD')
    unity = extract_unity(numbers)
    only_numbers = [x for x in numbers if x != unity]
    return create_regex_with_numbers(only_numbers)

def extract_unity(numbers):
    if ('million' in numbers) :
        return 'million'
    else:
        return 'billion'

def create_regex_with_numbers(range_numbers):
    numbers = [int(number) for number in range_numbers]
    minimum_number = min(numbers)
    maximum_number = max(numbers)
    # for digit in str(maximum_number):
    return(str(maximum_number)[0], "6[0-5][0-9].+&.*")

