import json
import time
from question_processor import QuestionProcessor
import requests

def fetchQuestion():
    # return ["My telephone lines in use are 1.217 million.","My unemployment rate is 40.6%.","My population is 3,060,631.", "One national symbol of this country is the edelweiss.", "The lotus blossom is the national symbol of this country.",
    #         "The major urban areas of this country are Santiago, Valparaiso and Concepcion.", "The title of my national anthem is Advance Australia Fair.",
    #         "What country has .dz as its internet country code?",  "What country has a latitude of 41.00 S?", "What country has a population growth rate of 1.46%?",
    #         "What country has a total area of 390757 sq km?", "What country has declared its independence on 22 May 1990?", "What country has religions including hindu, muslim, Christian, and sikh?",
    #         "What country has Yaounde as its capital?",  "In 1923, we proclaimed our independence.", "My latitude is 16 00 S and my longitude is 167 00 E.", "My population growth rate is between 1.44% and 1.47%.",
    #        "My national symbol is the elephant.", "My latitude is 16 00 S and my longitude is 167 00 E.", "My internet country code is .br.",  "My independence was declared in August 1971.",
    #         "My death rate is greater than 13 death/1000 and my capital starts with Mos.", "My capital name starts with Moga.", "My capital name starts with Ath and ends with ens.","22 September 1960 is the date of independence of this country." ]


    return  "What country has a birth rate of 46.12 births/ 1000 population?"
ATLAS_WEB_SERVER_URLS = ['https://192.168.0.2', 'https://192.168.1.2', 'https://132.203.14.228']

def main():

#     flag = ''
#     for cycle in xrange(2):
#         question = fetch_question()
#         print question
#         answer = fetch_answer(question)
#         if is_right_answer(answer):
#             # app.base_station.set_question(question, answer)
#             print 'Nicely done!'
#             break
#         else:
#             print 'Oh Oh'
#
# def fetch_answer(question):
#     print "question : " + question
#     processor = QuestionProcessor()
#     processor.answer_question(question)
#     return processor.answer
#
# def is_right_answer(answer):
#     print answer
#     answer_is_good = raw_input('Is this the right answer ? (y/n) : ')
#     strikes = 0
#     if answer_is_good[0] is 'y':
#         return True
#     else:
#         strikes += 1
#         if strikes < 2:
#             return False
#         else :
#             return True
#
# def fetch_question():
#     question = ''
#     for url in ATLAS_WEB_SERVER_URLS:
#         try:
#             response = requests.get(url, verify=False, timeout=0.1)
#             if response.status_code == 200:
#                 question = response.text
#                 break
#         except Exception:
#             pass
#     return json.loads(question)['question']

    question = fetchQuestion()
    start_time = time.time()
    print "question : " + question
    processor = QuestionProcessor()
    processor.answer_question(question)
    print "answer : " + processor.answer
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()