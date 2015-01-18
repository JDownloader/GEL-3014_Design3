from hello import Hello
from webserver import WebServer


def main():
    hey = Hello()
    hey.say_hello()
    ws = WebServer()
    ws.start_server()

if __name__ == "__main__":
    main()