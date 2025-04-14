from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth.models import User
from main.models import Members, Admin_Setup, Transfer_History, Game_Delay_Report
from .models import GTT
import random
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import datetime
# Create your views here.


class Game(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=user_id)
            member_has_game = get_member.has_game
            member_opponent = get_member.current_opponent
            member_started_game = get_member.game_started
            if member_has_game:
                if not member_started_game:
                    member_is_challenger = get_member.is_challenger
                    challenge_amount = int(get_member.current_challenge_amount)
                    potential_wining_amount = int(challenge_amount * 2)
                    format_challenge_amount = "{:,}".format(challenge_amount)
                    context = {
                        "is_challenger":member_is_challenger,
                        "opponent":member_opponent,
                        "format_amount":format_challenge_amount,
                        "potential_wining":"{:,}".format(potential_wining_amount),
                        "amount":challenge_amount,
                        "username":username
                    }
                    return render(request,"game_preview.html",context)
                else:
                    return redirect(f"/game/gameRoom/{username}/vs/{member_opponent}")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")


class Start_Game(View):
    def get(self,request,amount):
        if request.user.is_authenticated:
            user_id = request.user.id
            get_member = Members.objects.get(id=user_id)
            get_member_balance = int(get_member.balance)
            mem_opp = get_member.current_opponent
            mem_opp_id = int(User.objects.get(username=mem_opp).id)
            get_member_opp_balance = int(Members.objects.get(id=mem_opp_id).balance)
            get_admin = Admin_Setup.objects.get(id=1)
            if Members.objects.get(id=mem_opp_id).current_opponent == request.user.username and get_member.current_opponent == mem_opp:
                if get_member_balance >= int(amount) and get_member_opp_balance >= int(amount):
                    if get_member.has_game:
                        if not Members.objects.get(id=mem_opp_id).game_started:
                            game_wining_price = int(int(amount) * 2)
                            if int(amount) <= 1000:
                                min_admin_charges = int(get_admin.min_game_charges)
                                new_game = GTT.objects.create(
                                    game_amount = int(amount),
                                    player_one = request.user.username,
                                    player_two =  get_member.current_opponent,
                                    to_send = request.user.username,
                                    to_receive = get_member.current_opponent,
                                    game_charges = min_admin_charges,
                                    game_wining_amount = game_wining_price
                                )
                            else:
                                max_game_charges = int(get_admin.max_game_charges)
                                new_game = GTT.objects.create(
                                    game_amount = int(amount),
                                    player_one = request.user.username,
                                    player_two = get_member.current_opponent,
                                    to_send = request.user.username,
                                    to_receive=get_member.current_opponent,
                                    game_charges = max_game_charges,
                                    game_wining_amount = game_wining_price
                                )
                            new_golden_number_no_of_play = int(get_admin.no_of_golden_number_played) + 1
                            update_admin = Admin_Setup.objects.filter(id=1).update(
                                no_of_golden_number_played=int(new_golden_number_no_of_play)
                            )
                            game_id = GTT.objects.get(player_one=request.user.username).id
                            create_debit_transaction_member = Transfer_History.objects.create(
                                transaction_type = "Debit",
                                receiver_name = f"Golden Number Challenge With '{get_member.current_opponent}'",
                                amount = "{:,}".format(int(amount)),
                                charges  = ""
                            )
                            #member players info
                            new_member_balance = get_member.balance - int(amount)
                            member_number_of_play = int(get_member.number_of_play)
                            new_member_number_of_play = member_number_of_play + 1
                            member_debit_transaction = get_member.transaction_history.add(create_debit_transaction_member)
                            update_member = Members.objects.filter(id=user_id).update(
                                balance=new_member_balance,
                                number_of_play=new_member_number_of_play,
                                game_started=True,
                                current_game_id=game_id,
                                has_transfer=True,
                                current_game_wining_amount = game_wining_price
                            )
                            #updating member-opponent info
                            create_debit_transaction_opponent = Transfer_History.objects.create(
                                transaction_type="Debit",
                                receiver_name=f"Golden Number Challenge With '{request.user.username}'",
                                amount="{:,}".format(int(amount)),
                                charges=""
                            )
                            member_opponent = get_member.current_opponent
                            get_opponent_id = int(User.objects.get(username=member_opponent).id)
                            get_opponent = Members.objects.get(id=get_opponent_id)
                            get_opponent_balance = get_opponent.balance
                            get_opponent_number_of_play = get_opponent.number_of_play
                            new_opponent_number_of_play = get_opponent_number_of_play + 1
                            opponent_debit_transaction = get_opponent.transaction_history.add(create_debit_transaction_opponent)
                            new_opponent_balance = get_opponent_balance - int(amount)
                            update_opponent = Members.objects.filter(id=get_opponent_id).update(
                                balance=new_opponent_balance,
                                number_of_play = new_opponent_number_of_play,
                                game_started=True,
                                current_game_id=game_id,
                                has_transfer=True,
                                current_game_wining_amount=game_wining_price
                            )
                            # updating today number of games play
                            today = datetime.today().day
                            get_admin = Admin_Setup.objects.get(id=1)
                            get_admin_today = int(get_admin.today)
                            if today == get_admin_today:
                                new_today_games = int(get_admin.today_number_of_games) + 1
                                update_today_games = Admin_Setup.objects.filter(id=1).update(
                                    today_number_of_games=new_today_games,
                                )
                            else:
                                update_today = Admin_Setup.objects.filter(id=1).update(
                                    today=today,
                                    today_number_of_games=1
                                )
                            return redirect("game_page")
                        else:
                            messages.info(request,f"{mem_opp} already in another game")
                            return redirect("home_page")
                    else:
                        return redirect("home_page")
                else:
                    messages.info(request,f"Can't Continue")
                    return redirect("home_page")
            else:
                messages.info(request,f"User Connected To Another Game")
                return redirect("home_page")
        else:
            return redirect("login_page")


