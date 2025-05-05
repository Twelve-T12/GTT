from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import View
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Members, Available_Players, Transfer_History,Challenges,Admin_Setup,About_Game,Term_Condition,Notifications,Leaderboard,Tournaments,All_Messages,All_Chats,Withdrawals
import datetime
from datetime import datetime as d
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.decorators import method_decorator
from django.db import transaction
import time
import json
from gttWhott.models import Gtt_Whot
from django.utils.dateformat import format
from payments.paystack import initialize_transaction
from payments.paystack import verify_transaction



# home_page
class IndexPage(View):
    def get(self,request):
        return render(request,"index.html")

class GamesPage(View):
    def get(self,request):
        return render(request,"games.html")

class HowItWorksPage(View):
    def get(self,request):
        return render(request,"how_it_works.html")


class TermsConditionPage(View):
    def get(self,request):
        return render(request,"terms_condition.html")

class PrivacyPage(View):
    def get(self,request):
        return render(request,"privacy.html")


class RegisterPage(View):
    def get(self,request):
        if request.user.is_authenticated:
            logout = auth.logout(request)
        get_number_registered = int(Admin_Setup.objects.get(id=1).number_registered_members)
        get_international_registration_link = Admin_Setup.objects.get(id=1).admin_international_registration_link
        format_number_registered = "{:,}".format(get_number_registered)
        context = {
            "number_registered":get_number_registered,
            "total_registered":format_number_registered,
            "international_registration_link":get_international_registration_link
        }
        return render(request,"register.html",context)

    def post(self,request):
        username = request.POST["username"].lower()
        gender = request.POST["gender"]
        email = request.POST["email"]
        password = request.POST["password"]
        country = request.POST["country"]

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if True: #not All_Phone_Numbers.objects.filter(phone_number=phone_number).exists():
                    if len(password) >= 8:
                        create_new_user = User.objects.create_user(
                            username = username,
                            email = email,
                            password = password
                        )
                        new_member = Members.objects.create(
                            user = create_new_user,
                            initial_password = password,
                            gender = gender,
                            country = country,
                            user_game_link = f"/play/{username}/amount"
                        )
                        #updating number registered
                        get_number_registered = int(Admin_Setup.objects.get(id=1).number_registered_members)
                        new_registered_member = get_number_registered + 1
                        update_new_register = Admin_Setup.objects.filter(id=1).update(
                            number_registered_members = new_registered_member
                        )



                        # logging in user directly
                        user = auth.authenticate(
                            username=username,
                            password=password
                        )
                        accept = auth.login(request, user)

                        # get_user_id = User.objects.get(username=username).id
                        # #Create Credit Transaction
                        # new_credit_transaction = Transfer_History.objects.create(
                        #     transaction_type = "Credit",
                        #     sender_name = "Register Bonus",
                        #     amount = 200
                        # )
                        # #Getting And Updating Member
                        # get_member = Members.objects.get(id=int(get_user_id))
                        # update_member_transfer_history = get_member.transaction_history.add(new_credit_transaction)
                        # update_member = Members.objects.filter(id=int(get_user_id)).update(
                        #     has_transfer = True
                        # )
                        # messages.success(request, f"You received #200 sign up bonus")
                        return redirect("home_page")
                    else:
                        messages.error(request,"password must not be less than 8 characters!")
                        return redirect("register_page")
                else:
                    pass
                    # messages.error(request, f"{phone_number} already exists")
                    # return redirect("register_page")
            else:
                messages.error(request,f"{email} already exists")
                return redirect("register_page")
        else:
            messages.error(request,f"{username} already exists")
            return redirect("register_page")


class LoginPage(View):
    def get(self,request):
        if request.user.is_authenticated:
            logout = auth.logout(request)
        return render(request,"login.html")

    def post(self,request):
        username = request.POST["username"].lower()
        password = request.POST["password"]

        check_user = auth.authenticate(
            username = username,
            password = password
        )
        if check_user is not None:
            login_user  = auth.login(request,check_user)
            messages.success(request, f"Welcome back '{username}'")
            return redirect("home_page")
        else:
            messages.error(request,"Invalid Details!")
            return redirect("login_page")

class LogoutPage(View):
    def get(self,request):
        logout = auth.logout(request)
        return redirect("index_page")



class HomePage(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=user_id)
            update_member = Members.objects.select_for_update().filter(id=int(user_id))
            update_member.update(
                deposit_in_progress=True,
            )
            if not get_member.is_available:
                update_member = Members.objects.filter(id=user_id).update(
                    can_transfer= True
                )
            if get_member.has_game:
                now = datetime.datetime.now()
                challenge_expiry_time = get_member.challenge_expiry_time
                if challenge_expiry_time > now:
                    return redirect(f"game_checker_page")
                else:
                    update_member = Members.objects.filter(id=user_id).update(
                        has_game = False
                    )
                    return redirect("home_page")
            else:
                #calculating member wining percent
                member_number_of_play = get_member.number_of_play
                member_number_of_win = get_member.number_of_win
                if int(member_number_of_play) > 0:
                    calculate_member_win_ratio = int(member_number_of_win) / int(member_number_of_play) * 100
                    round_member_win_ratio = round(calculate_member_win_ratio)
                    # update member win ratio
                    update_wint_ratio = Members.objects.filter(id=user_id).update(
                        win_ratio=round_member_win_ratio,
                        shuffling_starting_game_on_progress=False,
                        shuffling_check=False
                    )
                else:
                    round_member_win_ratio = 0
                    # update member win ratio
                    update_wint_ratio = Members.objects.filter(id=user_id).update(
                        win_ratio=round_member_win_ratio,
                        shuffling_starting_game_on_progress=False,
                        shuffling_check=False
                    )
                member_balance = get_member.balance
                member_started_game = get_member.game_started
                member_is_blacklisted = get_member.is_blacklisted
                member_current_game = get_member.current_game_type
                member_current_opponent = get_member.current_opponent
                member_current_challenge_wining_amount = int(get_member.current_game_wining_amount)
                format_balance = "{:,}".format(member_balance)
                get_member_challenges = get_member.my_challenges.all()
                get_has_clicked_missed_challenges = get_member.has_clicked_missed_challenges
                all_available_players = Available_Players.objects.all()
                context = {
                    "username":username,
                    "balance":format_balance,
                    "is_blacklisted":member_is_blacklisted,
                    "started_game":member_started_game,
                    "current_game":member_current_game,
                    "opponent":member_current_opponent,
                    "challenge_wining_price":"{:,}".format(member_current_challenge_wining_amount),
                    "has_clicked_missed_challenges":get_has_clicked_missed_challenges,
                    "available_players":all_available_players,
                    "challenge":get_member_challenges
                }
                return render(request,"home.html",context)
        else:
            return redirect("index_page")



class NotificationsAlertsPage(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=int(user_id))
            get_member_balance = get_member.balance
            get_member_notifications = get_member.notifications.all()
            for i in get_member_notifications:
                update_seen_notification = Notifications.objects.select_for_update().filter(id=int(i.id))
                update_seen_notification.update(
                    is_seen = True
                )
            if not get_member.is_available:
                update_member = Members.objects.filter(id=user_id).update(
                    can_transfer= True
                )
            update_member = Members.objects.select_for_update().filter(id=int(user_id))
            update_member.update(
                deposit_in_progress=True,
            )
            context = {
                "username":username,
                "balance":"{:,}".format(get_member_balance),
                "notifications":get_member_notifications
            }
            return render(request,"notifications.html",context)
        else:
            return redirect("index_page")


