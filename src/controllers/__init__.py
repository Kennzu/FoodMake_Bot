from .common import register_common_handlers
from .registration import register_registration_handlers
from .couples import register_couple_handlers
from .breakfasts import register_breakfast_handler
from .lanch import register_lanch_handlers
from .dinner import register_dinner_handlers
from .add_food import register_add_food_handlers
from .request_cookie import register_request_cookie_handlers

def register_handlers(dp):
    register_common_handlers(dp) # start + view_id
    register_registration_handlers(dp) # registratiom
    register_couple_handlers(dp) # all with couple
    register_breakfast_handler(dp) # all with breakfast
    register_lanch_handlers(dp) # all with lanch
    register_dinner_handlers(dp) # all with dinner
    register_add_food_handlers(dp) # all with adding food
    register_request_cookie_handlers(dp) # all with requests cookie

    