class Check_Start_Game(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            check_member_started_game = Members.objects.get(id=user_id).game_started
            return HttpResponse(check_member_started_game)
        else:
            return redirect("login_page")


class Continue_Game(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=user_id)
            if get_member.game_started:
                if get_member.current_game_type == "Golden Number":
                    member_opponent = get_member.current_opponent
                    return redirect(f"/game/gameRoom/{username}/vs/{member_opponent}")
                elif get_member.current_game_type == "Golden Whot":
                    return redirect(f"/gttWhott/gttWhot/gameRoom")
            else:
                return redirect("home_page")
        else:
            return redirect("home_page")


class Game_Room(View):
    def get(self,request,user,opponent):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=user_id)
            if get_member.game_started:
                get_member = Members.objects.get(id=user_id)
                member_opponent = get_member.current_opponent
                member_game_id = int(get_member.current_game_id)
                get_game = GTT.objects.get(id=member_game_id)
                game_amount = get_game.game_amount
                game_has_tie = get_game.has_tie
                game_has_finished = get_game.has_finished
                get_result_collated = get_game.result_collated
                format_game_amount = "{:,}".format(game_amount)
                game_round = get_game.game_round
                member_opponent_id_for_phone_number = int(User.objects.get(username=member_opponent).id)
                get_member_opponent_phone_number = Members.objects.get(id=member_opponent_id_for_phone_number).phone_number
                member_opponent_whatsapp_number = "234" + get_member_opponent_phone_number[1:]
                member_opponent_whatsapp_link = f"https://wa.me/{member_opponent_whatsapp_number}?text=Hi,%20My%20Name%20Is%20{request.user.username},%20I%20Am%20An%20Opponent%20From%20GTT..."
                if int(game_round) <= 4 or not game_has_finished:
                    game_player_one = get_game.player_one
                    game_player_one_count = get_game.player_one_count
                    game_player_two = get_game.player_two
                    game_player_two_count = get_game.player_two_count
                    potential_wining_amount = int(get_game.game_wining_amount)
                    get_to_send = get_game.to_send
                    get_has_sent = get_game.has_sent
                    get_has_received = get_game.has_received
                    get_receiver_receiver_number = get_game.receiver_number
                    get_to_receive = get_game.to_receive
                    get_sign = get_game.current_game_sign
                    get_first_number = get_game.current_first_number
                    get_second_number = get_game.current_second_number
                    get_golden_number = get_game.current_golden_number
                    get_random_number = get_game.current_random_number
                    get_second_random_number = get_game.current_second_random_number
                    get_third_random_number = get_game.current_third_random_number
                    all_numbers = [get_first_number,get_second_number,get_golden_number,get_random_number,get_second_random_number,get_third_random_number]
                    shuffle_all_numbers = random.shuffle(all_numbers)
                    shuffle_first_number = all_numbers[0]
                    shuffle_second_number = all_numbers[1]
                    shuffle_third_number = all_numbers[2]
                    shuffle_fourth_number = all_numbers[3]
                    shuffle_fifth_number = all_numbers[4]
                    shuffle_sixth_number = all_numbers[5]
                    get_game_has_tie = get_game.has_tie
                    get_game_has_finished = get_game.has_finished
                    get_found_a_winner = get_game.not_found_winner
                    get_game_winner = get_game.game_winner
                    context = {
                        "opponent":member_opponent,
                        "format_game_amount":format_game_amount,
                        "round":game_round,
                        "player_one":game_player_one,
                        "player_one_count":game_player_one_count,
                        "player_two":game_player_two,
                        "player_two_count":game_player_two_count,
                        "potential_wining":"{:,}".format(potential_wining_amount),
                        "sender":get_to_send,
                        "has_sent":get_has_sent,
                        "sender_first_number":get_first_number,
                        "sender_second_number":get_second_number,
                        "sender_golden_number":get_golden_number,
                        "sender_random_number":get_random_number,
                        "sender_second_random_number":get_second_random_number,
                        "sender_third_random_number":get_third_random_number,
                        "has_received":get_has_received,
                        "receiver":get_to_receive,
                        "first_number":shuffle_first_number,
                        "second_number":shuffle_second_number,
                        "third_number":shuffle_third_number,
                        "fourth_number":shuffle_fourth_number,
                        "fifth_number":shuffle_fifth_number,
                        "sixth_number":shuffle_sixth_number,
                        "sign":get_sign,
                        "check_first_number":get_first_number,
                        "check_second_number":get_second_number,
                        "receiver_number":get_receiver_receiver_number,
                        "golden_number":get_golden_number,
                        "game_tie":get_game_has_tie,
                        "game_finished":get_game_has_finished,
                        "found_a_winner":get_found_a_winner,
                        "winner":get_game_winner,
                        "opponent_whatsapp_link":member_opponent_whatsapp_link
                    }
                    return render(request, "game_room.html",context)
                else:
                    get_player_one = get_game.player_one
                    get_player_two = get_game.player_two
                    get_player_one_count = int(get_game.player_one_count)
                    get_player_two_count = int(get_game.player_two_count)
                    if get_player_one_count > get_player_two_count and not get_result_collated:
                        update_game = GTT.objects.filter(id=member_game_id).update(
                            has_finished = False,
                            not_found_winner=False,
                            game_winner = get_game.player_one,
                            result_collated = True
                        )
                        #crediting and debiting winner player_one
                        get_player_one_id = int(User.objects.get(username=get_player_one).id)
                        #create credit transaction
                        new_credit_transaction = Transfer_History.objects.create(
                            transaction_type = 'Credit',
                            sender_name = f"Winning '{get_player_two}' Golden Number",
                            amount = "{:,}".format(get_game.game_wining_amount),
                            charges = ""
                        )
                        get_member = Members.objects.get(id=get_player_one_id)
                        update_member_credit_transaction = get_member.transaction_history.add(new_credit_transaction)
                        #create debit transaction
                        new_debit_transaction = Transfer_History.objects.create(
                            transaction_type='Debit',
                            receiver_name=f"Winning Golden Number '{get_player_two}' Game charges",
                            amount="{:,}".format(get_game.game_charges),
                            charges=""
                        )
                        update_member_debit_transaction = get_member.transaction_history.add(new_debit_transaction)
                        #updating user balance
                        get_member_balance = int(get_member.balance)
                        get_member_admin_charge = int(get_member.admin_charge)
                        new_member_admin_charge = get_member_admin_charge + int(get_game.game_charges)
                        get_member_number_win = int(get_member.number_of_win)
                        new_win = get_member_number_win + 1
                        new_balance = get_member_balance + int(get_game.game_wining_amount) - int(get_game.game_charges)
                        update_player_one_balance = Members.objects.filter(id=get_player_one_id).update(
                            balance = new_balance,
                            number_of_win = new_win,
                            admin_charge = new_member_admin_charge
                        )
                        #get and update opponent loss
                        get_member_opponent_id = int(User.objects.get(username=get_member.current_opponent).id)
                        member_opponent_loss = int(Members.objects.get(id=get_member_opponent_id).number_of_loss)
                        new_opponent_loss = member_opponent_loss + 1
                        update_member_opponent_loss = Members.objects.filter(id=get_member_opponent_id).update(
                            number_of_loss = new_opponent_loss
                        )
                        return redirect(f"/game/gameRoom/{username}/vs/{member_opponent}")
                    elif get_player_two_count > get_player_one_count and not get_result_collated:
                        update_game = GTT.objects.filter(id=member_game_id).update(
                            has_finished=False,
                            not_found_winner=False,
                            game_winner = get_game.player_two,
                            result_collated =True
                        )
                        # crediting and debiting winner player_one
                        get_player_two_id = int(User.objects.get(username=get_player_two).id)
                        # create credit transaction
                        new_credit_transaction = Transfer_History.objects.create(
                            transaction_type='Credit',
                            sender_name=f"Winning '{get_player_one}' Golden Number",
                            amount="{:,}".format(get_game.game_wining_amount),
                            charges=""
                        )
                        get_member = Members.objects.get(id=get_player_two_id)
                        update_member_credit_transaction = get_member.transaction_history.add(new_credit_transaction)
                        # create debit transaction
                        new_debit_transaction = Transfer_History.objects.create(
                            transaction_type='Debit',
                            receiver_name=f"Winning Golden Number '{get_player_one}' Game charges",
                            amount="{:,}".format(get_game.game_charges),
                            charges=""
                        )
                        update_member_debit_transaction = get_member.transaction_history.add(new_debit_transaction)
                        # updating user balance
                        get_member_balance = int(get_member.balance)
                        get_member_admin_charge = int(get_member.admin_charge)
                        new_member_admin_charge = get_member_admin_charge + int(get_game.game_charges)
                        get_member_number_win = int(get_member.number_of_win)
                        new_win = get_member_number_win + 1
                        new_balance = get_member_balance + int(get_game.game_wining_amount) - int(get_game.game_charges)
                        update_player_one_balance = Members.objects.filter(id=get_player_two_id).update(
                            balance=new_balance,
                            number_of_win=new_win,
                            admin_charge = new_member_admin_charge
                        )
                        # get and update opponent loss
                        get_member_opponent_id = int(User.objects.get(username=get_member.current_opponent).id)
                        member_opponent_loss = int(Members.objects.get(id=get_member_opponent_id).number_of_loss)
                        new_opponent_loss = member_opponent_loss + 1
                        update_member_opponent_loss = Members.objects.filter(id=get_member_opponent_id).update(
                            number_of_loss=new_opponent_loss
                        )
                        return redirect(f"/game/gameRoom/{username}/vs/{member_opponent}")
                    elif get_player_two_count == get_player_one_count and not get_result_collated:
                        update_game = GTT.objects.filter(id=member_game_id).update(
                            has_finished=False,
                            has_tie = True,
                            result_collated = True
                        )
                        get_game_amount = int(get_game.game_amount)
                        get_game_charges = int(get_game.game_charges)
                        each_player_charges = int(get_game_charges/2)
                        #update member
                        member_balance = int(get_member.balance)
                        member_number_of_draw = int(get_member.number_of_draw)
                        member_admin_charge = int(get_member.admin_charge)
                        #players balance
                        players_new_balance = get_game_amount - each_player_charges
                        new_member_admin_charges = member_admin_charge + each_player_charges
                        #create member credit transaction
                        new_member_draw_credit_transaction = Transfer_History.objects.create(
                            transaction_type = "Credit",
                            sender_name = f"Draw Golden Number with '{member_opponent}'",
                            amount = "{:,}".format(get_game_amount),
                            charges = ""
                        )
                        update_member_credit_transaction = get_member.transaction_history.add(new_member_draw_credit_transaction)
                        # create member debit transaction
                        new_member_draw_debit_transaction = Transfer_History.objects.create(
                            transaction_type = "Debit",
                            receiver_name = f"Draw Golden Number with '{member_opponent}' Game charges",
                            amount = "{:,}".format(each_player_charges),
                            charges = ""
                        )
                        update_member_debit_transaction = get_member.transaction_history.add(new_member_draw_debit_transaction)
                        new_member_balance = member_balance + players_new_balance
                        update_member = Members.objects.filter(id=user_id).update(
                            balance = new_member_balance,
                            number_of_draw = int(member_number_of_draw + 1),
                            admin_charge = new_member_admin_charges
                        )
                        #####################################
                        #update member_opponent
                        member_opponent_id = int(User.objects.get(username=member_opponent).id)
                        member_opponent = Members.objects.get(id=member_opponent_id)
                        member_opponent_balance = int(member_opponent.balance)
                        member_opponent_number_of_draw = int(member_opponent.number_of_draw)
                        member_opponent_admin_charges = int(member_opponent.admin_charge)
                        new_member_opponent_admin_charges = member_opponent_admin_charges + each_player_charges
                        #create member_opponent credit transaction
                        new_member_opponent_draw_credit_transaction = Transfer_History.objects.create(
                            transaction_type="Credit",
                            sender_name=f"Draw Golden Number with '{username}'",
                            amount="{:,}".format(get_game_amount),
                            charges=""
                        )
                        update_member_opponent_credit_transaction = member_opponent.transaction_history.add(new_member_opponent_draw_credit_transaction)
                        # create member_opponent debit transaction
                        new_member_opponent_draw_debit_transaction = Transfer_History.objects.create(
                            transaction_type="Debit",
                            receiver_name=f"Draw with Golden Number '{username}' charges",
                            amount="{:,}".format(each_player_charges),
                            charges=""
                        )
                        update_member_opponent_debit_transaction = member_opponent.transaction_history.add(new_member_opponent_draw_debit_transaction)
                        new_member_opponent_balance = member_opponent_balance + players_new_balance
                        update_member_opponent = Members.objects.filter(id=member_opponent_id).update(
                            balance=new_member_opponent_balance,
                            number_of_draw=int(member_opponent_number_of_draw + 1),
                            admin_charge=new_member_opponent_admin_charges
                        )
                        return redirect(f"/game/gameRoom/{username}/vs/{member_opponent}")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")


