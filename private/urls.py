from django.urls import path
from .views import Get_All_Members_Info,Get_Member_Info,Credit_Member,Debit_Member,Admin_Help_Am_play_Gtt_Whott,Send_General_Mail,Send_Private_Mail,All_Black_List_Members,Add_Member_Black_List,Remove_Member_Black_List,Admin_Get_Game_Delay_Report,Admin_Remove_Member_Get_Game_Delay_Report,Admin_Quick_Add_Members_Phone_Numbers


urlpatterns = [
    path("getAllMembersInfo",Get_All_Members_Info.as_view(),name="get_all_members_info_page"),
    path("getMemberInfo",Get_Member_Info.as_view(),name="get_member_info_page"),
    path("creditMember",Credit_Member.as_view(),name="credit_member_page"),
    path("debitMember",Debit_Member.as_view(),name="debt_member_page"),
    path("adminHelpAmPlayGttWhott/<str:username>",Admin_Help_Am_play_Gtt_Whott.as_view(),name="admin_help_am_play_gtt_whott_page"),
    path("generalMail",Send_General_Mail.as_view(),name="general_email_page"),
    path("privateMail",Send_Private_Mail.as_view(),name="private_email_page"),
    path("allBlackListMembers",All_Black_List_Members.as_view(),name="blacklist_page"),
    path("blackListMember",Add_Member_Black_List.as_view(),name="blacklist_member_page"),
    path("<str:id>/<str:username>/remove",Remove_Member_Black_List.as_view(),name="remove_member_blacklist_page"),
    path("adminGetGameDelayReport",Admin_Get_Game_Delay_Report.as_view(),name="admin_get_game_delay_report_page"),
    path("adminRemoveGameDelayReport/<str:id>",Admin_Remove_Member_Get_Game_Delay_Report.as_view(),name="admin_remove_game_delay_report_page"),
    path("adminQuickAddPhoneNumbers",Admin_Quick_Add_Members_Phone_Numbers.as_view(),name="admin_quick_add_phone_number_page")
]
