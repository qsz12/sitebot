from loguru import logger
import re

from datetime import datetime as dt
from random import choice

from thefuzz.fuzz import token_set_ratio as ratio

from constants.responses import CONST_RESPONSES_MAP
from constants.config import Constants


CONSTANTS = Constants()


class UserMessage:
    def __init__(self, user_query: str):
        self.user_query: str = user_query
        self.post_process_sequence: list = []
        self.possible_responses: str = []
        self.raw_response: str = ""
        self.raw_response_score: float = 0.0
        self.raw_response_entities = []
        self.processed_response: str = ""

        self.run()

    def handle_time(self):
        """adds a time value in HH:MM to input string,/
        which has to be formattable

        Args:
            resp_str (str): response to an FAQ usually

        Returns:
            str: same as resp_str but with current time
        """
        current_time = dt.now()
        timevars: dict = {
            "hh_mm": current_time.strftime("%H:%M"),
            "day": current_time.strftime("%A"),
            "dd": current_time.day,
            "mm": current_time.month,
            "yyyy": current_time.year,
        }
        logger.info(self.raw_response_entities)
        response_map = {
            i: timevars.get(i) for i in self.raw_response_entities
        }
        if None in response_map.values():
            logger.exception("time values error, state is: {}".format(str(timevars)))
        else:
            logger.info(response_map)
            self.processed_response = self.raw_response.format(**response_map)

    def handle_weather(self):
        weather_component: str = ""
        logger.warning(
            "weather component not implemented yet: {}".format(weather_component)
        )
        self.processed_response = "I don't know how to answer that yet."

    def fetch_response_entities(self):
        match_list = []
        try:
            match_list = [i[1:-1] for i in re.findall(r"\{.*?\}", self.raw_response)]
        except Exception as exc:
            logger.exception("Could not process entities: {}".format(str(exc)))
        self.raw_response_entities = match_list

    def select_answer(self):
        try:
            user_query: str = self.user_query
            logger.info(user_query)
            if CONST_RESPONSES_MAP.get(user_query):
                possible_response_matches = [(CONST_RESPONSES_MAP.get(user_query), 100)]
            else:
                possible_response_matches = []
                for possible_match in CONST_RESPONSES_MAP:
                    match_ratio = ratio(user_query, possible_match)
                    if match_ratio >= CONSTANTS.query_fuzzy_match_threshold:
                        possible_response_matches.append((possible_match, match_ratio))
            if len(possible_response_matches):
                logger.info(possible_response_matches)
                possible_response_matches.sort(key=lambda x: x[1], reverse=True)
                final_response = CONST_RESPONSES_MAP[possible_response_matches[0][0]]
            else:
                final_response = CONST_RESPONSES_MAP.get("ERR_SYS_BOT_DETECT_FAIL", {})
        except Exception as exc:
            logger.exception("Error detecting response: {}".format(str(exc)))
            final_response = "Sorry, something seems to have gone wrong"
            logger.info(final_response)
        self.post_process_sequence = final_response.get("postProcessSequence", [])
        self.possible_responses = possible_response_matches
        response_options_list = final_response.get("validResponses", [])
        self.raw_response = choice(response_options_list)

    def run(self):
        self.select_answer()
        self.fetch_response_entities()
        if len(self.post_process_sequence):
            for func in self.post_process_sequence:
                getattr(self, func)()
        else:
            self.processed_response = self.raw_response

    def __str__(self):
        return self.processed_response