class Sender_Numbers_Collation(View):
    def post(self,request):
        if request.user.is_authenticated:
            #getting numbers
            get_first_number = int(float((request.POST["sender_first_number"])))
            get_sign = request.POST["sender_sign"]
            get_second_number = int(float(request.POST["sender_second_number"]))
            get_sender_golden_number = int(float(request.POST["sender_golden_number"]))
            get_sender_random_number = int(float(request.POST["sender_random_number"]))
            get_sender_second_random_number = int(float(request.POST["sender_second_random_number"]))
            get_sender_third_random_number = int(float(request.POST["sender_third_random_number"]))
            #getting member details
            username = request.user.username
            user_id = request.user.id
            get_member = Members.objects.get(id=user_id)
            if get_member.game_started:
                member_opponent = get_member.current_opponent
                member_current_game_id = int(get_member.current_game_id)
                #updating member current game
                update_member_current_game = GTT.objects.filter(id=member_current_game_id).update(
                    current_first_number = get_first_number,
                    current_game_sign = get_sign,
                    current_second_number = get_second_number,
                    current_golden_number = get_sender_golden_number,
                    current_random_number = get_sender_random_number,
                    current_second_random_number = get_sender_second_random_number,
                    current_third_random_number = get_sender_third_random_number,
                    has_sent = True,
                    game_reload = True
                )
                return redirect(f"/game/gameRoom/{username}/vs/{member_opponent}")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")

