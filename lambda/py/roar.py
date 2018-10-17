# -*- coding: utf-8 -*-
"""Skill to make a cougar roar. (This is for you Dad if you ever see this)"""

import random
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response


# ==================================================================================================================================
# Constants and Other Data, Vars, etc...
# ==================================================================================================================================
SKILL_NAME = "Cougar Roar"
HELP_MESSAGE = "You can say tell me to roar like a cougar, or, you can say exit... What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "The Cougar skill can't help you with that.  It can roar like a cougar. That's it. What can I help you with?"
FALLBACK_REPROMPT = 'What can I help you with?'
EXCEPTION_MESSAGE = "Sorry. I cannot help you with that."