class TournamentPage(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_tournaments = Tournaments.objects.all()
            get_member = Members.objects.get(id=int(user_id))
            member_balance = get_member.balance
            member_allow_tournament_notification = get_member.allow_tournament_alert
            context = {
                "username":username,
                "balance":"{:,}".format(member_balance),
                "tournaments":get_tournaments,
                "allow_notification":member_allow_tournament_notification
            }
            return render(request,"tournament.html",context)
        else:
            return redirect("index_page")


class LeaderBoardPage(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_leaderboard = Leaderboard.objects.all()
            get_member = Members.objects.get(id=int(user_id))
            member_balance = get_member.balance
            context = {
                "username": username,
                "balance":"{:,}".format(member_balance),
                "leaderboard": get_leaderboard
            }
            return render(request, "leaderboard.html", context)
        else:
            return redirect("index_page")


class ChatPage(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=int(user_id))
            member_balance = get_member.balance
            get_member_chats = get_member.my_chats.order_by('date_created')
            update_member = Members.objects.select_for_update().filter(id=int(user_id))
            update_member.update(
                deposit_in_progress=True,
            )
            context = {
                "username":username,
                "balance":"{:,}".format(member_balance),
                "chats":get_member_chats
            }
            return render(request,"chat.html",context)
        else:
            return redirect("index_page")

@method_decorator(transaction.atomic,name="dispatch")
class StartChat(View):
    def get(self,request,user):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=int(user_id))
            if username != user:
                if User.objects.filter(username=user).exists():
                    if All_Chats.objects.filter(chat_one=username,chat_two=user).exists():
                        get_chat = All_Chats.objects.select_for_update().get(chat_one=username,chat_two=user)
                        chat_id = get_chat.id
                        chat_one = get_chat.chat_one
                        chat_two = get_chat.chat_two
                        return redirect(f"/message/{chat_id}/{chat_two}/{chat_one}")
                    elif All_Chats.objects.filter(chat_one=user,chat_two=username).exists():
                        get_chat = All_Chats.objects.select_for_update().get(chat_one=user,chat_two=username)
                        chat_id = get_chat.id
                        chat_one = get_chat.chat_one
                        chat_two = get_chat.chat_two
                        return redirect(f"/message/{chat_id}/{chat_two}/{chat_one}")
                    else:
                        print("Start Creating vhat and message")
                        creating_new_message = All_Messages.objects.select_for_update().create(
                            sender = username,
                            receiver = user,
                        )
                        creating_new_chat = All_Chats.objects.select_for_update().create(
                            chat_one = username,
                            chat_two = user,
                            last_sender = username
                        )
                        chat_id = creating_new_chat.id
                        chat_one = creating_new_chat.chat_one
                        chat_two = creating_new_chat.chat_two
                        adding_message_to_chat = creating_new_chat.messages.add(creating_new_message)
                        # updating member
                        update_member_chat = get_member.my_chats.add(creating_new_chat)
                        # getting and updating user chat
                        get_user_id = User.objects.get(username=user).id
                        get_user_member = Members.objects.get(id=int(get_user_id))
                        update_user_member_chat = get_user_member.my_chats.add(creating_new_chat)
                        # should return to their message room
                        return redirect(f"/message/{chat_id}/{chat_two}/{chat_one}")
                else:
                    messages.error(request,f"'@{user}' does not exists")
                    return redirect("index_page")
            else:
                messages.error(request,"oops,sorry cant start chat")
                return redirect("home_page")
        else:
            return redirect("index_page")



@method_decorator(transaction.atomic,name="dispatch")
class MessagesPage(View):
    def get(self,request,room_id,chat_one,chat_two):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=int(user_id))
            get_chat = All_Chats.objects.get(id=int(room_id))
            get_last_messages = get_chat.messages.last()
            get_last_receiver = get_last_messages.receiver
            print(f"us{username}")
            print(f"rc {get_last_receiver}")
            if get_last_receiver == username:
                print(f"ls {get_last_receiver}")
                update_chat_last_seen = All_Chats.objects.select_for_update().filter(id=int(room_id))
                update_chat_last_seen.update(
                    last_message_seen = True
                )
            is_room_exists = All_Chats.objects.select_for_update().filter(id=int(room_id))
            if User.objects.filter(username=chat_one).exists():
                if User.objects.filter(username=chat_two).exists():
                    allow_profile_view = True
                    if username != chat_one:
                        # get_chat_one_allow_profile_view
                        get_chat_one_id = User.objects.get(username=chat_one).id
                        get_member_chat_one = Members.objects.get(id=int(get_chat_one_id))
                        allow_profile_view = get_member_chat_one.profile_visibility_privacy
                    else:
                        # get_chat_two_allow_profile_view
                        get_chat_two_id = User.objects.get(username=chat_two).id
                        get_member_chat_two = Members.objects.get(id=int(get_chat_two_id))
                        allow_profile_view = get_member_chat_two.profile_visibility_privacy
                    if is_room_exists.exists():
                        get_room = All_Chats.objects.get(id=int(room_id))
                        get_all_messages = get_room.messages.all()
                        chat_one = get_room.chat_one
                        chat_two = get_room.chat_two
                        update_member_current_room_id = Members.objects.select_for_update().filter(id=int(user_id))
                        update_member_current_room_id.update(
                            current_room_id = int(room_id)
                        )
                        context = {
                            "username":username,
                            "balance":"{:,}".format(get_member.balance),
                            "messages":get_all_messages,
                            "room_id":int(room_id),
                            "chat_one":chat_one,
                            "chat_two":chat_two,
                            "allow_profile_view":allow_profile_view
                        }
                        return render(request,"messages.html",context)
                    else:
                        return redirect("index_page")
                else:
                    return redirect("index_page")
            else:
                return redirect("index_page")
        else:
            return redirect("index_page")


    def post(self,request,room_id,chat_one,chat_two):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=int(user_id))
            is_room_exists = All_Chats.objects.select_for_update().filter(id=int(room_id))
            if User.objects.filter(username=chat_one).exists():
                if User.objects.filter(username=chat_two).exists():
                    if is_room_exists.exists():
                        if username != chat_two:
                            print(f"user is chat one")
                            if All_Chats.objects.filter(chat_one=username,chat_two=chat_two).exists():
                                get_message = request.POST["message"]
                                if get_message != "":
                                    print(f"{get_message} user is chat one")
                                    create_new_message = All_Messages.objects.create(
                                        sender = username,
                                        receiver = chat_two,
                                        message = get_message
                                    )
                                    get_chat = All_Chats.objects.select_for_update().get(id=int(room_id))
                                    get_chat.date_created = d.now()
                                    get_chat.last_message_seen = False
                                    get_chat.last_sender = username
                                    get_chat.save()
                                    add_message = get_chat.messages.add(create_new_message)
                                    return redirect(f"/message/{room_id}/{chat_one}/{chat_two}")
                                else:
                                    return redirect("home_page")
                            else:
                                return redirect("index_page")
                        elif username != chat_one:
                            print(f" user is chat two {chat_one}")
                            if All_Chats.objects.filter(chat_one=chat_one,chat_two=username).exists():
                                get_message = request.POST["message"]
                                if get_message != "":
                                    print(get_message)
                                    create_new_message = All_Messages.objects.create(
                                        sender = username,
                                        receiver = chat_one,
                                        message = get_message
                                    )
                                    get_chat = All_Chats.objects.select_for_update().get(id=int(room_id))
                                    get_chat.date_created = d.now()
                                    get_chat.last_message_seen = False
                                    get_chat.last_sender = username
                                    get_chat.save()
                                    add_message = get_chat.messages.add(create_new_message)
                                    return redirect(f"/message/{room_id}/{chat_one}/{chat_two}")
                                else:
                                    return redirect("home_page")
                            else:
                                return redirect("index_page")
                        else:
                            print(f"user is same")
                            if All_Chats.objects.filter(chat_one=username, chat_two=username).exists():
                                get_message = request.POST["message"]
                                if get_message != "":
                                    print(f"{get_message} user is chat one")
                                    create_new_message = All_Messages.objects.create(
                                        sender=username,
                                        receiver=username,
                                        message=get_message
                                    )
                                    get_chat = All_Chats.objects.select_for_update().get(id=int(room_id))
                                    get_chat.date_created = d.now()
                                    get_chat.last_message_seen = False
                                    get_chat.last_sender = username
                                    get_chat.save()
                                    add_message = get_chat.messages.add(create_new_message)
                                    return redirect(f"/message/{room_id}/{chat_one}/{chat_two}")
                                else:
                                    return redirect("home_page")
                            else:
                                return redirect("index_page")
                    else:
                        messages.error(request,"Not Id")
                        return redirect("index_page")
                else:
                    return redirect("index_page")
            else:
                return redirect("index_page")
        else:
            return redirect("index_page")



