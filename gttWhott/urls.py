from django.urls import path
from .views import Gtt_Whott_Game,Start_Gtt_Card_Game,Gtt_Whott_Game_Room,Collect_Card,Game_General_Market,Count_Cards,Power_Cards,Gtt_Whot_Game_Reload,Update_Game_Reload,End_Game,Finish_Game,Gtt_Whot_Member_Special_Service


urlpatterns = [
    path("gttWhott",Gtt_Whott_Game.as_view(),name="gttWhott_page"),
    path("startGame/gttWhot/<str:amount>",Start_Gtt_Card_Game.as_view(),name="gttWhot_start_game_page"),
    path("gttWhot/gameRoom",Gtt_Whott_Game_Room.as_view(),name="gttWhot_game_room_page"),
    path("gttWhot/collectCard/<str:id>/<str:card_shape>/<str:card_number>",Collect_Card.as_view(),name="collect_card_page"),
    path("gttWhot/generalMarket",Game_General_Market.as_view(),name="gttWhot_general_market_page"),
    path("gttWhot/countCards",Count_Cards.as_view(),name="count_cards_page"),
    path("gttWHot/powerCards/<str:id>/<str:card_shape>/<str:card_number>",Power_Cards.as_view(),name="power_cards_page"),
    path("gttWhot/check/gameReload",Gtt_Whot_Game_Reload.as_view(),name="gttWhott_game_repload_page"),
    path("gttWhot/update/gameReload",Update_Game_Reload.as_view(),name="update_gttWhot_game_reload_page"),
    path("gttWhot/endGame",End_Game.as_view(),name="end_game_page"),
    path("gttWhot/finishGame",Finish_Game.as_view(),name="finish_game_page"),
    path("gttWhot/specialService",Gtt_Whot_Member_Special_Service.as_view(),name="gtt_whot_member_special_service"),
]
