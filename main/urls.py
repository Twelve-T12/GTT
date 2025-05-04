from django.urls import path
from .views import IndexPage,GamesPage,HowItWorksPage,TermsConditionPage,PrivacyPage,RegisterPage,LoginPage,LogoutPage,NotificationsAlertsPage,TournamentPage,LeaderBoardPage,HomePage,ChatPage,StartChat,MessagesPage,CheckUserChatProfile,ProfilePage,SettingsPage,StartGamePage,DepositPage,ConfirmDeposit,WithdrawalPage,StartTransferPage,Confirm_Transfer,TransactionHistoryPage,WithdrawalHistory,ProcessWithdrawal,NotificationPreferencePage,PrivacySettings,ChangePasswordPage,Available_Settings,Unavailable_Settings,Player_Connection,Missed_Challenges,Search_Player,Ajax_Check_Member_Gtt_Whot_Shuffle_Cards_In_Progress,Ajax_Update_Member_Gtt_Whot_Shuffle_Cards_In_Progress,Game_Checker,ContinueGame,Accept_Challenge,Decline_Challenge,Admin_Private_Space,sse_connection
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("",IndexPage.as_view(),name="index_page"),
    path("games",GamesPage.as_view(),name="games_page"),
    path("howItWorks",HowItWorksPage.as_view(),name="how_it_works_page"),
    path("Terms_And_Conditions",TermsConditionPage.as_view(),name="terms_conditions_page"),
    path("privacy",PrivacyPage.as_view(),name="privacy_page"),
    path("register",RegisterPage.as_view(),name="register_page"),
    path("login",LoginPage.as_view(),name="login_page"),
    path("logout",LogoutPage.as_view(),name="logout_page"),
    path("notifications",NotificationsAlertsPage.as_view(),name="notification_alerts_page"),
    path("tournaments",TournamentPage.as_view(),name="tournament_page"),
    path("leaderboard",LeaderBoardPage.as_view(),name="leaderboard_page"),
    path("home",HomePage.as_view(),name="home_page"),
    path("chats",ChatPage.as_view(),name="chat_page"),
    path("chat/<str:user>",StartChat.as_view(),name="start_chat_page"),
    path("message/<str:room_id>/<str:chat_one>/<str:chat_two>",MessagesPage.as_view(),name="messages_page"),
    path("about/<str:user>/profile",CheckUserChatProfile.as_view(),name="check_chat_user_profile_page"),
    path("profile/<str:user>",ProfilePage.as_view(),name="profile_page"),
    path("<str:user>/settings",SettingsPage.as_view(),name="settings_page"),
    path("startGame",StartGamePage.as_view(),name="start_game_page"),
    path("<str:amount>/confirmDeposit/<str:response>",ConfirmDeposit.as_view(),name="confirm_deposit_page"),
    path("makeDeposit",DepositPage.as_view(),name="make_deposit_page"),
    path("makeWithdrawal",WithdrawalPage.as_view(),name="make_withdrawal_page"),
    path("startTransfer",StartTransferPage.as_view(),name="start_transfer_page"),
    path("confirm_transfer",Confirm_Transfer.as_view(),name="confirm_transfer_page"),
    path("transactionHistory",TransactionHistoryPage.as_view(),name="transaction_history_page"),
    path("withdrawalHistory",WithdrawalHistory.as_view(),name="withdrawal_history_page"),
    path("process/<str:amount>/<str:commission>",ProcessWithdrawal.as_view(),name="process_withdrawal_page"),
    path("notificationPreference",NotificationPreferencePage.as_view(),name="notification_preference_page"),
    path("privacySettings",PrivacySettings.as_view(),name="privacy_settings_page"),
    path("changePassword",ChangePasswordPage.as_view(),name="change_password_page"),

    path("available_settings/<str:user>", Available_Settings.as_view(), name="available_settings_page"),
    path("unavailable_settings/<str:user>", Unavailable_Settings.as_view(), name="unavailable_settings_page"),
    path("play/<str:user>/amount/<str:amount>/<str:game_type>",Player_Connection.as_view(),name="player_connection_page"),
    path("missedChallenges",Missed_Challenges.as_view(),name="missed_challenges_page"),

    path("searchPlayer",Search_Player.as_view(),name="search_player_page"),
    path("checkShuffleCardsInProgress", Ajax_Check_Member_Gtt_Whot_Shuffle_Cards_In_Progress.as_view(),name="check_shuffle_cards_in_progress"),
    path("updateShuffleCardsInProgress/<str:challenger>/<str:challenge>",Ajax_Update_Member_Gtt_Whot_Shuffle_Cards_In_Progress.as_view(), name="update_shuffle_cards_in_progress"),







    path("checkGame",Game_Checker.as_view(),name="game_checker_page"),
    path("continue/game",ContinueGame.as_view(),name="continue_game_page"),

    path("accept/challenge",Accept_Challenge.as_view(),name="accept_challenge_page"),
    path("decline/challenge",Decline_Challenge.as_view(),name="decline_challenge_page"),


    path("adminPrivateSpace",Admin_Private_Space.as_view(),name="admin_private_space_page"),

    path("events/",sse_connection,name="sse_connection_function"),


    # password resetting
    path("forgotPassword",auth_views.PasswordResetView.as_view(template_name="forgot_password.html"),name="reset_password"),
    path("passwordEmailSent",auth_views.PasswordResetDoneView.as_view(template_name="forgot_password_mail_sent.html"),name="password_reset_done"),
    path("reset/<uidb64>/<token>",auth_views.PasswordResetConfirmView.as_view(template_name="reset_password.html"),name="password_reset_confirm"),
    path("passwordResetSuccessfully",auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),name="password_reset_complete")
]