class CheckUserChatProfile(View):
    def get(self,request,user):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=int(user_id))
            if user != username and User.objects.filter(username=user).exists():
                get_user = User.objects.get(username=user)
                get_user_id = get_user.id
                get_user_username = get_user.username
                get_user_member = Members.objects.get(id=int(get_user_id))
                if get_user_member.profile_visibility_privacy:
                    user_member_gender = get_user_member.gender
                    user_member_country = get_user_member.country
                    user_member_game_played = get_user_member.number_of_play
                    user_member_win = get_user_member.number_of_win
                    user_member_loss = get_user_member.number_of_loss
                    user_member_highest_win = get_user_member.highest_win
                    user_member_highest_loss = get_user_member.highest_loss
                    user_member_date_joined = get_user.date_joined
                    context = {
                        "username":username,
                        "balance":"{:,}".format(get_member.balance),
                        "user_username":get_user_username,
                        "user_gender":user_member_gender,
                        "user_country":user_member_country,
                        "user_game_played":"{:,}".format(user_member_game_played),
                        "user_win":"{:,}".format(user_member_win),
                        "user_loss":"{:,}".format(user_member_loss),
                        "user_highest_win":"{:,}".format(user_member_highest_win),
                        "user_highest_lost":"{:,}".format(user_member_highest_loss),
                        "user_date_joined":user_member_date_joined
                    }
                    return render(request,"user_chat_profile.html",context)
                else:
                    return redirect("home_page")
            else:
                return redirect("index_page")
        else:
            return redirect("index_page")



class ProfilePage(View):
    def get(self,request,user):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=user_id)
            update_member = Members.objects.select_for_update().filter(id=int(user_id))
            update_member.update(
                deposit_in_progress=True,
            )
            if not get_member.is_available:
                update_member = Members.objects.filter(id=user_id).update(
                    can_transfer= True
                )
            if get_member.has_game:
                now = datetime.datetime.now()
                challenge_expiry_time = get_member.challenge_expiry_time
                if challenge_expiry_time > now:
                    return redirect(f"game_checker_page")
                else:
                    update_member = Members.objects.filter(id=user_id).update(
                        has_game=False,
                    )
                    return redirect("home_page")
            else:
                get_member = Members.objects.get(id=user_id)
                member_email = request.user.email
                member_gender = get_member.gender
                member_number_of_play = get_member.number_of_play
                format_play = "{:,}".format(member_number_of_play)
                member_number_of_draw = get_member.number_of_draw
                format_draw = "{:,}".format(member_number_of_draw)
                member_number_of_win = get_member.number_of_win
                format_win = "{:,}".format(member_number_of_win)
                member_number_of_loss = get_member.number_of_loss
                format_loss = "{:,}".format(member_number_of_loss)
                if int(member_number_of_play) > 0:
                    calculate_member_win_ratio = int(member_number_of_win)/int(member_number_of_play) * 100
                    round_member_win_ratio = round(calculate_member_win_ratio)
                    #update member win ratio
                    update_wint_ratio = Members.objects.filter(id=user_id).update(
                        win_ratio = round_member_win_ratio,
                        shuffling_starting_game_on_progress=False,
                        shuffling_check=False
                    )
                else:
                    round_member_win_ratio = 0
                    # update member win ratio
                    update_wint_ratio = Members.objects.filter(id=user_id).update(
                        win_ratio=round_member_win_ratio,
                        shuffling_starting_game_on_progress=False,
                        shuffling_check=False
                    )
                member_balance = get_member.balance
                format_balance = "{:,}".format(member_balance)
                member_win_ratio = round_member_win_ratio
                member_number_of_reports = int(get_member.number_of_reports)
                format_member_number_of_reports = "{:,}".format(member_number_of_reports)
                context = {
                    "username": username,
                    "country":get_member.country,
                    "email":member_email,
                    "gender":member_gender,
                    "balance": format_balance,
                    "total_play":format_play,
                    "total_draw":format_draw,
                    "total_loss":format_loss,
                    "total_win":format_win,
                    "win_ratio":member_win_ratio,
                    "total_reports":member_number_of_reports,
                    "format_total_reports":format_member_number_of_reports,
                    "highest_win":"{:,}".format(get_member.highest_win),
                    "highest_loss":"{:,}".format(get_member.highest_loss)
                }
                return render(request,"profile.html",context)
        else:
            return redirect("index_page")


class SettingsPage(View):
    def get(self,request,user):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=user_id)
            update_member = Members.objects.select_for_update().filter(id=int(user_id))
            update_member.update(
                deposit_in_progress=True,
            )
            if not get_member.is_available:
                update_member = Members.objects.filter(id=user_id).update(
                    can_transfer= True
                )
            if get_member.has_game:
                now = datetime.datetime.now()
                challenge_expiry_time = get_member.challenge_expiry_time
                if challenge_expiry_time > now:
                    return redirect(f"game_checker_page")
                else:
                    update_member = Members.objects.filter(id=user_id).update(
                        has_game=False,
                    )
                    return redirect("home_page")
            else:
                # calculating member wining percent
                member_number_of_play = get_member.number_of_play
                member_number_of_win = get_member.number_of_win
                if int(member_number_of_play) > 0:
                    calculate_member_win_ratio = int(member_number_of_win) / int(member_number_of_play) * 100
                    round_member_win_ratio = round(calculate_member_win_ratio)
                    # update member win ratio
                    update_wint_ratio = Members.objects.filter(id=user_id).update(
                        win_ratio=round_member_win_ratio,
                        shuffling_starting_game_on_progress=False,
                        shuffling_check=False
                    )
                else:
                    round_member_win_ratio = 0
                    # update member win ratio
                    update_wint_ratio = Members.objects.filter(id=user_id).update(
                        win_ratio=round_member_win_ratio,
                        shuffling_starting_game_on_progress=False,
                        shuffling_check=False
                    )
                get_withdrawal_charge = int(Admin_Setup.objects.get(id=1).withdrawal_charges)
                get_member = Members.objects.get(id=user_id)
                member_balance = get_member.balance
                member_started_game = get_member.game_started
                member_is_blacklisted = get_member.is_blacklisted
                member_current_game = get_member.current_game_type
                format_balance = "{:,}".format(member_balance)
                member_is_available = get_member.is_available
                member_has_transfer = get_member.has_transfer
                member_transfers = get_member.transaction_history.all()
                get_admin = Admin_Setup.objects.get(id=1)
                get_admin_deposit_link = get_admin.deposit_link
                get_admin_withdrawal_link = get_admin.withdrawal_link
                context = {
                    "username": username,
                    "balance": format_balance,
                    "bal": member_balance,
                    "current_game":member_current_game,
                    "deposit_link":get_admin_deposit_link,
                    "withdrawal_link":get_admin_withdrawal_link,
                    "withdrawal_charges":get_withdrawal_charge,
                    "started_game":member_started_game,
                    "is_blacklisted":member_is_blacklisted,
                    "available":member_is_available,
                    "transfer":member_has_transfer,
                    "transactions":member_transfers
                }
                return render(request, "settings.html", context)
        else:
            return redirect("index_page")


