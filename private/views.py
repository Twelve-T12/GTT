import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.models import User

from gttWhott.models import Gtt_Whot
from main.models import Members,Transfer_History,Game_Delay_Report,All_Phone_Numbers
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Black_List


# Create your views here.

class Get_All_Members_Info(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                get_all_members = Members.objects.all()
                context = {
                    "all_members":get_all_members
                }
                return render(request,"get_all_members_details.html",context)
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")


class Get_Member_Info(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                get_member = request.GET["get_member_username"].lower()
                if User.objects.filter(username=get_member).exists():
                    get_user = User.objects.get(username=get_member)
                    get_user_id = get_user.id
                    get_user_first_name = get_user.first_name
                    get_user_last_name = get_user.last_name
                    get_user_email = get_user.email
                    get_user_details = Members.objects.get(id=get_user_id)
                    get_user_phone_number = get_user_details.phone_number
                    get_user_whatsapp_number = "234" + get_user_phone_number[1:]
                    get_user_whatsapp_link = f"https://wa.me/{get_user_whatsapp_number}?text=Hi,%20{get_member}%20This%20Is%20Support%20From%20GTT"
                    get_user_gender = get_user_details.gender
                    get_user_balance = get_user_details.balance
                    get_user_admin_charges = get_user_details.admin_charge
                    get_user_number_of_play = get_user_details.number_of_play
                    get_user_number_of_draw = get_user_details.number_of_draw
                    get_user_number_of_win = get_user_details.number_of_win
                    get_user_number_of_loss = get_user_details.number_of_loss
                    get_user_win_ratio = get_user_details.win_ratio
                    get_user_transfer_history = get_user_details.transaction_history.all()
                    get_user_game_started = get_user_details.game_started
                    get_user_current_game_id = get_user_details.current_game_id
                    get_user_current_opponent = get_user_details.current_opponent
                    get_user_number_of_reports = get_user_details.number_of_reports

                    context = {
                        "user_id":"{:,}".format(get_user_id),
                        "user_username":get_member,
                        "user_first_name":get_user_first_name,
                        "user_last_name":get_user_last_name,
                        "user_email":get_user_email,
                        "user_whatsapp_link":get_user_whatsapp_link,
                        "user_gender":get_user_gender,
                        "user_balance":"{:,}".format(get_user_balance),
                        "user_admin_charges":"{:,}".format(get_user_admin_charges),
                        "user_number_of_play":"{:,}".format(get_user_number_of_play),
                        "user_number_of_win":"{:,}".format(get_user_number_of_win),
                        "user_number_of_draw":"{:,}".format(get_user_number_of_draw),
                        "user_number_of_loss":"{:,}".format(get_user_number_of_loss),
                        "user_win_ratio":"{:,}".format(get_user_win_ratio),
                        "user_transfer_history":get_user_transfer_history,
                        "user_game_started":get_user_game_started,
                        "user_current_game_id":get_user_current_game_id,
                        "user_current_opponent":get_user_current_opponent,
                        "user_number_of_reports":get_user_number_of_reports
                    }
                    return render(request,"get_member.html",context)
                else:
                    messages.info(request,f"{get_member} not exist")
                    return redirect("admin_private_space_page")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")



class Credit_Member(View):
    def post(self,request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                get_credit_username = request.POST["credit_username"].lower()
                get_credit_amount = int(request.POST["credit_amount"])
                format_get_credit_amount = "{:,}".format(get_credit_amount)
                get_credit_sender_name = request.POST["credit_sender_name"]
                if User.objects.filter(username=get_credit_username).exists():
                    #create credit transaction
                    get_user_id = int(User.objects.get(username=get_credit_username).id)
                    get_user = Members.objects.get(id=get_user_id)
                    get_user_balance = int(get_user.balance)
                    new_balance = get_user_balance + get_credit_amount
                    new_credit_transaction = Transfer_History.objects.create(
                        transaction_type = "Credit",
                        sender_name = get_credit_sender_name,
                        amount = "{:,}".format(get_credit_amount),
                        charges = "",
                        net_balance="{:,}".format(new_balance)
                    )
                    get_user_id = int(User.objects.get(username=get_credit_username).id)
                    get_user = Members.objects.get(id=get_user_id)
                    update_user_credit_transaction_history = get_user.transaction_history.add(new_credit_transaction)
                    get_user_balance = int(get_user.balance)
                    new_balance = get_user_balance + get_credit_amount
                    #updating user
                    update_user = Members.objects.filter(id=get_user_id).update(
                        balance = new_balance,
                        has_transfer = True
                    )
                    messages.info(request,f"{get_credit_username} Credited With #{format_get_credit_amount} Successfully!!!")
                    return redirect("admin_private_space_page")
                else:
                    messages.info(request,f"{get_credit_username} not exist")
                    return redirect("admin_private_space_page")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")




class Debit_Member(View):
    def post(self,request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                get_debit_username = request.POST["debit_username"].lower()
                get_debit_amount = int(request.POST["debit_amount"])
                format_get_debit_amount = "{:,}".format(get_debit_amount)
                get_debit_charges_amount = int(request.POST["debit_charges_amount"])
                get_debit_receiver_name = request.POST["debit_receiver_name"]
                if User.objects.filter(username=get_debit_username).exists():
                    #create debit transaction
                    get_user_id = int(User.objects.get(username=get_debit_username).id)
                    get_user = Members.objects.get(id=get_user_id)
                    get_user_balance = int(get_user.balance)
                    get_user_admin_charge = int(get_user.admin_charge)
                    new_balance = get_user_balance - get_debit_amount
                    new_admin_charge = get_user_admin_charge + get_debit_charges_amount
                    new_debit_transaction = Transfer_History.objects.create(
                        transaction_type = "Debit",
                        receiver_name = get_debit_receiver_name,
                        amount = "{:,}".format(get_debit_amount),
                        charges = "#",
                        net_balance="{:,}".format(new_balance)
                    )
                    update_user_debit_transaction = get_user.transaction_history.add(new_debit_transaction)
                    #updating user
                    update_user = Members.objects.filter(id=get_user_id).update(
                        balance = new_balance,
                        admin_charge = new_admin_charge,
                        has_transfer = True
                    )
                    messages.info(request, f"{get_debit_username} Debited With #{format_get_debit_amount} Successfully!!!")
                    return redirect("admin_private_space_page")
                else:
                    messages.info(request,f"{get_debit_username} not exist")
                    return redirect("admin_private_space_page")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")



class Admin_Help_Am_play_Gtt_Whott(View):
    def post(self,request,username="username"):
        if request.user.is_authenticated:
            username = request.POST["username"]
            user_id = User.objects.get(username=username).id
            get_member = Members.objects.get(id=int(user_id))
            member_current_game_id = get_member.current_game_id
            get_game = Gtt_Whot.objects.get(id=int(member_current_game_id))
            if get_member.game_started:
                if get_member.current_game_type == "Golden Whot":
                    if int(get_game.number_of_general_market) >= 1:
                        if not get_game.required_to_pick:
                            if get_game.to_play == username:
                                get_general_market = get_game.general_market.all()
                                list_for_gen_market = []
                                for i in get_general_market:
                                    list_for_gen_market.append(i)
                                shuffle_list_gen_market = random.shuffle(list_for_gen_market)
                                new_card_list = []
                                new_card_list.append(list_for_gen_market[0])
                                print(new_card_list)
                                # Player One Check
                                if get_game.player_one == username:
                                    for i in new_card_list:
                                        new_card_player_one = get_game.player_one_cards.add(i)
                                        remove_card_general_market = get_game.general_market.remove(i)
                                    new_no_player_one_cards = int(get_game.player_one_number_of_cards) + 1
                                    new_no_general_market = int(get_game.number_of_general_market) - 1
                                    update_player_one = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                                        number_of_general_market = new_no_general_market,
                                        player_one_number_of_cards = new_no_player_one_cards,
                                        to_play = get_member.current_opponent,
                                        game_reload = True,
                                        hold_on = False
                                    )
                                    update_member = Members.objects.filter(id=int(user_id)).update(
                                        current_number_of_whott_cards = new_no_player_one_cards
                                    )
                                # Player Two Check
                                if get_game.player_two == username:
                                    for i in new_card_list:
                                        new_card_player_one = get_game.player_two_cards.add(i)
                                        remove_card_general_market = get_game.general_market.remove(i)
                                    new_no_player_two_cards = int(get_game.player_two_number_of_cards) + 1
                                    new_no_general_market = int(get_game.number_of_general_market) - 1
                                    update_player_one = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                                        number_of_general_market = new_no_general_market,
                                        player_two_number_of_cards = new_no_player_two_cards,
                                        to_play = get_member.current_opponent,
                                        game_reload = True,
                                        hold_on = False
                                    )
                                    update_member = Members.objects.filter(id=int(user_id)).update(
                                        current_number_of_whott_cards = new_no_player_two_cards
                                    )
                                messages.info(request,f"Successfully Played For: {username}")
                                return redirect("admin_private_space_page")
                            else:
                                return HttpResponse("Not Your Turn")
                        else:
                            return redirect(f"/private/adminHelpAmPlayGttWhott/{username}")
                    else:
                        check_get_game = Gtt_Whot.objects.get(id=int(member_current_game_id))
                        check_player_one_number_of_cards = int(
                            check_get_game.player_one_number_of_cards)
                        check_player_two_number_of_cards = int(
                            check_get_game.player_two_number_of_cards)
                        check_number_of_general_market = int(
                            check_get_game.number_of_general_market)
                        if check_player_one_number_of_cards == 0 and check_player_two_number_of_cards >= 1:
                            update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                                user_can_play = False,
                                player_won = True,
                                game_winner = get_game.player_one,
                                game_reload = True,
                                hold_on = False
                            )
                        elif check_player_two_number_of_cards == 0  and check_player_one_number_of_cards >= 1:
                            update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                                user_can_play = False,
                                player_won=True,
                                game_winner=get_game.player_two,
                                game_reload= True,
                                hold_on = False
                            )
                        elif check_number_of_general_market == 0 and check_player_one_number_of_cards >= 1 and check_player_two_number_of_cards >= 1:
                            update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                                user_can_play = False,
                                has_tie = True,
                                game_reload =True,
                                hold_on = False
                            )
                        return redirect(f"/private/adminHelpAmPlayGttWhott/{username}")
                else:
                    return redirect("home_page")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")

    def get(self,request,username):
        if request.user.is_authenticated:
            user_id = User.objects.get(username=username).id
            get_member = Members.objects.get(id=int(user_id))
            member_current_game_id = get_member.current_game_id
            get_game = Gtt_Whot.objects.get(id=int(member_current_game_id))
            if get_member.game_started:
                if get_member.current_game_type == "Golden Whot":
                    if get_game.required_to_pick:
                        get_game_player_required_to_pick = get_game.player_required_to_pick
                        get_game_how_many_required_to_pick = get_game.how_many_required_to_pick
                        if int(get_game_how_many_required_to_pick) == 2:
                            get_general_market = get_game.general_market.all()
                            list_for_gen_market = []
                            if int(get_game_how_many_required_to_pick) == 2:
                                if int(get_game.number_of_general_market) != 1:
                                    if int(get_game.number_of_general_market) != 0:
                                        for i in get_general_market:
                                            list_for_gen_market.append(i)
                                        shuffle_list_gen_market = random.shuffle(list_for_gen_market)
                                        new_card_list = []
                                        for i in range(2):
                                            new_card_list.append(list_for_gen_market[i])
                                        if username == get_game_player_required_to_pick and get_game_player_required_to_pick == get_game.player_one:
                                            #updating player one and general market
                                            for i in new_card_list:
                                                get_game.player_one_cards.add(i.id)
                                                get_game.general_market.remove(i.id)
                                            new_no_of_general_market = int(get_game.number_of_general_market) - 2
                                            new_player_one_no_of_cards = int(get_game.player_one_number_of_cards) + 2
                                            update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                                                number_of_general_market = new_no_of_general_market,
                                                player_one_number_of_cards = new_player_one_no_of_cards,
                                                to_play = get_member.current_opponent,
                                                game_reload = True,
                                                required_to_pick = False,
                                                hold_on= False
                                            )
                                            update_member = Members.objects.filter(id=int(user_id)).update(
                                                current_number_of_whott_cards = new_player_one_no_of_cards
                                            )
                                            return redirect("admin_private_space_page")
                                        elif username == get_game_player_required_to_pick and get_game_player_required_to_pick == get_game.player_two:
                                            # updating player two and general market
                                            for i in new_card_list:
                                                get_game.player_two_cards.add(i.id)
                                                get_game.general_market.remove(i.id)
                                            new_no_of_general_market = int(get_game.number_of_general_market) - 2
                                            new_player_two_no_of_cards = int(get_game.player_two_number_of_cards) + 2
                                            update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                                                number_of_general_market=new_no_of_general_market,
                                                player_two_number_of_cards=new_player_two_no_of_cards,
                                                to_play=get_member.current_opponent,
                                                game_reload=True,
                                                required_to_pick=False,
                                                hold_on=False
                                            )
                                            update_member = Members.objects.filter(id=int(user_id)).update(
                                                current_number_of_whott_cards=new_player_two_no_of_cards
                                            )
                                            return redirect("admin_private_space_page")
                                    else:
                                        for i in get_general_market:
                                            list_for_gen_market.append(i)
                                        shuffle_list_gen_market = random.shuffle(list_for_gen_market)
                                        new_card_list = []
                                        for i in range(1):
                                            new_card_list.append(list_for_gen_market[i])
                                        if username == get_game_player_required_to_pick and get_game_player_required_to_pick == get_game.player_one:
                                            #updating player one and general market
                                            for i in new_card_list:
                                                get_game.player_one_cards.add(i.id)
                                                get_game.general_market.remove(i.id)
                                            new_no_of_general_market = int(get_game.number_of_general_market) - 1
                                            new_player_one_no_of_cards = int(get_game.player_one_number_of_cards) + 1
                                            update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                                                number_of_general_market = new_no_of_general_market,
                                                player_one_number_of_cards = new_player_one_no_of_cards,
                                                to_play = get_member.current_opponent,
                                                game_reload = True,
                                                required_to_pick = False,
                                                has_tie = True,
                                                user_can_play = False,
                                                hold_on = False
                                            )
                                            update_member = Members.objects.filter(id=int(user_id)).update(
                                                current_number_of_whott_cards = new_player_one_no_of_cards
                                            )
                                            return redirect("admin_private_space_page")
                                        elif username == get_game_player_required_to_pick and get_game_player_required_to_pick == get_game.player_two:
                                            # updating player two and general market
                                            for i in new_card_list:
                                                get_game.player_two_cards.add(i.id)
                                                get_game.general_market.remove(i.id)
                                            new_no_of_general_market = int(get_game.number_of_general_market) - 1
                                            new_player_two_no_of_cards = int(get_game.player_two_number_of_cards) + 1
                                            update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                                                number_of_general_market=new_no_of_general_market,
                                                player_two_number_of_cards=new_player_two_no_of_cards,
                                                to_play=get_member.current_opponent,
                                                game_reload=True,
                                                required_to_pick=False,
                                                has_tie = True,
                                                user_can_play = False,
                                                hold_on = False
                                            )
                                            update_member = Members.objects.filter(id=int(user_id)).update(
                                                current_number_of_whott_cards=new_player_two_no_of_cards
                                            )
                                        return redirect("admin_private_space_page")
                                else:
                                    for i in get_general_market:
                                        list_for_gen_market.append(i)
                                    shuffle_list_gen_market = random.shuffle(list_for_gen_market)
                                    new_card_list = []
                                    for i in range(1):
                                        new_card_list.append(list_for_gen_market[i])
                                    if username == get_game_player_required_to_pick and get_game_player_required_to_pick == get_game.player_one:
                                        #updating player one and general market
                                        for i in new_card_list:
                                            get_game.player_one_cards.add(i.id)
                                            get_game.general_market.remove(i.id)
                                        new_no_of_general_market = int(get_game.number_of_general_market) - 1
                                        new_player_one_no_of_cards = int(get_game.player_one_number_of_cards) + 1
                                        update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                                            number_of_general_market = new_no_of_general_market,
                                            player_one_number_of_cards = new_player_one_no_of_cards,
                                            to_play = get_member.current_opponent,
                                            game_reload = True,
                                            required_to_pick = False,
                                            has_tie = True,
                                            user_can_play = False,
                                            hold_on = False
                                        )
                                        update_member = Members.objects.filter(id=int(user_id)).update(
                                            current_number_of_whott_cards = new_player_one_no_of_cards
                                        )
                                        return redirect("admin_private_space_page")
                                    elif username == get_game_player_required_to_pick and get_game_player_required_to_pick == get_game.player_two:
                                        # updating player two and general market
                                        for i in new_card_list:
                                            get_game.player_two_cards.add(i.id)
                                            get_game.general_market.remove(i.id)
                                        new_no_of_general_market = int(get_game.number_of_general_market) - 1
                                        new_player_two_no_of_cards = int(get_game.player_two_number_of_cards) + 1
                                        update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                                            number_of_general_market=new_no_of_general_market,
                                            player_two_number_of_cards=new_player_two_no_of_cards,
                                            to_play=get_member.current_opponent,
                                            game_reload=True,
                                            required_to_pick=False,
                                            has_tie = True,
                                            user_can_play = False,
                                            hold_on = False
                                        )
                                        update_member = Members.objects.filter(id=int(user_id)).update(
                                            current_number_of_whott_cards=new_player_two_no_of_cards
                                        )
                                    return redirect("admin_private_space_page")
                            return redirect("admin_private_space_page")
                        elif int(get_game_how_many_required_to_pick) == 1:
                            get_general_market = get_game.general_market.all()
                            list_for_gen_market = []
                            for i in get_general_market:
                                list_for_gen_market.append(i)
                            shuffle_list_gen_market = random.shuffle(list_for_gen_market)
                            new_card_list = []
                            for i in range(1):
                                new_card_list.append(list_for_gen_market[i])
                            if username == get_game_player_required_to_pick and get_game_player_required_to_pick == get_game.player_one:
                                # updating player one and general market
                                for i in new_card_list:
                                    get_game.player_one_cards.add(i.id)
                                    get_game.general_market.remove(i.id)
                                new_no_of_general_market = int(get_game.number_of_general_market) - 1
                                new_player_one_no_of_cards = int(get_game.player_one_number_of_cards) + 1
                                update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                                    number_of_general_market=new_no_of_general_market,
                                    player_one_number_of_cards=new_player_one_no_of_cards,
                                    to_play=get_member.current_opponent,
                                    game_reload=True,
                                    required_to_pick=False,
                                    hold_on = False
                                )
                                update_member = Members.objects.filter(id=int(user_id)).update(
                                    current_number_of_whott_cards=new_player_one_no_of_cards
                                )
                                return redirect("admin_private_space_page")
                            elif username == get_game_player_required_to_pick and get_game_player_required_to_pick == get_game.player_two:
                                # updating player two and general market
                                for i in new_card_list:
                                    get_game.player_two_cards.add(i.id)
                                    get_game.general_market.remove(i.id)
                                new_no_of_general_market = int(get_game.number_of_general_market) - 1
                                new_player_two_no_of_cards = int(get_game.player_two_number_of_cards) + 1
                                update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                                    number_of_general_market=new_no_of_general_market,
                                    player_two_number_of_cards=new_player_two_no_of_cards,
                                    to_play=get_member.current_opponent,
                                    game_reload=True,
                                    required_to_pick=False,
                                    hold_on = False
                                )
                                update_member = Members.objects.filter(id=int(user_id)).update(
                                    current_number_of_whott_cards=new_player_two_no_of_cards
                                )
                                return redirect("admin_private_space_page")
                            return redirect("admin_private_space_page")
                    else:
                        return redirect("admin_private_space_page")
                else:
                    return redirect("home_page")
            else:
                return redirect("home_page")
        else:
            return redirect("home_page")






