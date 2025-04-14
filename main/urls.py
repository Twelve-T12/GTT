from django.urls import path
from .views import Home,Profile,Settings,Search_Player,About,Register,Terms_Conditions,Ajax_Check_Member_Gtt_Whot_Shuffle_Cards_In_Progress,Ajax_Update_Member_Gtt_Whot_Shuffle_Cards_In_Progress,Login,Logout,Available_Settings,Unavailable_Settings,Transfer,Confirm_Transfer,Player_Connection,Game_Checker,Challenge,Missed_Challenges,Accept_Challenge,Decline_Challenge,Has_Challenge,Admin_Private_Space
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("",Home.as_view(),name="home_page"),
    path("profile/<str:user>",Profile.as_view(),name="profile_page"),
    path("<str:user>/settings",Settings.as_view(),name="settings_page"),
    path("searchPlayer",Search_Player.as_view(),name="search_player_page"),
    path("about",About.as_view(),name="about_page"),
    path("register",Register.as_view(),name="register_page"),
    path("Terms_And_Conditions",Terms_Conditions.as_view(),name="terms_conditions_page"),
    path("checkShuffleCardsInProgress", Ajax_Check_Member_Gtt_Whot_Shuffle_Cards_In_Progress.as_view(),name="check_shuffle_cards_in_progress"),
    path("updateShuffleCardsInProgress/<str:challenger>/<str:challenge>",Ajax_Update_Member_Gtt_Whot_Shuffle_Cards_In_Progress.as_view(), name="update_shuffle_cards_in_progress"),

    path("login",Login.as_view(),name="login_page"),
    path("logout",Logout.as_view(),name="logout_page"),

    path("available_settings/<str:user>",Available_Settings.as_view(),name="available_settings_page"),
    path("unavailable_settings/<str:user>",Unavailable_Settings.as_view(),name="unavailable_settings_page"),
    path("transfer/<str:user>",Transfer.as_view(),name="transfer_page"),
    path("confirm_transfer",Confirm_Transfer.as_view(),name="confirm_transfer_page"),

    path("play/<str:user>/amount/<str:amount>/<str:game_type>",Player_Connection.as_view(),name="player_connection_page"),
    path("checkGame",Game_Checker.as_view(),name="game_checker_page"),
    path("get/challenges/<str:user>",Challenge.as_view(),name="challenges_page"),
    path("missedChallenges",Missed_Challenges.as_view(),name="missed_challenges_page"),
    path("accept/challenge",Accept_Challenge.as_view(),name="accept_challenge_page"),
    path("decline/challenge",Decline_Challenge.as_view(),name="decline_challenge_page"),
    path("check/challenge",Has_Challenge.as_view(),name="has_challenge_page"),

    path("adminPrivateSpace",Admin_Private_Space.as_view(),name="admin_private_space_page"),


    # password resetting
    path("forgotPassword",auth_views.PasswordResetView.as_view(template_name="forgot_password.html"),name="reset_password"),
    path("passwordEmailSent",auth_views.PasswordResetDoneView.as_view(template_name="forgot_password_mail_sent.html"),name="password_reset_done"),
    path("reset/<uidb64>/<token>",auth_views.PasswordResetConfirmView.as_view(template_name="reset_password.html"),name="password_reset_confirm"),
    path("passwordResetSuccessfully",auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),name="password_reset_complete")
]