class StartGamePage(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=int(user_id))
            member_balance = get_member.balance
            member_is_available = get_member.is_available
            context = {
                "username":username,
                "balance":"{:,}".format(member_balance),
                "is_available":member_is_available,
                "started_game": get_member.game_started,
                "current_game": get_member.current_game_type,
                "opponent": get_member.current_opponent,
                "challenge_wining_price": "{:,}".format(get_member.current_game_wining_amount),
            }
            return render(request,"start_game.html",context)
        else:
            return redirect("index_page")


class DepositPage(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=user_id)
            member_balance = get_member.balance
            update_member = Members.objects.select_for_update().filter(id=int(user_id))
            update_member.update(
                deposit_in_progress=True,
            )
            context = {
                "username":username,
                "balance":"{:,}".format(member_balance)
            }
            return render(request,"make_deposit.html",context)
        else:
            return redirect("index_page")

    def post(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            update_member = Members.objects.select_for_update().filter(id=int(user_id))
            update_member.update(
                deposit_in_progress=True,
            )
            email = request.user.email
            amount = request.POST["amount"]
            print(f"amount::{amount}")
            callback_url = f'https://goldentwelve.onrender.com/{amount}/confirmDeposit/response'
            response = initialize_transaction(email, amount, callback_url)
            print(response)

            if response.get('status'):
                print("EERRAMM")
                return redirect(response['data']['authorization_url'])
            else:
                messages.error(request,"opps,sorry something went wrong")
                return redirect("home_page")


@method_decorator(transaction.atomic,name="dispatch")
class ConfirmDeposit(View):
    def get(self,request,amount,response):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=int(user_id))
            member_balance = get_member.balance
            get_member_deposit_in_progress = get_member.deposit_in_progress

            if get_member_deposit_in_progress:
                reference = request.GET.get('reference')
                result = verify_transaction(reference)

                if result['status'] and result['data']['status'] == 'success':
                    # Payment successful, update your DB here
                    new_balance = int(amount) + int(get_member.balance)
                    update_member = Members.objects.select_for_update().filter(id=int(user_id))
                    update_member.update(
                        balance = int(new_balance),
                        deposit_in_progress = False,
                    )
                    # creating notification
                    new_notification = Notifications.objects.create(
                        notification_type = "System_Message",
                        notification_message = f"Your account was credited with #{'{:,}'.format(int(amount))} deposit"
                    )
                    add_notification = get_member.notifications.add(new_notification)
                    get_new_member_balance = Members.objects.get(id=user_id).balance
                    context = {
                        "username":username,
                        "balance":"{:,}".format(get_new_member_balance),
                        "amount":"{:,}".format(int(amount))
                    }
                    return render(request,"deposit_success.html",context)
                update_member = Members.objects.select_for_update().filter(id=int(user_id))
                update_member.update(
                    deposit_in_progress=False,
                )
                context = {
                    "username": username,
                    "balance": member_balance,
                    "amount": "{:,}".format(int(amount))
                }
                return render(request, "deposit_failed.html", context)
            else:
                messages.error(request,"oops can't process transaction")
                return redirect("home_page")
        else:
            return redirect("index_page")


class WithdrawalPage(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=user_id)
            member_balance = get_member.balance
            context = {
                "username":username,
                "balance":"{:,}".format(member_balance)
            }
            return render(request,"make_withdrawal.html",context)
        else:
            return redirect("index_page")

class StartTransferPage(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=user_id)
            member_balance = get_member.balance
            if not get_member.is_available:
                update_member = Members.objects.filter(id=user_id).update(
                    can_transfer= True
                )
            context = {
                "username":username,
                "balance":"{:,}".format(member_balance)
            }
            return render(request,"start_transfer.html",context)
        else:
            return redirect("home_page")


    def post(self, request):
        if request.user.is_authenticated:
            receiver_username = request.POST["receiver_username"].lower()
            if User.objects.filter(username=receiver_username).exists():
                if request.user.username != receiver_username:
                    amount = int(request.POST["amount"])
                    narration = request.POST["narration"]
                    print(narration)
                    user_id = request.user.id
                    get_member = Members.objects.get(id=user_id)
                    member_balance = get_member.balance
                    charges = int(Admin_Setup.objects.get(id=1).transfer_charges)
                    checking_remaining_balance = member_balance - charges - amount
                    member_can_transfer = get_member.can_transfer
                    if member_can_transfer:
                        if amount >= 500:
                            if checking_remaining_balance >= 0:
                                get_receiver_user = User.objects.get(username=receiver_username)
                                receiver_id = get_receiver_user.id
                                receiver_email = get_receiver_user.email
                                get_receiver = Members.objects.get(id=receiver_id)
                                format_amount = "{:,}".format(amount)
                                admin_charges = charges
                                format_charges = "{:,}".format(admin_charges)
                                total_charges = int(amount) + int(admin_charges)
                                context = {
                                    "username":request.user.username,
                                    "balance":"{:,}".format(member_balance),
                                    "receiver_username": receiver_username,
                                    "receiver_email": receiver_email,
                                    "amount": amount,
                                    "service_charges": admin_charges,
                                    "format_amount": format_amount,
                                    "format_charges": format_charges,
                                    "narration":narration,
                                    "total_fee":"{:,}".format(total_charges)
                                }
                                return render(request, "transfer_summary.html", context)
                            else:
                                messages.error(request, f"not enough balance")
                                return redirect("start_transfer_page")
                        else:
                            messages.error(request, f"Minimum Transfer 500")
                            return redirect("start_transfer_page")
                    else:
                        messages.error(request, f"Can't process transaction,Pleas check 'Avaialability Settings'")
                        return redirect("start_transfer_page")
                else:
                    messages.error(request,
                                  f"Transfer Not Accepted...'@{request.user.username}' to '@{request.user.username}'")
                    return redirect("start_transfer_page")
            else:
                messages.error(request, f"'@{receiver_username}' not found")
                return redirect("start_transfer_page")
        else:
            return redirect("index_page")