class Send_General_Mail(View):
    def post(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                subject = request.POST["general_mail_subject"]
                message = request.POST["general_mail_message"]
                get_all_users = User.objects.all()
                email_list = []
                for i in get_all_users:
                    email_list.append(i.email)
                sender_email = settings.EMAIL_HOST_USER
                # sending mail
                send_mail = EmailMessage(
                    subject,
                    message,
                    sender_email,
                    email_list
                )
                send_mail.send(fail_silently=True)
                messages.info(request,f"General Mail Sent Successfully")
                return redirect("admin_private_space_page")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")



class Send_Private_Mail(View):
    def post(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                receiver = request.POST["receiver_private_mail"].lower()
                subject = request.POST["private_mail_subject"]
                message = request.POST["private_mail_message"]
                if User.objects.filter(username=receiver).exists():
                    user_email = User.objects.get(username=receiver).email
                    sender_email = settings.EMAIL_HOST_USER
                    # sending mail
                    send_mail = EmailMessage(
                        subject,
                        message,
                        sender_email,
                        [user_email]
                    )
                    send_mail.send(fail_silently=True)
                    messages.info(request, f"Private Mail Sent Successfully")
                    return redirect("admin_private_space_page")
                else:
                    messages.info(request,f"{receiver} not exist")
                    return redirect("admin_private_space_page")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")

class All_Black_List_Members(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                get__all_blacklist = Black_List.objects.all()
                context = {
                    "blacklist":get__all_blacklist
                }
                return render(request,"blacklist.html",context)
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")

class Add_Member_Black_List(View):
    def post(self,request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                get_username = request.POST["username"].lower()
                get_reason = request.POST["reason"]
                if User.objects.filter(username=get_username).exists():
                    # creating new black list
                    new_black_list = Black_List.objects.create(
                        username=get_username,
                        reason=get_reason
                    )
                    get_member_id = User.objects.get(username=get_username).id
                    # update user is_blacklisted
                    update_user_is_blacklisted = Members.objects.filter(id=int(get_member_id)).update(
                        is_blacklisted=True
                    )
                    messages.info(request, f"'{get_username}' is blacklisted successfully!!!")
                    return redirect("admin_private_space_page")
                else:
                    messages.info(request, f"'{get_username}' Not Available!!!")
                    return redirect("admin_private_space_page")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")


class Remove_Member_Black_List(View):
    def get(self,request,id,username):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                blacklist_id = int(id)
                #deleting black list
                delete_member_blacklist = Black_List.objects.filter(id=blacklist_id).delete()
                #updating member blacklist
                get_member_id = User.objects.get(username=username).id
                update_member_blacklist = Members.objects.filter(id=int(get_member_id)).update(
                    is_blacklisted = False
                )
                messages.info(request,f"'{username}' removed successfully!")
                return redirect("blacklist_page")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")



class Admin_Get_Game_Delay_Report(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                get_delay_reports = Game_Delay_Report.objects.all()
                context = {
                    "game_reports":get_delay_reports
                }
                return render(request, "admin_get_delay_report.html",context)
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")



class Admin_Remove_Member_Get_Game_Delay_Report(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                get_delay_reports = Game_Delay_Report.objects.filter(id=int(id)).delete()
                messages.info(request, f" removed successfully!")
                return redirect("admin_get_game_delay_report_page")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")


class Admin_Quick_Add_Members_Phone_Numbers(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                get_members = Members.objects.all()
                for i in get_members:
                    if not All_Phone_Numbers.objects.filter(phone_number=i.phone_number).exists():
                        append_phone_number = All_Phone_Numbers.objects.create(
                            username = i.user,
                            phone_number = i.phone_number
                        )
                    else:
                        print("phone number dey there before!")
                messages.info(request,f"completed!")
                return redirect("admin_private_space_page")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")