class First_Number(View):
    def post(self,request):
        if request.user.is_authenticated:
            get_receiver_first_number = int(request.POST["receiver_first_number"])
            username = request.user.username
            user_id = request.user.id
            get_member = Members.objects.get(id=user_id)
            if get_member.game_started:
                member_opponent = get_member.current_opponent
                get_member_current_game_id = int(get_member.current_game_id)
                update_game = GTT.objects.filter(id=get_member_current_game_id).update(
                    has_received = True,
                    receiver_number = get_receiver_first_number,
                    game_reload=True
                )
                return redirect(f"/game/gameRoom/{username}/vs/{member_opponent}")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")

class Second_Number(View):
    def post(self,request):
        if request.user.is_authenticated:
            get_receiver_second_number = int(request.POST["receiver_second_number"])
            username = request.user.username
            user_id = request.user.id
            get_member = Members.objects.get(id=user_id)
            if get_member.game_started:
                member_opponent = get_member.current_opponent
                get_member_current_game_id = int(get_member.current_game_id)
                update_game = GTT.objects.filter(id=get_member_current_game_id).update(
                    has_received = True,
                    receiver_number = get_receiver_second_number,
                    game_reload=True
                )
                return redirect(f"/game/gameRoom/{username}/vs/{member_opponent}")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")