@method_decorator(transaction.atomic,name="dispatch")
class Confirm_Transfer(View):
    def post(self, request):
        if request.user.is_authenticated:
            user_id = request.user.id
            receiver_username = request.POST["receiver_username"]
            amount = int(request.POST["amount"])
            charges = int(request.POST["charges"])
            narration = request.POST["narration"]
            format_amount = "{:,}".format(amount)
            format_charges = "{:,}".format(charges)

            get_member = Members.objects.select_for_update().get(id=user_id)
            member_balance = get_member.balance
            charges = int(Admin_Setup.objects.get(id=1).transfer_charges)
            checking_remaining_balance = member_balance - charges - amount
            member_can_transfer = get_member.can_transfer
            if member_can_transfer:
                if amount >= 500:
                    if checking_remaining_balance >= 0:
                        # getting receiver
                        get_receiver_id = User.objects.get(username=receiver_username).id
                        get_receiver = Members.objects.select_for_update().get(id=get_receiver_id)
                        receiver_balance = int(get_receiver.balance)
                        increase_receiver_balance = int(receiver_balance + amount)
                        update_receiver = Members.objects.select_for_update().filter(id=get_receiver_id)
                        update_receiver.update(
                            balance=increase_receiver_balance,
                            has_transfer=True
                        )
                        # Updating Transaction History
                        create_credit_transaction = Transfer_History.objects.create(
                            transaction_type="Credit_Transfer",
                            transaction_topic=f"Transfer from @{request.user.username}",
                            sender_name=request.user.username,
                            receiver_name=receiver_username,
                            amount=format_amount,
                            charges=format_charges,
                            net_balance="{:,}".format(increase_receiver_balance)
                        )
                        # adding transaction to receiver
                        add_credit_transaction = get_receiver.transaction_history.add(create_credit_transaction)

                        # creating notification for receiver
                        creating_new_notification = Notifications.objects.create(
                            notification_type = "Transfer_Message",
                            notification_message = f"You received #{format_amount} worth of GOLD from @{request.user.username} '{narration}'"
                        )
                        adding_notification_receiver = get_receiver.notifications.add(creating_new_notification)

                        # setting sender
                        user_id = request.user.id
                        get_member = Members.objects.select_for_update().get(id=user_id)
                        member_balance = int(get_member.balance)
                        member_admin_charge = get_member.admin_charge
                        new_admin_charges = int(member_admin_charge + charges)
                        decrease_sender_balance = member_balance - amount - charges
                        update_sender = Members.objects.select_for_update().filter(id=user_id)
                        update_sender.update(
                            balance=decrease_sender_balance,
                            has_transfer=True,
                            admin_charge=new_admin_charges
                        )
                        # Update Transaction History
                        create_debit_transaction = Transfer_History.objects.create(
                            transaction_type="Debit_Transfer",
                            transaction_topic=f"Transfer to @{receiver_username}",
                            sender_name=request.user.username,
                            receiver_name=receiver_username,
                            amount=format_amount,
                            charges=format_charges,
                            net_balance="{:,}".format(decrease_sender_balance)
                        )
                        # add debit transaction
                        add_debit_transaction = get_member.transaction_history.add(create_debit_transaction)
                        messages.success(request, f"#{format_amount} sent to {receiver_username} Successfully!!")
                        context = {
                            "username":request.user.username,
                            "receiver":receiver_username,
                            "amount":format_amount,
                            "balance":"{:,}".format(get_member.balance)
                        }
                        return render(request,"transfer_successful.html",context)
                    else:
                        messages.error(request, f"Insufficient Balance")
                        return redirect("home_page")
                else:
                    messages.error(request, f"Minimum Transfer 500")
                    return redirect("start_transfer_page")
            else:
                messages.error(request, f"Can't process transaction,Pleas check 'Avaialability Settings'")
                return redirect("start_transfer_page")
        else:
            return redirect("index_page")





class TransactionHistoryPage(View):
    def get(self,request):
        if request.user.is_authenticated:
            get_username = request.user.username
            user_id = request.user.id
            get_member = Members.objects.get(id=int(user_id))
            get_member_balance = get_member.balance
            get_member_transaction_history = get_member.transaction_history.all()
            context = {
                "username":get_username,
                "balance":"{:,}".format(get_member_balance),
                "transactions":get_member_transaction_history
            }
            return render(request,"transaction_history.html",context)
        else:
            return redirect("index_page")


class WithdrawalHistory(View):
    def get(self,request):
        if request.user.is_authenticated:
            get_username = request.user.username
            user_id = request.user.id
            get_member = Members.objects.get(id=int(user_id))
            get_member_balance = get_member.balance
            get_member_withdrawal_history = get_member.my_withdrawals.all()
            context = {
                "username": get_username,
                "balance": "{:,}".format(get_member_balance),
                "withdrawals": get_member_withdrawal_history
            }
            return render(request, "withdrawal_history.html", context)
        else:
            return redirect("index_page")


@method_decorator(transaction.atomic,name="dispatch")
class ProcessWithdrawal(View):
    def get(self,request,amount,commission):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            amount = amount.replace(',','')
            commission = commission.replace(',', '')
            if int(amount) == 500:
                commission = 50
            if int(amount) == 1000:
                commission = 100
            if int(amount) == 2000 or int(amount) == 5000 or int(amount) == 10000:
                commission = 200
            if int(amount) == 50000 or int(amount) == 100000:
                commission = 1000
            get_member = Members.objects.get(id=int(user_id))
            new_balance = int(get_member.balance) - int(amount) - int(commission)
            if new_balance >= 0:
                create_new_withdrawal = Withdrawals.objects.create(
                    user = username,
                    amount = "{:,}".format(int(amount))
                )
                add_withdrawal_to_member = get_member.my_withdrawals.add(create_new_withdrawal)
                update_member = Members.objects.select_for_update().filter(id=int(user_id))
                update_member.update(
                    balance = new_balance
                )
                messages.success(request, f"Withdrawal placed successful")
                return redirect(f"withdrawal_history_page")
            else:
                messages.success(request, f"insufficient fund,can't process withdrawla")
                return redirect(f"/{username}/settings")
        else:
            return redirect("index_page")



class NotificationPreferencePage(View):
    def get(self,request):
        if request.user.is_authenticated:
            get_username = request.user.username
            user_id = request.user.id
            get_member = Members.objects.get(id=int(user_id))
            get_member_balance = get_member.balance
            get_member_allow_system_alert = get_member.allow_system_alert
            get_member_allow_challenge_alert = get_member.allow_missed_challenge_alert
            get_member_allow_tournament_alert = get_member.allow_tournament_alert
            get_member_allow_bonus_alert = get_member.allow_bonus_alert
            context = {
                "username":get_username,
                "balance":"{:,}".format(get_member_balance),
                "allow_system_alert": get_member_allow_system_alert,
                "allow_challenge_alert":get_member_allow_challenge_alert,
                "allow_tournament_alert":get_member_allow_tournament_alert,
                "allow_bonus_alert":get_member_allow_bonus_alert
            }
            return render(request,"notification_preference.html",context)
        else:
            return redirect("index_page")

    def post(self,request):
        if request.user.is_authenticated:
            get_system_alert = request.POST["system_alerts"]
            get_missed_challenge_alert = request.POST["missed_challenge_alert"]
            get_tournament_alert = request.POST["tournament_alert"]
            get_bonus_alert = request.POST["bonus_alert"]
            user_id = request.user.id
            update_member = Members.objects.filter(id=int(user_id)).update(
                allow_system_alert=get_system_alert,
                allow_missed_challenge_alert=get_missed_challenge_alert,
                allow_tournament_alert=get_tournament_alert,
                allow_bonus_alert=get_bonus_alert
            )
            messages.success(request, "Notification Preference Updated!")
            return redirect(f"/{request.user.username}/settings")
        else:
            return redirect("index_page")



