from django.urls import path
from game.views import Game,Start_Game,Check_Start_Game,Continue_Game,Game_Room,Sender_Numbers_Collation,First_Number,Second_Number,Third_Number,Fourth_Number,Fifth_Number,Sixth_Number,Next_Round,Check_Game_Reload,Update_Game_Reload,Finish_Round,End_Game,Opponent_Delay_Report


urlpatterns = [
    path("game",Game.as_view(),name="game_page"),
    path("start/game/<str:amount>",Start_Game.as_view(),name="start_game_page"),
    path("check/game",Check_Start_Game.as_view(),name="check_start_game_page"),
    path("continue/game",Continue_Game.as_view(),name="continue_game_page"),
    path("gameRoom/<str:user>/vs/<str:opponent>",Game_Room.as_view(),name="game_room_page"),
    path("senderNumbersCollation",Sender_Numbers_Collation.as_view(),name="game_number_page"),
    path("receiverFirstNumber",First_Number.as_view(),name="receiver_first_number_page"),
    path("receiverSecondNumber",Second_Number.as_view(),name="receiver_second_number_page"),
    path("receiverThirdNumber",Third_Number.as_view(),name="receiver_third_number_page"),
    path("receiverFourthNumber",Fourth_Number.as_view(),name="receiver_fourth_number_page"),
    path("receiverFifthNumber",Fifth_Number.as_view(),name="receiver_fifth_number_page"),
    path("receiverSixthNumber",Sixth_Number.as_view(),name="receiver_sixth_number_page"),
    path("nextRound",Next_Round.as_view(),name="next_round_page"),
    path("checkGameReload",Check_Game_Reload.as_view(),name="check_game_reload_page"),
    path("updateGameReload",Update_Game_Reload.as_view(),name="update_game_reload_page"),
    path("finishRound",Finish_Round.as_view(),name="finish_round_page"),
    path("endGame",End_Game.as_view(),name="end_game_page"),
    path("opponentDelayReport",Opponent_Delay_Report.as_view(),name="opponent_delay_page")
]