class Third_Number(View):
    def post(self,request):
        if request.user.is_authenticated:
            get_receiver_third_number = int(request.POST["receiver_third_number"])
            username = request.user.username
            user_id = request.user.id
            get_member = Members.objects.get(id=user_id)
            if get_member.game_started:
                member_opponent = get_member.current_opponent
                get_member_current_game_id = int(get_member.current_game_id)
                update_game = GTT.objects.filter(id=get_member_current_game_id).update(
                    has_received = True,
                    receiver_number = get_receiver_third_number,
                    game_reload=True
                )
                return redirect(f"/game/gameRoom/{username}/vs/{member_opponent}")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")



class Fourth_Number(View):
    def post(self,request):
        if request.user.is_authenticated:
            get_receiver_fourth_number = int(request.POST["receiver_fourth_number"])
            username = request.user.username
            user_id = request.user.id
            get_member = Members.objects.get(id=user_id)
            if get_member.game_started:
                member_opponent = get_member.current_opponent
                get_member_current_game_id = int(get_member.current_game_id)
                update_game = GTT.objects.filter(id=get_member_current_game_id).update(
                    has_received = True,
                    receiver_number = get_receiver_fourth_number,
                    game_reload=True
                )
                return redirect(f"/game/gameRoom/{username}/vs/{member_opponent}")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")


