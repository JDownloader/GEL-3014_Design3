from question_processor import QuestionProcessor


def fetchQuestion():
    return "What country has Yaounde as its capital?"

def main():
    question = fetchQuestion()
    print "question : " + question
    processor = QuestionProcessor()
    processor.start(question)

if __name__ == "__main__":
    main()