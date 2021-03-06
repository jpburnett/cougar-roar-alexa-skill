# -*- coding: utf-8 -*-
"""Skill to make a cougar roar. (This is for you Dad if you ever see this)"""

import random
import logging
import resources
import math

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ==================================================================================================================================
# Constants and Other Data, Vars, etc...
# ==================================================================================================================================
SKILL_NAME = "Cougar Roar"
TEST_MESSAGE = "THIS IS A TEST"
HELP_MESSAGE = "You can say tell me to roar like a cougar, or, you can say exit... What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "The Cougar skill can't help you with that.  It can roar like a cougar. That's it. What can I help you with?"
FALLBACK_REPROMPT = 'What can I help you with?'
EXCEPTION_MESSAGE = "Sorry. I cannot help you with that."

# =====================================================================
# Helper Functions
# =====================================================================

# Function to grab a random roar
def getRandomRoar(inputList):
    """Gets a random entry from a list"""
    randomRoar = random.choice(list(inputList))
    return inputList[randomRoar]
# =====================================================================
# Handlers
# =====================================================================

# We bout to do some roaring here
class RoarHandler(AbstractRequestHandler):
    """Handler for Skill Launch and Roar Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("RoarIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In RoarHandler")

        roar = getRandomRoar(resources.AUDIO)

        speech = '<audio src=\"' + roar + '"\/>'

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, "Cougar Roar"))
        return handler_input.response_builder.response

# Help handler (AmazonHelpIntent)
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(SimpleCard(
                SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response

# Cancel or Stop Handler (AmazonCancel or AmazonStop Intent)
class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response

class RepeatIntentHandler(AbstractRequestHandler):
    """Handler for Repeat Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In RepeatIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        attr = handler_input.attributes_manager.session_attributes
        handler_input.response_builder.speak(
            attr['speech']).ask(
            attr['reprompt'])
        return handler_input.response_builder.response

# Fallback Handler (AmazonFallbackIntent)
class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.
    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(FALLBACK_MESSAGE).ask(
            FALLBACK_REPROMPT)
        return handler_input.response_builder.response


# Session End Handler (AmazonStopIntent)
class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response

class YesIntentHandler(AbstractRequestHandler):
    """Handler for the YesIntent."""
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        logger.debug("In YesIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]
        session_attr = handler_input.attributes_manager.session_attributes

        #Get what the previous intent was
        prev_intent = session_attr.get("PREV_INTENT")

        if prev_intent == "LaunchIntent":
            speech = data.HELP_MESSAGE
            reprompt = data.FALLBACK_MESSAGE

            handler_input.response_builder.speak(speech) \
            .set_should_end_session(False).ask(reprompt)
            return handler_input.response_builder.response

        if (prev_intent == "RecipeIntent"
            or prev_intent == "RandomItemIntent"
            or prev_intent == "AMAZON.YesIntent"
            or prev_intent == "AMAZON.NoIntent"):
            speech = data.HELP_MESSAGE
            reprompt = data.FALLBACK_MESSAGE

            handler_input.response_builder.speak(speech) \
            .set_should_end_session(False).ask(reprompt)
            return handler_input.response_builder.response

class NoIntentHandler(AbstractRequestHandler):
    """Handler for the NoIntent. Sometimes its okay to say no"""
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        logger.debug("In NoIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]
        
        speech = data.STOP_MESSAGE
        handler_input.response_builder.speak(_(speech))
            .set_should_end_session(True)

        return handler_input.response_builder.response

class LocalizationInterceptor(AbstractRequestInterceptor):
    """Add function to request attributes, that can load locale specific data."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale))
        i18n = gettext.translation(
            'data', localedir='locales', languages=[locale], fallback=True)
        handler_input.attributes_manager.request_attributes["_"] = i18n.gettext

# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)
        return handler_input.response_builder.response

# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))

# Register intent handlers for the skill builder (sb)
sb.add_request_handler(RoarHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(LocalizationInterceptor())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(RepeatIntentHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Uncomment the following lines of code for request, response logs.
# sb.add_global_request_interceptor(RequestLogger())
# sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()