class Fifth_Number(View):
    def post(self,request):
        if request.user.is_authenticated:
            get_receiver_fifth_number = int(request.POST["receiver_fifth_number"])
            username = request.user.username
            user_id = request.user.id
            get_member = Members.objects.get(id=user_id)
            if get_member.game_started:
                member_opponent = get_member.current_opponent
                get_member_current_game_id = int(get_member.current_game_id)
                update_game = GTT.objects.filter(id=get_member_current_game_id).update(
                    has_received = True,
                    receiver_number = get_receiver_fifth_number,
                    game_reload=True
                )
                return redirect(f"/game/gameRoom/{username}/vs/{member_opponent}")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")


class Sixth_Number(View):
    def post(self,request):
        if request.user.is_authenticated:
            get_receiver_sixth_number = int(request.POST["receiver_sixth_number"])
            username = request.user.username
            user_id = request.user.id
            get_member = Members.objects.get(id=user_id)
            if get_member.game_started:
                member_opponent = get_member.current_opponent
                get_member_current_game_id = int(get_member.current_game_id)
                update_game = GTT.objects.filter(id=get_member_current_game_id).update(
                    has_received = True,
                    receiver_number = get_receiver_sixth_number,
                    game_reload=True
                )
                return redirect(f"/game/gameRoom/{username}/vs/{member_opponent}")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")


