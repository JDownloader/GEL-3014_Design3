from question_processor import QuestionProcessor
import time

def fetchQuestion():
    # return ["My telephone lines in use are 1.217 million.","My unemployment rate is 40.6%.","My population is 3,060,631.", "One national symbol of this country is the edelweiss.", "The lotus blossom is the national symbol of this country.",
    #         "The major urban areas of this country are Santiago, Valparaiso and Concepcion.", "The title of my national anthem is Advance Australia Fair.",
    #         "What country has .dz as its internet country code?",  "What country has a latitude of 41.00 S?", "What country has a population growth rate of 1.46%?",
    #         "What country has a total area of 390757 sq km?", "What country has declared its independence on 22 May 1990?", "What country has religions including hindu, muslim, Christian, and sikh?",
    #         "What country has Yaounde as its capital?",  "In 1923, we proclaimed our independence.", "My latitude is 16 00 S and my longitude is 167 00 E.", "My population growth rate is between 1.44% and 1.47%.",
    #        "My national symbol is the elephant.", "My latitude is 16 00 S and my longitude is 167 00 E.", "My internet country code is .br.",  "My independence was declared in August 1971.",
    #         "My death rate is greater than 13 death/1000 and my capital starts with Mos.", "My capital name starts with Moga.", "My capital name starts with Ath and ends with ens.","22 September 1960 is the date of independence of this country." ]
    return "My national symbol is the elephant."

def main():

    question = fetchQuestion()
    start_time = time.time()
    print "question : " + question
    processor = QuestionProcessor()
    processor.start(question)
    print "answer : " + processor.answer
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()