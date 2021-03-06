from push_weather.info import info
from push_weather.Crawling_Weather import crawling_weather
from push_weather.Send_Message import send_message

if __name__ == '__main__':
    send_message(crawling_weather(info))