class PrivacySettings(View):
    def get(self,request):
        if request.user.is_authenticated:
            get_username = request.user.username
            user_id = request.user.id
            get_member = Members.objects.get(id=int(user_id))
            get_member_balance = get_member.balance
            get_member_game_invite = get_member.game_invite_privacy
            get_member_profile_visibility = get_member.profile_visibility_privacy
            get_member_username_search = get_member.username_search_visibility_privacy
            get_member_balance_visibility = get_member.balance_visibility_privacy
            context = {
                "username":get_username,
                "balance":"{:,}".format(get_member_balance),
                "game_invite_privacy":get_member_game_invite,
                "profile_privacy":get_member_profile_visibility,
                "username_privacy":get_member_username_search,
                "balance_privacy":get_member_balance_visibility
            }
            return render(request,"privacy_settings.html",context)
        else:
            return redirect("index_page")


    def post(self,request):
        if request.user.is_authenticated:
            get_game_privacy = request.POST["game_invite_privacy"]
            get_profile_privacy = request.POST["profile_privacy"]
            get_username_privacy = request.POST["username_privacy"]
            get_balance_privacy = request.POST["balance_privacy"]
            user_id = request.user.id
            update_member = Members.objects.filter(id=int(user_id)).update(
                game_invite_privacy = get_game_privacy,
                profile_visibility_privacy = get_profile_privacy,
                username_search_visibility_privacy = get_username_privacy,
                balance_visibility_privacy = get_balance_privacy
            )
            messages.success(request,"Privacy Updated!")
            return redirect(f"/{request.user.username}/settings")
        else:
            return redirect("index_page")


class ChangePasswordPage(View):
    def get(self,request):
        if request.user.is_authenticated:
            get_username = request.user.username
            user_id = request.user.id
            get_member = Members.objects.get(id=int(user_id))
            get_member_balance = get_member.balance
            get_member_transaction_history = get_member.transaction_history.all()
            context = {
                "username":get_username,
                "balance":"{:,}".format(get_member_balance),
                "transactions":get_member_transaction_history
            }
            return render(request,"change_password.html",context)
        else:
            return redirect("index_page")


@method_decorator(transaction.atomic,name="dispatch")
class Available_Settings(View):
    def post(self,request,user):
        if request.user.is_authenticated:
            game_type = request.POST["game_type"]
            stake_amount = int(request.POST["stake_amount"])
            user_id = request.user.id
            get_member = Members.objects.select_for_update().get(id=user_id)
            member_balance = get_member.balance
            member_started_game = get_member.game_started
            if not member_started_game:
                if not Available_Players.objects.filter(username=user).exists():
                    if stake_amount >= 500:
                        if stake_amount <= member_balance:
                            member_gender = get_member.gender
                            member_win_ratio = get_member.win_ratio
                            member_chat_link = ""
                            member_allow_search = get_member.username_search_visibility_privacy
                            member_country = get_member.country
                            member_game_link = f"play/{user}/amount/{stake_amount}/{game_type}"
                            update_member_game_link = Members.objects.select_for_update().filter(id=user_id)
                            update_member_game_link.update(
                                user_game_link = member_game_link
                            )
                            #adding member to available_players_link
                            new_available_player = Available_Players.objects.create(
                                username = user,
                                stake_amount = stake_amount,
                                win_ratio = member_win_ratio,
                                game_link = member_game_link,
                                gender = member_gender,
                                game_type= game_type,
                                chat_link = member_chat_link,
                                allow_player_search = member_allow_search,
                                country = member_country,
                                format_stake_amount = "{:,}".format(stake_amount)
                            )

                            # updating member availability
                            available_id = Available_Players.objects.select_for_update().get(username=user).id
                            update_player_availability = Members.objects.select_for_update().filter(id=user_id)
                            update_player_availability.update(
                                is_available=True,
                                available_id=available_id,
                                can_transfer=False
                            )
                            messages.success(request,"Ready to Play!")
                            return redirect("home_page")
                        else:
                            messages.error(request,f"Insufficient Balance")
                            return redirect(f"/{user}/settings")
                    else:
                        messages.error(request, f"Minimum Stake Amount is 500 GOLD")
                        return redirect(f"/{user}/settings")
                else:
                    messages.error(request, f"Already Available")
                    return redirect(f"home_page")
            else:
                return redirect("continue_game_page")
        else:
            return redirect("index_page")



@method_decorator(transaction.atomic,name="dispatch")
class Unavailable_Settings(View):
    def post(self,request,user):
        if request.user.is_authenticated:
            user_id = request.user.id
            if Available_Players.objects.filter(username=user).exists():
                get_user = Available_Players.objects.get(username=user).id
                remove_payer = Available_Players.objects.select_for_update().filter(id=get_user)
                remove_payer.delete()
                update_user = Members.objects.filter(id=user_id)
                update_user.update(
                    is_available = False,
                    can_transfer = True
                )
                messages.success(request,f"{user} now unavailable")
            else:
                messages.success(request, f"{user} not available")
            return redirect(f"/{user}/settings")
        else:
            return redirect("login_page")


@method_decorator(transaction.atomic,name="dispatch")
class Player_Connection(View):
    def get(self,request,user,amount,game_type):
        if request.user.is_authenticated:
            if User.objects.filter(username=user).exists():
                if user != request.user.username:
                    get_challenged_id = User.objects.select_for_update().get(username=user).id
                    get_challenged_member_availability = Members.objects.get(id=get_challenged_id).is_available
                    user_id = request.user.id
                    get_user = Members.objects.get(id=user_id)
                    get_user_availability = get_user.is_available
                    get_user_balance = int(get_user.balance)
                    get_opp_game_started = Members.objects.get(id=int(get_challenged_id)).game_started
                    if get_user_balance >= int(amount):
                        if not get_user.game_started and not get_opp_game_started:
                            if get_user_availability:
                                if get_challenged_member_availability:
                                    create_challenge = Challenges.objects.create(
                                        challenger = request.user.username,
                                        amount = int(amount),
                                        challenge_game_type = game_type,
                                        challenged = user
                                    )
                                    #adding challenge
                                    get_challenged = Members.objects.select_for_update().get(id=get_challenged_id).my_challenges
                                    add_challenge = get_challenged.add(create_challenge)
                                    messages.success(request,f"Request Sent To '{user}'...Waiting For '{user}' Response,If No Respoonse In 30 Seconds '{user}' Probably Declined Or '{user}' Is Not Online. ")
                                    return redirect("home_page")
                                else:
                                    messages.error(request,f"{user} Not Available")
                                    return redirect("home_page")
                            else:
                                messages.error(request,f"Please Make Sure You are Available!!!")
                                return redirect("home_page")
                        else:
                            messages.error(request,f"user already in a game")
                            return redirect("home_page")
                    else:
                        messages.error(request,f"Insufficient Fund")
                        return redirect("home_page")
                else:
                    messages.error(request,f"Can't connect to You")
                    return redirect("home_page")
            else:
                messages.error(request,f"{user} not recognized")
                return redirect("home_page")
        else:
            return redirect("login_page")






class Search_Player(View):
    def post(self,request):
        player_name = request.POST["player_name"].lower()
        if User.objects.filter(username=player_name).exists():
            get_user_id = int(User.objects.get(username=player_name).id)
            if Available_Players.objects.filter(username=player_name).exists() and Members.objects.get(id=get_user_id).is_available:
                get_member_availability_id = Members.objects.get(id=get_user_id).available_id
                get_member_availability_details = Available_Players.objects.get(id=get_member_availability_id)
                data = {
                    "player_name": player_name,
                    "member_id":get_member_availability_id,
                    "member_country":Members.objects.get(id=get_user_id).country,
                    "member_stake_amount": "{:,}".format(get_member_availability_details.stake_amount),
                    "member_game_type": Available_Players.objects.get(id=get_member_availability_id).game_type,
                    "member_game_link": get_member_availability_details.game_link,
                    "member_gender": get_member_availability_details.gender,
                    "member_time_available": get_member_availability_details.time_available
                }
                return JsonResponse(data)
            else:
                print(False)
                return HttpResponse(f"Unavailable")
        else:
            print(f"{player_name} not exist")
            return HttpResponse("Unavailable")