class Next_Round(View):
    def get(self,request):
        if request.user.is_authenticated:
            username = request.user.username
            user_id = request.user.id
            get_member = Members.objects.get(id=user_id)
            if get_member.game_started:
                member_opponent = get_member.current_opponent
                get_member_current_game_id = int(get_member.current_game_id)
                get_game = GTT.objects.get(id=get_member_current_game_id)
                get_player_one = get_game.player_one
                get_player_two = get_game.player_two
                get_player_one_count = int(get_game.player_one_count)
                get_player_two_count = int(get_game.player_two_count)
                new_round = int(get_game.game_round + 1)
                get_game_golden_number = get_game.current_golden_number
                get_game_receiver_number = get_game.receiver_number
                #updating member if win
                if get_game_golden_number == get_game_receiver_number:
                    if get_player_one == username:
                        new_player_one_count = get_player_one_count + 1
                        update_game = GTT.objects.filter(id=get_member_current_game_id).update(
                            game_round=new_round,
                            player_one_count=new_player_one_count,
                            to_send=username,
                            has_sent=False,
                            to_receive=member_opponent,
                            has_received=False,
                            game_reload=True
                        )
                    elif get_player_two == username:
                        new_player_two_count = get_player_two_count + 1
                        update_game = GTT.objects.filter(id=get_member_current_game_id).update(
                            game_round=new_round,
                            player_two_count=new_player_two_count,
                            to_send=username,
                            has_sent=False,
                            to_receive=member_opponent,
                            has_received=False,
                            game_reload=True
                        )
                #updating member_opponent if loss
                else:
                    if get_player_one == member_opponent:
                        new_player_one_count = get_player_one_count + 1
                        update_game = GTT.objects.filter(id=get_member_current_game_id).update(
                            game_round=new_round,
                            player_one_count=new_player_one_count,
                            to_send=username,
                            has_sent=False,
                            to_receive=member_opponent,
                            has_received=False,
                            game_reload=True
                        )
                    elif get_player_two == member_opponent:
                        new_player_two_count = get_player_two_count + 1
                        update_game = GTT.objects.filter(id=get_member_current_game_id).update(
                            game_round=new_round,
                            player_two_count=new_player_two_count,
                            to_send=username,
                            has_sent=False,
                            to_receive=member_opponent,
                            has_received=False,
                            game_reload=True
                        )
                return redirect(f"/game/gameRoom/{username}/vs/{member_opponent}")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")


class Finish_Round(View):
    def post(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=user_id)
            if get_member.game_started:
                member_opponent = get_member.current_opponent
                get_member_current_game_id = get_member.current_game_id
                update_a_winner_game = GTT.objects.filter(id=get_member_current_game_id).update(
                    has_finished = True,
                    game_reload=True
                )
                return redirect(f"/game/gameRoom/{username}/vs/{member_opponent}")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")




class End_Game(View):
    def post(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            get_member = Members.objects.get(id=user_id)
            if get_member.game_started:
                member_opponent = get_member.current_opponent
                get_member_current_game_id = get_member.current_game_id
                if GTT.objects.filter(id=get_member_current_game_id).exists():
                    delete_game = GTT.objects.filter(id=get_member_current_game_id).delete()
                    update_member = Members.objects.filter(id=user_id).update(
                        game_started = False
                    )
                    #get and update member_opponent
                    get_member_opponent_id = int(User.objects.get(username=member_opponent).id)
                    update_member_opponent = Members.objects.filter(id=get_member_opponent_id).update(
                        game_started = False
                    )
                return redirect("home_page")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")



class Check_Game_Reload(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            member_current_game_id = Members.objects.get(id=user_id).current_game_id
            check_game_reload = GTT.objects.get(id=member_current_game_id).game_reload
            return HttpResponse(check_game_reload)
        else:
            return redirect("login_page")


class Update_Game_Reload(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            member_current_game_id = Members.objects.get(id=user_id).current_game_id
            update_game_reload = GTT.objects.filter(id=member_current_game_id).update(
                game_reload = False
            )
            return HttpResponse(True)
        else:
            return redirect("login_page")

class Opponent_Delay_Report(View):
    def post(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            get_member = Members.objects.get(id=user_id)
            member_opponent = get_member.current_opponent
            if get_member.game_started:
                member_opponent_id = int(User.objects.get(username=member_opponent).id)
                get_member_opponent = Members.objects.get(id=member_opponent_id)
                create_game_delay_report = Game_Delay_Report.objects.create(
                    reporter = request.user.username,
                    report = member_opponent
                )
                #adding and updating member opponent reports
                new_member_opponent_report_history = get_member_opponent.report_history.add(create_game_delay_report)
                new_member_opponent_report = int(get_member_opponent.number_of_reports) + 1
                update_member_opponent = Members.objects.filter(id=member_opponent_id).update(
                    number_of_reports = new_member_opponent_report
                )
                subject = f"Game Delay Report"
                message = f"{get_member} Reported {member_opponent} For Game Delay"
                receiver_email = "Babalekan14@gmail.com"
                sender_email = settings.EMAIL_HOST_USER
                # sending mail
                send_mail = EmailMessage(
                    subject,
                    message,
                    sender_email,
                    [receiver_email]
                )
                send_mail.send(fail_silently=True)

                return redirect("home_page")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")