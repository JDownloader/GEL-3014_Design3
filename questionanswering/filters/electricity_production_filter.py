from collections import OrderedDict
from questionanswering import bidictionnary
import nltk

def process(question, query_builder):
    mapped_question = next(question)
    if ('electricity' in mapped_question) & ('production' in mapped_question):
        electricity_production_information = extract_electricity_production_information(mapped_question)
        query_builder.with_category_data("electricity - production",   electricity_production_information[0] + " kWh")
        query_builder.with_regex_query(electricity_production_information[1])
    yield mapped_question

def extract_electricity_production_information(mapped_question):
    reverse_dict = bidictionnary.Bidict(mapped_question)
    numbers = reverse_dict.keys_with_value('CD')
    unity = extract_unity(numbers)
    only_numbers = [x for x in numbers if x != unity]
    return (unity, create_regex_with_numbers(only_numbers))

def extract_unity(numbers):
    if ('million' in numbers) :
        return 'million'
    else:
        return 'billion'

def create_regex_with_numbers(range_numbers):
    min_and_max = process_min_and_max_from_two_numbers(range_numbers)
    regex = ''
    for index,digit in enumerate(min_and_max[0]):
        if (index is 0) :
            regex += digit[0]
        else:
            regex += '[' + min_and_max[0][index] + '-' + (min_and_max[1][index] if min_and_max[1][index] is not '0' else '9') + ']'
    regex += '.+&.*'
    return regex

def process_min_and_max_from_two_numbers(range_numbers):
    numbers = [int(number) for number in range_numbers]
    return (str(min(numbers)), str(max(numbers)))