class Missed_Challenges(View):
    def get(self,request):
        if request.user.is_authenticated:
            get_user_username = request.user.username
            get_user_id = request.user.id
            get_member = Members.objects.get(id=int(get_user_id))
            if get_member.has_game:
                now = datetime.datetime.now()
                challenge_expiry_time = get_member.challenge_expiry_time
                if challenge_expiry_time > now:
                    return redirect(f"/game/game")
                else:
                    update_member = Members.objects.filter(id=get_user_id).update(
                        has_game=False,
                    )
                    return redirect("home_page")
            else:
                get_member_balance = get_member.balance
                format_member_balance = "{:,}".format(get_member_balance)
                get_member_missed_challenges = get_member.missed_challenges.all()
                update_member_has_clicked_missed_challenges = Members.objects.filter(id=get_user_id).update(
                    has_clicked_missed_challenges = True
                )
                context = {
                    "username":get_user_username,
                    "balance":format_member_balance,
                    "missed_challenges":get_member_missed_challenges
                }
                return render(request,"missed_challenges.html",context)
        else:
            return redirect("login_page")

@method_decorator(transaction.atomic,name="dispatch")
class Accept_Challenge(View):
    def post(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            challenge_id = int(request.POST["challenge_id"])
            get_challenge = Challenges.objects.get(id=challenge_id)
            challenger_username = get_challenge.challenger
            amount = get_challenge.amount
            challenge_game_type = get_challenge.challenge_game_type
            get_member = Members.objects.get(id=user_id)
            member_balance = int(get_member.balance)
            get_challenger_id = int(User.objects.select_for_update().get(username=challenger_username).id)
            check_challenger_available  = Members.objects.select_for_update().get(id=get_challenger_id).is_available
            check_challenged_available = Members.objects.select_for_update().get(id=user_id).is_available
            if not get_member.game_started:
                if check_challenged_available and check_challenger_available:
                    if member_balance >= amount:
                        get_challenge_time = Challenges.objects.select_for_update().get(id=challenge_id).time
                        additional_time = datetime.timedelta(seconds=20)
                        challenge_expiry_time = get_challenge_time + additional_time

                        #updating challenger
                        get_challenger_id = int(User.objects.get(username=challenger_username).id)
                        remove_challenger_available_players = Available_Players.objects.select_for_update().filter(username=challenger_username)
                        remove_challenger_available_players.delete()
                        update_challenger = Members.objects.select_for_update().filter(id=get_challenger_id)
                        update_challenger.update(
                            has_game = True,
                            current_opponent = request.user.username,
                            challenge_expiry_time = challenge_expiry_time,
                            is_challenger = True,
                            current_challenge_amount = amount,
                            is_available = False,
                            current_game_type = challenge_game_type
                        )

                        #update challenged
                        remove_challenged_available_players = Available_Players.objects.select_for_update().filter(
                            username=request.user.username)
                        remove_challenged_available_players.delete()
                        update_challenged = Members.objects.select_for_update().filter(id=user_id)
                        update_challenged.update(
                            has_game = True,
                            current_opponent = challenger_username,
                            challenge_expiry_time = challenge_expiry_time,
                            is_challenger = False,
                            current_challenge_amount = amount,
                            is_available = False,
                            current_game_type = challenge_game_type
                        )

                        # removing challenge
                        remove_challenge = get_member.my_challenges.remove(challenge_id)
                        return redirect("home_page")
                    else:
                        #removing challenge
                        remove_challenge = get_member.my_challenges.remove(challenge_id)
                        #deleting challenge
                    delete_challenge = Challenges.objects.filter(id=challenge_id).delete()
                    messages.error(request,f"Insufficient Balance")
                    return redirect("home_page")
                else:
                    messages.error(request,f"Connection Broken")
                    return redirect("home_page")
            else:
                return redirect("continue_game_page")
        else:
            return redirect("login_page")


@method_decorator(transaction.atomic,name="dispatch")
class Decline_Challenge(View):
    def post(self,request):
        if request.user.is_authenticated:
            challenge_id = int(request.POST["challenge_id"])

            # removing challenge
            user_id = request.user.id
            get_member = Members.objects.select_for_update().get(id=user_id)
            member_challenge = get_member.my_challenges.remove(challenge_id)

            # deleting challenge
            delete_challenge = Challenges.objects.filter(id=challenge_id).delete()
            return HttpResponse("Challenge Decline")
        else:
            return redirect("login_page")



class Game_Checker(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            get_member = Members.objects.get(id=int(user_id))
            get_member_current_game = get_member.current_game_type
            if get_member_current_game == "Golden Number":
                return redirect("/game/game")
            elif get_member_current_game == "whot":
                return redirect("/gttWhott/gttWhott")
        else:
            return redirect("home_page")


class ContinueGame(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=user_id)
            if get_member.game_started:
                if get_member.current_game_type == "Golden Number":
                    member_opponent = get_member.current_opponent
                    return redirect(f"/game/gameRoom/{username}/vs/{member_opponent}")
                elif get_member.current_game_type == "whot":
                    return redirect(f"/gttWhott/gttWhot/gameRoom")
            else:
                return redirect("home_page")
        else:
            return redirect("home_page")



class Ajax_Check_Member_Gtt_Whot_Shuffle_Cards_In_Progress(View):
    def get(self, request):
        if request.user.is_authenticated:
            user_id = request.user.id
            get_member = Members.objects.get(id=user_id)
            has_shuffled = get_member.shuffling_check
            return HttpResponse(has_shuffled)
        else:
            return redirect("login_page")

@method_decorator(transaction.atomic,name="dispatch")
class Ajax_Update_Member_Gtt_Whot_Shuffle_Cards_In_Progress(View):
    def post(self, request,challenger,challenge):
        if request.user.is_authenticated:
            user_id = request.user.id
            update_member = Members.objects.select_for_update().filter(id=int(user_id))
            update_member.update(
                shuffling_check = True
            )
            get_member_opponent_id = User.objects.select_for_update().get(username=challenge).id
            update_mem_opp = Members.objects.filter(id=int(get_member_opponent_id))
            update_mem_opp.update(
                shuffling_check =True
            )
            return HttpResponse(True)
        else:
            return redirect("login_page")









class Admin_Private_Space(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                username = request.user.username
                get_all_members = Members.objects.all()
                balance_list = []
                number_of_play = []
                admin_charges_list = []
                for i in get_all_members:
                    balance_list.append(int(i.balance))
                    number_of_play.append(int(i.number_of_play))
                    admin_charges_list.append((int(i.admin_charge)))
                total_member_balance = sum(balance_list)
                format_total_member_balance = "{:,}".format(total_member_balance)
                total_admin_chargers = sum(admin_charges_list)
                format_total_admin_charges = "{:,}".format(total_admin_chargers)
                remaining_balance = total_member_balance - total_admin_chargers
                format_remaining_balance = "{:,}".format(remaining_balance)
                total_number_of_play = sum(number_of_play)
                format_number_of_play = "{:,}".format(total_number_of_play)
                get_total_number_of_registered_members = Admin_Setup.objects.get(id=1).number_registered_members
                format_number_registered_members = "{:,}".format(get_total_number_of_registered_members)
                get_admin = Admin_Setup.objects.get(id=1)
                get_no_of_golden_number_played = int(get_admin.no_of_golden_number_played)
                get_no_of_golden_whot_played = int(get_admin.no_of_golden_Whot_played)
                get_admin_today = int(get_admin.today)
                now = d.today().day
                if get_admin_today == now:
                    get_today_no_of_games_played = int(get_admin.today_number_of_games)
                else:
                    get_today_no_of_games_played = 0
                context = {
                    "username":username,
                    "total_number_of_members":format_number_registered_members,
                    "total_number_of_play":format_number_of_play,
                    "total_member_balance":format_total_member_balance,
                    "total_admin_charges_balance":format_total_admin_charges,
                    "company_remaining_balance":format_remaining_balance,
                    "golden_number_played":"{:,}".format(get_no_of_golden_number_played),
                    "golden_whot_played":"{:,}".format(get_no_of_golden_whot_played),
                    "today_no_of_games":"{:,}".format(get_today_no_of_games_played)
                }
                return render(request,"admin_private_space.html",context)
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")


# Handling Errors

#Until time for production

def error_403(request,exception):
    return render(request,"error_403.html")

def error_404(request,exception):
    return render(request,"error_404.html")


def error_500(request):
    support_link = "https://wa.me/7019462683?text=Hi%20Please%20I%20Have%20A%20Problem"
    # send message to developer
    subject = "There is an Internal Error!!"
    message = "Hi,You need to check your server error log to fix this error ASAP!!"
    sender_email = settings.EMAIL_HOST_USER
    receiver_email = ["GoldenTwelveTransaction@gmail.com"]
    send_mail = EmailMessage(
        subject,
        message,
        sender_email,
        receiver_email
    )
    send_mail.send(fail_silently=True)
    context = {
        "support_link":support_link
    }
    return render(request,"error_500.html",context)


def sse_connection(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        username = request.user.username
        def  event_stream():
            first_n = 0
            second_n = 0
            while True:
                get_member = Members.objects.get(id=int(request.user.id))
                yield f"data:{json.dumps({'type':'first_n','username':get_member.user.username,'balance':'{:,}'.format(get_member.balance)})}\n\n"

                # real-time for member  chat
                get_member_chats = list(get_member.my_chats.order_by('date_created').values("chat_one","chat_two","date_created","id","last_message_seen","last_sender"))
                for cht in get_member_chats:
                    cht["date_created"] = cht["date_created"].isoformat()  # or use format(msg["date"], 'c') for Django formatting
                yield f"data:{json.dumps({'type': 'chats', 'chats': get_member_chats})}\n\n"


                # real time to get if user has add_notification
                get_member_notifications = get_member.notifications.all()
                for i in get_member_notifications:
                    if not i.is_seen:
                        print(f"{i.id} he never see am {i.is_seen}")
                        yield f"data:{json.dumps({'type': 'notification'})}\n\n"

                # real-time for member  chat messages
                get_member_current_chat_id = get_member.current_room_id
                if All_Chats.objects.filter(id=int(get_member_current_chat_id)).exists():
                    get_chat = All_Chats.objects.get(id=int(get_member_current_chat_id))
                    get_messages = list(get_chat.messages.values("sender","receiver","message","date"))
                    for msg in get_messages:
                        msg["date"] = msg["date"].isoformat()  # or use format(msg["date"], 'c') for Django formatting
                    yield f"data:{json.dumps({'type': 'messages', 'messages': get_messages})}\n\n"


                # real-time to get all all_available_players
                all_available_players = list(Available_Players.objects.values(
                    "username","stake_amount","win_ratio","game_link","gender",
                    "time_available","game_type","chat_link","allow_player_search",
                    "country","format_stake_amount","id"
                ))
                for avp in all_available_players:
                    avp["time_available"] = avp["time_available"].isoformat()  # or use format(msg["date"], 'c') for Django formatting
                yield f"data:{json.dumps({'type': 'available_players', 'players': all_available_players})}\n\n"


                # real-time for member challenges
                get_member_challenges = get_member.my_challenges.all()
                now = datetime.datetime.now()
                for i in get_member_challenges:
                    extra_time = datetime.timedelta(seconds=3) + i.time
                    if extra_time > now:
                        pass
                    else:
                        challenge_id = i.id
                        remove_challenge = get_member.my_challenges.remove(challenge_id)
                        add_missed_challenges = get_member.missed_challenges.add(challenge_id)
                        create_new_notification = Notifications.objects.create(
                            notification_type="Missed_Challenge",
                            notification_message = f"Player '@{i.challenger}' challenged you to a #{'{:,}'.format(i.amount)}  {i.challenge_game_type} game"
                        )
                        add_notification = get_member.notifications.add(create_new_notification)
                        update_member_has_clicked_missed_challenges = Members.objects.filter(id=user_id).update(
                            has_clicked_missed_challenges=False
                        )
                get_member_challenges = list(get_member.my_challenges.values("challenger","amount","challenge_game_type","challenged","id"))
                yield f"data:{json.dumps({'type': 'member_challenges', 'data': get_member_challenges})}\n\n"

                # Real-time for user whot game reload
                member_current_game_id = Members.objects.get(id=user_id).current_game_id
                if Gtt_Whot.objects.filter(id=member_current_game_id).exists():
                    check_game_reload = Gtt_Whot.objects.get(id=member_current_game_id).game_reload
                    if check_game_reload:
                        print("game reload")
                        yield f"data:{json.dumps({'type': 'check_member_game_reload', 'game_reload': check_game_reload})}\n\n"
                    else:
                        print("NO GAME RELOAD")



                # Real-time for user whot game timer
                member_current_game_id = Members.objects.get(id=user_id).current_game_id
                if Gtt_Whot.objects.filter(id=member_current_game_id).exists():
                    check_game_timer = Gtt_Whot.objects.get(id=member_current_game_id).game_timer
                    check_to_play = Gtt_Whot.objects.get(id=member_current_game_id).to_play
                    check_user_can_play = Gtt_Whot.objects.get(id=member_current_game_id).user_can_play
                    reload = False
                    if check_to_play == request.user.username and check_user_can_play:
                        reload = True
                    if check_game_timer >= 1:
                        new_timer = int(check_game_timer) - 1
                    else:
                        new_timer = 0
                    update_timer = Gtt_Whot.objects.filter(id=int(member_current_game_id))
                    update_timer.update(
                        game_timer=new_timer
                    )
                    yield f"data:{json.dumps({'type': 'check_member_whot_game_timer', 'game_timer': check_game_timer, 'reload':reload})}\n\n"

                # check member allow game reload
                if Gtt_Whot.objects.filter(id=member_current_game_id).exists():
                    check_to_play = Gtt_Whot.objects.get(id=member_current_game_id).to_play
                    if check_to_play == request.user.username:
                        get_member_allow_game_reload = get_member.allow_game_reload
                        yield f"data:{json.dumps({'type': 'check_allow_game_reload', 'allow_reload': get_member_allow_game_reload})}\n\n"



                #Real-time for user has game
                member_has_challenge = get_member.has_game
                if member_has_challenge:
                    print(member_has_challenge)
                    yield f"data:{json.dumps({'type':'check_member_has_game','has_game':member_has_challenge})}\n\n"




                if second_n < 100:
                    get_all_members = list(Members.objects.values("balance", "country"))
                    yield f"data:{json.dumps({'type':'second_n','data':get_all_members})}\n\n"

                yield "keep-alive\n\n"
                time.sleep(1)


        response = StreamingHttpResponse(event_stream(),content_type="text/event-stream")
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no" #for nginx (disables buffering)
        return response
    else:
        return redirect("index_page")
