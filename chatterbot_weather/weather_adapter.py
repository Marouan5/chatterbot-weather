# -*- coding: utf-8 -*-
import re
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
import forecastio


class WeatherLogicAdapter(LogicAdapter):
    """
    A logic adapter that returns information regarding the weather and
    the forecast for a specific location. Currently, only basic information
    is returned, but additional features are planned in the future.
    """

    def __init__(self, **kwargs):
        super(WeatherLogicAdapter, self).__init__(**kwargs)

        self.forecastio_api_key = kwargs.get('forecastio_api_key')

    def process(self, statement):
        """
        Returns the forecast for a location (using latitude and longitude).
        """
        user_input = statement.text.lower()

        if 'weather' not in user_input:
            return 0, Statement('')

        latitude = self.get_latitude(user_input)
        longitude = self.get_longitude(user_input)

        if latitude is not '' and longitude is not '':
            # @TODO: Add more options for getting weather. This could include
            # the current temperature, the current cloud cover, etc. This
            # might require removing the forecastio library (which is
            # probably a good idea).
            return 1, Statement(
                'The forecast for tomorrow is: ' + self.get_weather(latitude, longitude)
            )

        return 0, Statement('')

    def get_latitude(self, user_input):
        """
        Returns the latitude extracted from the input.
        """
        from nltk import tokenize

        for token in tokenize.word_tokenize(user_input):
            if 'latitude=' in token:
                return re.sub('latitude=', '', token)

        return ''

    def get_longitude(self, user_input):
        """
        Returns the longitude extracted from the input.
        """
        from nltk import tokenize

        for token in tokenize(user_input):
            if 'longitude=' in token:
                return re.sub('longitude=', '', token)

        return ''

    def get_weather(self, latitude, longitude):
        """
        Returns the weather for a given latitude and longitude.
        """
        # @TODO: Find some way to suppress the warnings generated by this.
        forecast = forecastio.load_forecast(self.forecastio_api_key, latitude, longitude)

        return forecast.hourly().summary
