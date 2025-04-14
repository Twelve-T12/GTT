from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth.models import User
from main.models import Members, Admin_Setup, Transfer_History, Game_Delay_Report
from .models import All_Gtt_Whot_Cards,Gtt_Whot,Special_Member
import random
from datetime import datetime
# Create your views here.

class Gtt_Whott_Game(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=int(user_id))
            member_has_game = get_member.has_game
            member_game_type = get_member.current_game_type
            if member_has_game:
                if not get_member.game_started:
                    if member_game_type == "Golden Whot":
                        member_opponent = get_member.current_opponent
                        member_is_challenger = get_member.is_challenger
                        challenge_amount = int(get_member.current_challenge_amount)
                        potential_wining_amount = int(challenge_amount * 2)
                        format_challenge_amount = "{:,}".format(challenge_amount)
                        context = {
                            "is_challenger": member_is_challenger,
                            "opponent": member_opponent,
                            "format_amount": format_challenge_amount,
                            "potential_wining": "{:,}".format(potential_wining_amount),
                            "amount": challenge_amount,
                            "username": username
                        }
                        return render(request,"gtt_whott_game_preview.html",context)
                    else:
                        return redirect("home_page")
                else:
                    return redirect("gttWhot_game_room_page")
            else:
                return redirect("home_page")
        else:
            return redirect("home_page")


class Start_Gtt_Card_Game(View):
    def get(self,request,amount):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=int(user_id))
            member_opponent = get_member.current_opponent
            get_member_opponent_id = User.objects.get(username=member_opponent).id
            get_member_opponent_details = Members.objects.get(id=int(get_member_opponent_id))
            if get_member.current_opponent == member_opponent:
                if get_member_opponent_details.current_opponent == username:
                    if get_member.balance >= int(amount) and get_member_opponent_details.balance >= int(amount):
                        if get_member.has_game:
                            if not get_member_opponent_details.game_started:
                                if get_member.current_game_type == "Golden Whot" and get_member_opponent_details.current_game_type == "Golden Whot":
                                    get_all_cards = All_Gtt_Whot_Cards.objects.all()
                                    create_new_gtt_whot_game = Gtt_Whot.objects.create(
                                        player_one=username,
                                        player_two=member_opponent,
                                        to_play=member_opponent
                                    )
                                    get_game = Gtt_Whot.objects.get(player_one=username)
                                    game_id = Gtt_Whot.objects.get(player_one=username).id
                                    # making list for general market
                                    list_for_game_market = []
                                    for i in get_all_cards:
                                        list_for_game_market.append(i)
                                    # adding list market to game market
                                    for i in list_for_game_market:
                                        get_game.general_market.add(i)
                                    ############FOR PLAYER ONE###########
                                    # getting general market
                                    get_general_market_for_player_one = get_game.general_market.all()
                                    new_gen_market_list_for_player_one = []
                                    list_for_player_one = []
                                    for i in get_general_market_for_player_one:
                                        new_gen_market_list_for_player_one.append(i)
                                    shuffle_gen_for_player_one = random.shuffle(new_gen_market_list_for_player_one)
                                    # adding 5 cars to player one list
                                    for i in range(5):
                                        list_for_player_one.append(new_gen_market_list_for_player_one[i])
                                    # adding cards to player one
                                    for i in list_for_player_one:
                                        get_game.player_one_cards.add(i)
                                    # removing player one cards from general market
                                    get_all_player_one_cards = get_game.player_one_cards.all()
                                    for i in get_all_player_one_cards:
                                        get_game.general_market.remove(i.id)
                                    ############FOR PLAYER TWO###########
                                    get_general_market_for_player_two = get_game.general_market.all()
                                    new_gen_market_list_for_player_two = []
                                    list_for_player_two = []
                                    for i in get_general_market_for_player_two:
                                        new_gen_market_list_for_player_two.append(i)
                                    shuffle_gen_for_player_one = random.shuffle(new_gen_market_list_for_player_two)
                                    # adding 5 cars to player two list
                                    for i in range(5):
                                        list_for_player_two.append(new_gen_market_list_for_player_two[i])
                                    # adding cards to player one
                                    for i in list_for_player_two:
                                        get_game.player_two_cards.add(i)
                                    # removing player one cards from general market
                                    get_all_player_two_cards = get_game.player_two_cards.all()
                                    for i in get_all_player_two_cards:
                                        get_game.general_market.remove(i.id)
                                    ########GETTING CURRENT CARD########
                                    get_general_market_for_current_card = get_game.general_market.all()
                                    new_gen_market_list_for_current_card = []
                                    list_for_current_card = []
                                    for i in get_general_market_for_current_card:
                                        new_gen_market_list_for_current_card.append(i)
                                    for i in range(1):
                                        ran_number = random.randint(1, 10)
                                        list_for_current_card.append(new_gen_market_list_for_current_card[int(ran_number)])
                                    # adding current card list to current card
                                    for i in list_for_current_card:
                                        get_game.current_card.add(i)
                                    # Removing Current Card From Market
                                    get_current_card = get_game.current_card.all()
                                    for i in get_current_card:
                                        get_game.general_market.remove(i.id)
                                    # Updating Game And Game Numbers
                                    get_admin = Admin_Setup.objects.get(id=1)
                                    for i in get_current_card:
                                        if int(i.card_number) == 1:
                                            update_game = Gtt_Whot.objects.filter(player_one=username).update(
                                            to_play = get_game.player_one,
                                        )
                                        elif int(i.card_number) == 2:
                                            update_game = Gtt_Whot.objects.filter(player_one=username).update(
                                            required_to_pick = True,
                                            how_many_required_to_pick = 2,
                                            player_required_to_pick = get_game.player_two,
                                        )
                                        elif int(i.card_number) == 14:
                                            update_game = Gtt_Whot.objects.filter(player_one=username).update(
                                            required_to_pick = True,
                                            how_many_required_to_pick = 1,
                                            player_required_to_pick = get_game.player_two,
                                        )
                                    if int(amount) <= 1000:
                                        update_game = Gtt_Whot.objects.filter(player_one=username).update(
                                            number_of_general_market=38,
                                            player_one_number_of_cards=5,
                                            player_two_number_of_cards=5,
                                            game_charges=int(get_admin.min_game_charges)
                                        )
                                    else:
                                        update_game = Gtt_Whot.objects.filter(player_one=username).update(
                                            number_of_general_market=38,
                                            player_one_number_of_cards=5,
                                            player_two_number_of_cards=5,
                                            game_charges=int(get_admin.max_game_charges)
                                        )
                                    # updating player member
                                    game_wining_price = int(amount) * 2
                                    get_member = Members.objects.get(id=int(user_id))
                                    get_member_balance = int(get_member.balance)
                                    new_member_balance = get_member_balance - int(amount)
                                    create_member_new_debit_transaction = Transfer_History.objects.create(
                                        transaction_type="Debit",
                                        receiver_name=f"Gtt-Whott Challenge With {member_opponent}",
                                        amount="{:,}".format(int(amount)),
                                        charges="",
                                        net_balance="{:,}".format(new_member_balance)
                                    )
                                    get_member = Members.objects.get(id=int(user_id))
                                    get_member_balance = int(get_member.balance)
                                    new_member_balance = get_member_balance - int(amount)
                                    get_member_number_of_play = int(get_member.number_of_play)
                                    new_member_no_of_play = get_member_number_of_play + 1
                                    update_member = Members.objects.filter(id=int(user_id)).update(
                                        balance=new_member_balance,
                                        number_of_play=new_member_no_of_play,
                                        game_started=True,
                                        current_game_id=game_id,
                                        has_transfer=True,
                                        current_game_wining_amount=game_wining_price,
                                        current_number_of_whott_cards=5
                                    )
                                    # adding debit transfer to member
                                    member_new_game_debit = get_member.transaction_history.add(
                                        create_member_new_debit_transaction)
                                    # updating member opponent
                                    get_member_opponent_id = User.objects.get(username=member_opponent).id
                                    get_member_opponent = Members.objects.get(id=int(get_member_opponent_id))
                                    get_member_opponent_balance = int(get_member_opponent.balance)
                                    new_member_opponent_balance = get_member_opponent_balance - int(amount)
                                    create_member_opponent_new_debit_transaction = Transfer_History.objects.create(
                                        transaction_type="Debit",
                                        receiver_name=f"Gtt-Whott Challenge With {username}",
                                        amount="{:,}".format(int(amount)),
                                        charges = "",
                                        net_balance="{:,}".format(new_member_opponent_balance)
                                    )
                                    get_member_opponent_id = User.objects.get(username=member_opponent).id
                                    get_member_opponent = Members.objects.get(id=int(get_member_opponent_id))
                                    get_member_opponent_balance = int(get_member_opponent.balance)
                                    new_member_opponent_balance = get_member_opponent_balance - int(amount)
                                    get_member_opponent_number_of_play = int(get_member_opponent.number_of_play)
                                    new_member_opponent_no_of_play = get_member_opponent_number_of_play + 1
                                    update_member_opponent = Members.objects.filter(id=int(get_member_opponent_id)).update(
                                        balance=new_member_opponent_balance,
                                        number_of_play=new_member_opponent_no_of_play,
                                        game_started=True,
                                        current_game_id=game_id,
                                        has_transfer=True,
                                        current_game_wining_amount=game_wining_price,
                                        current_number_of_whott_cards=5
                                    )
                                    # adding debit transfer to member_opponent
                                    member_opponent_new_debit_transfer = get_member_opponent.transaction_history.add(
                                        create_member_opponent_new_debit_transaction)
                                    new_golden_whot_no_of_play = int(get_admin.no_of_golden_Whot_played) + 1
                                    update_admin = Admin_Setup.objects.filter(id=1).update(
                                        no_of_golden_Whot_played=int(new_golden_whot_no_of_play)
                                    )
                                    #updating today number of games play
                                    today = datetime.today().day
                                    get_admin = Admin_Setup.objects.get(id=1)
                                    get_admin_today = int(get_admin.today)
                                    if today == get_admin_today:
                                        new_today_games = int(get_admin.today_number_of_games) + 1
                                        update_today_games = Admin_Setup.objects.filter(id=1).update(
                                            today_number_of_games = new_today_games,
                                        )
                                    else:
                                        update_today = Admin_Setup.objects.filter(id=1).update(
                                            today = today,
                                            today_number_of_games = 1
                                        )
                                    return redirect("gttWhott_page")
                                else:
                                    messages.info(request, f"Please Retry Game Again")
                                    return redirect("home_page")
                            else:
                                messages.info(request, f"{member_opponent} already in another game")
                                return redirect("home_page")
                        else:
                            return redirect("home_page")
                    else:
                        messages.info(request, f"Can't Continue")
                        return redirect("home_page")
                else:
                    messages.info(request, f"{member_opponent} Has Switched To Another Game ")
                    return redirect("home_page")
            else:
                messages.info(request,f"You Switched To Another Game..")
                return redirect("home_page")
        else:
            return redirect("login_page")


class Gtt_Whott_Game_Room(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=int(user_id))
            if get_member.game_started:
                get_member_no_of_cards = get_member.current_number_of_whott_cards
                member_opponent = get_member.current_opponent
                get_member_opponent_id = User.objects.get(username=member_opponent).id
                get_member_opponent_details = Members.objects.get(id=int(get_member_opponent_id))
                get_member_opponent_no_of_cards = get_member_opponent_details.current_number_of_whott_cards
                get_member_current_game_id = get_member.current_game_id
                get_game_challenge_amount = get_member.current_challenge_amount
                get_game_wining_price = get_member.current_game_wining_amount
                get_game = Gtt_Whot.objects.get(id=int(get_member_current_game_id))
                game_user_can_play = get_game.user_can_play
                game_has_tie = get_game.has_tie
                game_has_finished = get_game.game_finished
                game_concluded = get_game.game_concluded
                get_game_winner = get_game.game_winner
                get_player_won = get_game.player_won
                check_hold_on = get_game.hold_on
                check_required_to_pick = get_game.required_to_pick
                no_cards_to_pick = int(get_game.how_many_required_to_pick)
                if not game_has_finished or not game_concluded:
                    get_player_one = get_game.player_one
                    get_player_two = get_game.player_two
                    get_no_of_general_market = get_game.number_of_general_market
                    get_general_market = get_game.general_market.all()
                    get_current_card = get_game.current_card.all()
                    get_player_one_cards = get_game.player_one_cards.all()
                    player_one_total_amount_of_cards = []
                    for i in get_player_one_cards:
                        player_one_total_amount_of_cards.append(int(i.card_number))
                    player_one_total_amount_of_cards = sum(player_one_total_amount_of_cards)
                    get_player_two_cards = get_game.player_two_cards.all()
                    player_two_total_amount_of_cards = []
                    for i in get_player_two_cards:
                        player_two_total_amount_of_cards.append(int(i.card_number))
                    player_two_total_amount_of_cards = sum(player_two_total_amount_of_cards)
                    get_player_one_amount_of_cards = get_game.player_one_amount_of_cards
                    get_player_two_amount_of_cards = get_game.player_two_amount_of_cards
                    check_counted_cards = get_game.counted_cards
                    member_opponent_id_for_phone_number = int(User.objects.get(username=member_opponent).id)
                    get_member_opponent_phone_number = Members.objects.get(id=member_opponent_id_for_phone_number).phone_number
                    member_opponent_whatsapp_number = "234" + get_member_opponent_phone_number[1:]
                    member_opponent_whatsapp_link = f"https://wa.me/{member_opponent_whatsapp_number}?text=Hi,%20My%20Name%20Is%20{request.user.username},%20I%20Am%20An%20Opponent%20From%20GTT..."
                    context = {
                        "potential_wining":"{:,}".format(get_game_wining_price),
                        "game_finished":game_has_finished,
                        "hold_on":check_hold_on,
                        "required_to_pick":check_required_to_pick,
                        "no_of_cards_to_pick":no_cards_to_pick,
                        "game_winner":get_game_winner,
                        "player_won":get_player_won,
                        "player_one_total_amount_of_cards":player_one_total_amount_of_cards,
                        "player_two_total_amount_of_cards":player_two_total_amount_of_cards,
                        "player_one_card_amount":get_player_one_amount_of_cards,
                        "player_two_card_amount":get_player_two_amount_of_cards,
                        "number_of_cards":get_member_no_of_cards,
                        "counted_cards":check_counted_cards,
                        "can_play":game_user_can_play,
                        "has_tie":game_has_tie,
                        "to_play":get_game.to_play,
                        "opponent":member_opponent,
                        "opp_number_of_cards":int(get_member_opponent_no_of_cards),
                        "challenge_amount":"{:,}".format(get_game_challenge_amount),
                        "challenge_price":"{:,}".format(get_game_wining_price),
                        "number_of_general_market":int(get_no_of_general_market),
                        "general_market":get_general_market,
                        "current_card":get_current_card,
                        "player_one":get_player_one,
                        "player_two":get_player_two,
                        "player_one_cards":get_player_one_cards,
                        "player_two_cards":get_player_two_cards,
                        "opponent_whatsapp_link":member_opponent_whatsapp_link,
                        "opponent_gender":get_member_opponent_details.gender,
                        "is_special": get_member.is_special
                    }
                    return render(request,"gtt_whott.html",context)
                else:
                    return redirect("home_page")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")


class Collect_Card(View):
    def post(self,request,id,card_shape,card_number):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=int(user_id))
            if get_member.game_started:
                if get_member.current_game_type == "Golden Whot":
                    member_current_game_id = get_member.current_game_id
                    get_game = Gtt_Whot.objects.get(id=int(member_current_game_id))
                    game_has_tie = get_game.has_tie
                    game_has_finished = get_game.game_finished
                    if not game_has_finished:
                        if get_game.to_play == username:
                            get_player_card_id = id
                            get_card_details = All_Gtt_Whot_Cards.objects.get(id=int(get_player_card_id))
                            check_card_has_power = get_card_details.has_power
                            get_player_card_shape = card_shape
                            get_player_card_number = card_number
                            get_player_one = get_game.player_one
                            get_player_two = get_game.player_two
                            get_game_required_to_pick = get_game.required_to_pick
                            get_game_current_card = get_game.current_card.all()
                            get_no_of_general_market = int(get_game.number_of_general_market)
                            if get_no_of_general_market >= 1:
                                for i in get_game_current_card:
                                    if i.card_shape == get_player_card_shape or i.card_number == get_player_card_number:
                                        if not get_game_required_to_pick:
                                            if not check_card_has_power:
                                                # updating current card
                                                for i in get_game_current_card:
                                                    get_game.current_card.remove(i.id)
                                                new_current_card = get_game.current_card.add(get_player_card_id)
                                                # updating player
                                                if get_player_one == username:
                                                    removing_card_player_one = get_game.player_one_cards.remove(
                                                        get_player_card_id)
                                                    new_player_one_no_of_cards = int(
                                                        get_game.player_one_number_of_cards) - 1
                                                    update_player_one_number_game = Gtt_Whot.objects.filter(
                                                        id=int(member_current_game_id)).update(
                                                        player_one_number_of_cards=new_player_one_no_of_cards,
                                                        to_play=get_member.current_opponent,
                                                        game_reload=True,
                                                        hold_on=False
                                                    )
                                                    new_member_number_of_whott_cards = int(
                                                        get_member.current_number_of_whott_cards) - 1
                                                    update_member = Members.objects.filter(id=int(user_id)).update(
                                                        current_number_of_whott_cards=new_member_number_of_whott_cards
                                                    )
                                                    check_get_game = Gtt_Whot.objects.get(id=int(member_current_game_id))
                                                    check_player_one_number_of_cards = int(
                                                        check_get_game.player_one_number_of_cards)
                                                    check_player_two_number_of_cards = int(
                                                        check_get_game.player_two_number_of_cards)
                                                    check_number_of_general_market = int(
                                                        check_get_game.number_of_general_market)
                                                    if check_player_one_number_of_cards == 0 and check_player_two_number_of_cards >= 1:
                                                        update_game = Gtt_Whot.objects.filter(
                                                            id=int(member_current_game_id)).update(
                                                            user_can_play=False,
                                                            player_won =True,
                                                            game_winner=get_game.player_one,
                                                            game_reload = True,
                                                            hold_on = False
                                                        )
                                                    elif check_player_two_number_of_cards == 0 and  check_player_one_number_of_cards >= 1:
                                                        update_game = Gtt_Whot.objects.filter(
                                                            id=int(member_current_game_id)).update(
                                                            user_can_play=False,
                                                            player_won=True,
                                                            game_winner=get_game.player_two,
                                                            game_reload = True,
                                                            hold_on = False
                                                        )
                                                    elif check_number_of_general_market == 0 and check_player_one_number_of_cards >= 1 and check_player_two_number_of_cards >= 1:
                                                        update_game = Gtt_Whot.objects.filter(
                                                            id=int(member_current_game_id)).update(
                                                            user_can_play=False,
                                                            has_tie=True,
                                                            game_reload = True,
                                                            hold_on = False
                                                        )
                                                if get_player_two == username:
                                                    removing_card_player_two = get_game.player_two_cards.remove(
                                                        get_player_card_id)
                                                    new_player_two_no_of_cards = int(
                                                        get_game.player_two_number_of_cards) - 1
                                                    update_player_two_number_game = Gtt_Whot.objects.filter(
                                                        id=int(member_current_game_id)).update(
                                                        player_two_number_of_cards=new_player_two_no_of_cards,
                                                        to_play=get_member.current_opponent,
                                                        game_reload=True,
                                                        hold_on=False
                                                    )
                                                    new_member_number_of_whott_cards = int(
                                                        get_member.current_number_of_whott_cards) - 1
                                                    update_member = Members.objects.filter(id=int(user_id)).update(
                                                        current_number_of_whott_cards=new_member_number_of_whott_cards
                                                    )
                                                    check_get_game = Gtt_Whot.objects.get(id=int(member_current_game_id))
                                                    check_player_one_number_of_cards = int(
                                                        check_get_game.player_one_number_of_cards)
                                                    check_player_two_number_of_cards = int(
                                                        check_get_game.player_two_number_of_cards)
                                                    check_number_of_general_market = int(
                                                        check_get_game.number_of_general_market)
                                                    if check_player_one_number_of_cards == 0 and check_player_two_number_of_cards >= 1:
                                                        update_game = Gtt_Whot.objects.filter(
                                                            id=int(member_current_game_id)).update(
                                                            player_won=True,
                                                            game_winner=get_game.player_one,
                                                            user_can_play=False,
                                                            game_reload=True,
                                                            hold_on = False
                                                        )
                                                    elif check_player_two_number_of_cards == 0 and check_player_one_number_of_cards >= 1:
                                                        update_game = Gtt_Whot.objects.filter(
                                                            id=int(member_current_game_id)).update(
                                                            player_won=True,
                                                            game_winner=get_game.player_two,
                                                            user_can_play=False,
                                                            game_reload=True,
                                                            hold_on = False
                                                        )
                                                    elif check_number_of_general_market == 0 and check_player_one_number_of_cards >= 1 and check_player_two_number_of_cards >= 1:
                                                        update_game = Gtt_Whot.objects.filter(
                                                            id=int(member_current_game_id)).update(
                                                            has_tie=True,
                                                            user_can_play=False,
                                                            game_reload=True,
                                                            hold_on = False
                                                        )
                                                return redirect("gttWhot_game_room_page")
                                            else:
                                                return redirect(
                                                    f"/gttWhott/gttWHot/powerCards/{get_player_card_id}/{get_player_card_shape}/{get_player_card_number}")
                                        else:
                                            return redirect("gttWhot_general_market_page")
                                    else:
                                        return HttpResponse("Invalid Card")
                            else:
                                update_game = Gtt_Whot.objects.filter(
                                    id=int(member_current_game_id)).update(
                                    has_tie=True,
                                    user_can_play=False,
                                    game_reload=True
                                )
                                return redirect("gttWhot_general_market_page")
                        else:
                            return HttpResponse("Not Your Turn")
                    else:
                        return redirect("home_page")
                else:
                    return redirect("home_page")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")

class Game_General_Market(View):
    def post(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
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
                                return redirect("gttWhot_game_room_page")
                            else:
                                return HttpResponse("Not Your Turn")
                        else:
                            return redirect("gttWhot_general_market_page")
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
                        return redirect("gttWhot_general_market_page")
                else:
                    return redirect("home_page")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")

    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
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
                                            return redirect("gttWhot_game_room_page")
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
                                            return redirect("gttWhot_game_room_page")
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
                                            return redirect("gttWhot_game_room_page")
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
                                        return redirect("gttWhot_game_room_page")
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
                                        return redirect("gttWhot_game_room_page")
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
                                    return redirect("gttWhot_game_room_page")
                            return redirect("gttWhot_game_room_page")
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
                                return redirect("gttWhot_game_room_page")
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
                                return redirect("gttWhot_game_room_page")
                            return redirect("gttWhot_game_room_page")
                    else:
                        return redirect("gttWhot_game_room_page")
                else:
                    return redirect("home_page")
            else:
                return redirect("home_page")
        else:
            return redirect("home_page")

class Count_Cards(View):
    def post(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=int(user_id))
            if get_member.game_started:
                member_current_game_id = get_member.current_game_id
                get_game = Gtt_Whot.objects.get(id=int(member_current_game_id))
                get_player_one_cards = get_game.player_one_cards.all()
                player_one_cards_amount_list = []
                for i in get_player_one_cards:
                    player_one_cards_amount_list.append(int(i.card_number))
                player_one_amount = sum(player_one_cards_amount_list)
                get_player_two_cards = get_game.player_two_cards.all()
                player_two_cards_amount_list = []
                for i in get_player_two_cards:
                    player_two_cards_amount_list.append(int(i.card_number))
                player_two_amount = sum(player_two_cards_amount_list)
                if int(player_one_amount) < int(player_two_amount):
                    update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                        game_winner = get_game.player_one,
                        counted_cards = True,
                        player_one_amount_of_cards = int(player_one_amount),
                        player_two_amount_of_cards = int(player_two_amount),
                        game_reload = True,
                        hold_on = False,
                    )
                elif int(player_one_amount) > int(player_two_amount):
                    update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                        game_winner=get_game.player_two,
                        counted_cards=True,
                        player_one_amount_of_cards=int(player_one_amount),
                        player_two_amount_of_cards=int(player_two_amount),
                        game_reload=True,
                        hold_on = False,
                    )
                else:
                    update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                        game_winner = "Draw",
                        counted_cards=True,
                        player_one_amount_of_cards=int(player_one_amount),
                        player_two_amount_of_cards=int(player_two_amount),
                        game_reload=True,
                        hold_on = False,
                    )
                return redirect("gttWhot_game_room_page")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")

class Power_Cards(View):
    def get(self,request,id,card_shape,card_number):
        if request.user.is_authenticated:
            username = request.user.username
            user_id = request.user.id
            get_card_details = All_Gtt_Whot_Cards.objects.get(id=int(id))
            get_card_requirement = get_card_details.requirement
            get_member = Members.objects.get(id=int(user_id))
            member_current_game_id = get_member.current_game_id
            get_game = Gtt_Whot.objects.get(id=int(member_current_game_id))
            get_player_one = get_game.player_one
            get_player_two = get_game.player_two
            if get_card_requirement == "HOLD ON":
                get_game_current_card = get_game.current_card.all()
                for i in get_game_current_card:
                    get_game.current_card.remove(i.id)
                new_current_card = get_game.current_card.add(id)
                # updating player
                if get_player_one == username:
                    removing_card_player_one = get_game.player_one_cards.remove(id)
                    new_player_one_no_of_cards = int(get_game.player_one_number_of_cards) - 1
                    update_player_one_number_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                        player_one_number_of_cards=new_player_one_no_of_cards,
                        to_play=username,
                        game_reload=True,
                        hold_on = True
                    )
                    new_member_number_of_whott_cards = int(get_member.current_number_of_whott_cards) - 1
                    update_member = Members.objects.filter(id=int(user_id)).update(
                        current_number_of_whott_cards=new_member_number_of_whott_cards
                    )
                if get_player_two == username:
                    removing_card_player_two = get_game.player_two_cards.remove(id)
                    new_player_two_no_of_cards = int(get_game.player_two_number_of_cards) - 1
                    update_player_two_number_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                        player_two_number_of_cards=new_player_two_no_of_cards,
                        to_play=username,
                        game_reload=True,
                        hold_on = True
                    )
                    new_member_number_of_whott_cards = int(get_member.current_number_of_whott_cards) - 1
                    update_member = Members.objects.filter(id=int(user_id)).update(
                        current_number_of_whott_cards=new_member_number_of_whott_cards
                    )
                return redirect("gttWhot_game_room_page")
            elif get_card_requirement == "PICK TWO":
                get_game_current_card = get_game.current_card.all()
                for i in get_game_current_card:
                    get_game.current_card.remove(i.id)
                new_current_card = get_game.current_card.add(id)
                if username == get_game.player_one:
                    get_game.player_one_cards.remove(id)
                    new_player_one_no_of_cards = int(get_game.player_one_number_of_cards) - 1
                    member_opponent = get_member.current_opponent
                    update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                        player_one_number_of_cards = new_player_one_no_of_cards,
                        to_play=member_opponent,
                        game_reload=True,
                        required_to_pick=True,
                        how_many_required_to_pick=2,
                        player_required_to_pick=member_opponent,
                        hold_on = False
                    )
                    update_member = Members.objects.filter(id=int(user_id)).update(
                        current_number_of_whott_cards = new_player_one_no_of_cards
                    )
                    return redirect("gttWhot_game_room_page")
                elif username == get_game.player_two:
                    get_game.player_two_cards.remove(id)
                    new_player_two_no_of_cards = int(get_game.player_two_number_of_cards) - 1
                    member_opponent = get_member.current_opponent
                    update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                        player_two_number_of_cards = new_player_two_no_of_cards,
                        to_play=member_opponent,
                        game_reload=True,
                        required_to_pick=True,
                        how_many_required_to_pick=2,
                        player_required_to_pick=member_opponent,
                        hold_on = False
                    )
                    update_member = Members.objects.filter(id=int(user_id)).update(
                        current_number_of_whott_cards=new_player_two_no_of_cards
                    )
                    return redirect("gttWhot_game_room_page")
            elif get_card_requirement == "GENERAL MARKET":
                get_game_current_card = get_game.current_card.all()
                for i in get_game_current_card:
                    get_game.current_card.remove(i.id)
                new_current_card = get_game.current_card.add(id)
                if username == get_game.player_one:
                    get_game.player_one_cards.remove(id)
                    new_player_one_no_of_cards = int(get_game.player_one_number_of_cards) - 1
                    member_opponent = get_member.current_opponent
                    update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                        player_one_number_of_cards=new_player_one_no_of_cards,
                        to_play=member_opponent,
                        game_reload=True,
                        required_to_pick=True,
                        how_many_required_to_pick=1,
                        player_required_to_pick=member_opponent,
                        hold_on = False
                    )
                    update_member = Members.objects.filter(id=int(user_id)).update(
                        current_number_of_whott_cards=new_player_one_no_of_cards
                    )
                    return redirect("gttWhot_game_room_page")
                elif username == get_game.player_two:
                    get_game.player_two_cards.remove(id)
                    new_player_two_no_of_cards = int(get_game.player_two_number_of_cards) - 1
                    member_opponent = get_member.current_opponent
                    update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                        player_two_number_of_cards=new_player_two_no_of_cards,
                        to_play=member_opponent,
                        game_reload=True,
                        required_to_pick=True,
                        how_many_required_to_pick=1,
                        player_required_to_pick=member_opponent,
                        hold_on = False
                    )
                    update_member = Members.objects.filter(id=int(user_id)).update(
                        current_number_of_whott_cards=new_player_two_no_of_cards
                    )
                    return redirect("gttWhot_game_room_page")
                else:
                    return redirect("home_page")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")



class Gtt_Whot_Game_Reload(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            member_current_game_id = Members.objects.get(id=user_id).current_game_id
            check_game_reload = Gtt_Whot.objects.get(id=member_current_game_id).game_reload
            return HttpResponse(check_game_reload)
        else:
            return redirect("login_page")

class Update_Game_Reload(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            member_current_game_id = Members.objects.get(id=user_id).current_game_id
            update_game_reload = Gtt_Whot.objects.filter(id=member_current_game_id).update(
                game_reload = False
            )
            return HttpResponse(True)
        else:
            return redirect("login_page")

class End_Game(View):
    def post(self,request):
        if request.user.is_authenticated:
            username = request.user.username
            user_id = request.user.id
            get_member = Members.objects.get(id=int(user_id))
            if get_member.game_started:
                member_current_game_id = get_member.current_game_id
                get_game = Gtt_Whot.objects.get(id=int(member_current_game_id))
                if not get_game.game_finished:
                    get_game_winner = get_game.game_winner
                    if get_game.player_one == get_game_winner:
                        get_player_id = User.objects.get(username=get_game.player_one).id
                        get_member = Members.objects.get(id=int(get_player_id))
                        get_current_winning_amount = get_member.current_game_wining_amount
                        get_game_charges = get_game.game_charges
                        # Create New Credit Transaction
                        net_credit_balance = int(get_member.balance) + int(get_current_winning_amount)
                        create_credit_transaction_history = Transfer_History.objects.create(
                            transaction_type = "Credit",
                            sender_name = f"Winning '{get_member.current_opponent}'",
                            amount = "{:,}".format(int(get_current_winning_amount)),
                            net_balance="{:,}".format(net_credit_balance)
                        )
                        new_member_credit_transaction = get_member.transaction_history.add(create_credit_transaction_history)
                        # Create New Debit Transaction
                        net_debit_balance = int(get_member.balance) + int(get_current_winning_amount) - int(
                            get_game_charges)
                        create_debit_transaction_history = Transfer_History.objects.create(
                            transaction_type = "Debit",
                            receiver_name = f"Winning Gtt-Whot Challenge '{get_member.current_opponent}' Game Charges",
                            amount = "{:,}".format(int(get_game_charges)),
                            charges="",
                            net_balance="{:,}".format(net_debit_balance)
                        )
                        new_member_debit_transaction = get_member.transaction_history.add(create_debit_transaction_history)
                        # update member
                        new_member_balance = int(get_member.balance) + int(get_current_winning_amount) - int(get_game_charges)
                        member_new_admin_charge = int(get_member.admin_charge) + int(get_game_charges)
                        new_member_no_of_wins = int(get_member.number_of_win) + 1
                        update_member = Members.objects.filter(id=int(get_player_id)).update(
                            balance = new_member_balance,
                            number_of_win = new_member_no_of_wins,
                            admin_charge=member_new_admin_charge
                        )
                        #Update Member Opponent
                        get_member_opp_id = User.objects.get(username=get_member.current_opponent).id
                        get_mem_opp = Members.objects.get(id=int(get_member_opp_id))
                        member_opp_new_no_loss = int(get_mem_opp.number_of_loss) + 1
                        update_member_opp = Members.objects.filter(id=int(get_member_opp_id)).update(
                            number_of_loss = member_opp_new_no_loss
                        )
                        #update game
                        update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                            game_finished = True,
                            game_reload = True
                        )
                    elif get_game.player_two == get_game_winner:
                        get_player_id = User.objects.get(username=get_game.player_two).id
                        get_member = Members.objects.get(id=int(get_player_id))
                        get_current_winning_amount = get_member.current_game_wining_amount
                        get_game_charges = get_game.game_charges
                        # Create New Credit Transaction
                        net_credit_balance = int(get_member.balance) + int(get_current_winning_amount)
                        create_credit_transaction_history = Transfer_History.objects.create(
                            transaction_type="Credit",
                            sender_name=f"Winning '{get_member.current_opponent}'",
                            amount="{:,}".format(int(get_current_winning_amount)),
                            net_balance="{:,}".format(net_credit_balance)
                        )
                        new_member_credit_transaction = get_member.transaction_history.add(
                            create_credit_transaction_history)
                        # Create New Debit Transaction
                        net_debit_balance = int(get_member.balance) + int(get_current_winning_amount) - int(
                            get_game_charges)
                        create_debit_transaction_history = Transfer_History.objects.create(
                            transaction_type="Debit",
                            receiver_name=f"Winning Gtt-Whot Challenge '{get_member.current_opponent}' Game Charges",
                            amount="{:,}".format(int(get_game_charges)),
                            charges="",
                            net_balance="{:,}".format(net_debit_balance)
                        )
                        new_member_debit_transaction = get_member.transaction_history.add(
                            create_debit_transaction_history)
                        # update member
                        new_member_balance = int(get_member.balance) + int(get_current_winning_amount) - int(
                            get_game_charges)
                        new_member_admin_charge = int(get_member.admin_charge) + int(get_game_charges)
                        new_member_no_of_wins = int(get_member.number_of_win) + 1
                        update_member = Members.objects.filter(id=int(get_player_id)).update(
                            balance=new_member_balance,
                            number_of_win=new_member_no_of_wins,
                            admin_charge=new_member_admin_charge
                        )
                        # Update Member Opponent
                        get_member_opp_id = User.objects.get(username=get_member.current_opponent).id
                        get_mem_opp = Members.objects.get(id=int(get_member_opp_id))
                        member_opp_new_no_loss = int(get_mem_opp.number_of_loss) + 1
                        update_member_opp = Members.objects.filter(id=int(get_member_opp_id)).update(
                            number_of_loss=member_opp_new_no_loss
                        )
                        update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                            game_finished=True,
                            game_reload = True
                        )
                    elif get_game_winner == "Draw":
                        get_member = Members.objects.get(id=int(user_id))
                        get_current_challenge_amount = get_member.current_challenge_amount
                        get_game_charges = int(get_game.game_charges)
                        per_player = get_game_charges/2
                        net_credit_balance = int(get_member.balance) + int(get_current_challenge_amount)
                        create_credit_draw_transaction = Transfer_History.objects.create(
                            transaction_type = "Credit",
                            sender_name = f"Draw Gtt-Whott with '{get_member.current_opponent}'",
                            amount = int(get_current_challenge_amount),
                            net_balance="{:,}".format(net_credit_balance)
                        )
                        add_credit_draw = get_member.transaction_history.add(create_credit_draw_transaction)
                        net_debit_balance = int(get_member.balance) + int(get_current_challenge_amount) - int(
                            per_player)
                        create_debit_draw_transactions = Transfer_History.objects.create(
                            transaction_type = "Debit",
                            receiver_name = f"Draw Gtt-Whott with '{get_member.current_opponent}' Game Charges",
                            amount = int(per_player),
                            charges="",
                            net_balance="{:,}".format(net_debit_balance)
                        )
                        add_debit_draw = get_member.transaction_history.add(create_debit_draw_transactions)
                        new_member_no_of_draw = int(get_member.number_of_draw) + 1
                        new_member_balance = int(get_member.balance) + int(get_current_challenge_amount) - int(per_player)
                        new_member_admin_charge = int(get_member.admin_charge) + int(per_player)
                        update_member = Members.objects.filter(id=int(user_id)).update(
                            balance = new_member_balance,
                            number_of_draw = new_member_no_of_draw,
                            admin_charge=new_member_admin_charge
                        )
                        # Update Member Opponent Draw
                        mem_opp_id = User.objects.get(username=get_member.current_opponent).id
                        get_opp_details = Members.objects.get(id=int(mem_opp_id))
                        net_mem_opp_credit_balance = int(get_opp_details.balance) + int(get_current_challenge_amount)
                        create_mem_opp_credit_draw_transaction = Transfer_History.objects.create(
                            transaction_type="Credit",
                            sender_name=f"Draw Gtt-Whott with '{get_opp_details.current_opponent}'",
                            amount=int(get_current_challenge_amount),
                            net_balance="{:,}".format(net_mem_opp_credit_balance)
                        )
                        add_credit_draw_mem_opp = get_opp_details.transaction_history.add(create_mem_opp_credit_draw_transaction)
                        net_mem_opp_debit_balance = int(get_opp_details.balance) + int(
                            get_current_challenge_amount) - int(
                            per_player)
                        create_mem_opp_debit_draw_transaction = Transfer_History.objects.create(
                            transaction_type="Debit",
                            receiver_name=f"Draw Gtt-Whott with '{get_opp_details.current_opponent}' Game Charges",
                            amount=int(per_player),
                            charges="",
                            net_balance="{:,}".format(net_mem_opp_debit_balance)
                        )
                        add_debit_draw_mem_opp = get_opp_details.transaction_history.add(create_mem_opp_debit_draw_transaction)
                        new_mem_opp_no_of_draw = int(get_opp_details.number_of_draw) + 1
                        new_mem_opp_balance = int(get_opp_details.balance) + int(get_current_challenge_amount) - int(per_player)
                        new_mem_opp_admin_charge = int(get_opp_details.admin_charge) + int(per_player)
                        update_member = Members.objects.filter(id=int(mem_opp_id)).update(
                            balance=new_mem_opp_balance,
                            number_of_draw=new_mem_opp_no_of_draw,
                            admin_charge=new_mem_opp_admin_charge
                        )
                        update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                            game_finished=True,
                            game_reload=True
                        )
                    return redirect("gttWhot_game_room_page")
                else:
                    return redirect("home_page")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")

class Finish_Game(View):
    def post(self,request):
        if request.user.is_authenticated:
            username = request.user.username
            user_id = request.user.id
            get_member = Members.objects.get(id=int(user_id))
            if get_member.game_started:
                member_current_game_id = get_member.current_game_id
                if Gtt_Whot.objects.filter(id=int(member_current_game_id)).exists():
                    get_game = Gtt_Whot.objects.get(id=int(member_current_game_id))
                    if get_game:
                        # update game
                        update_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).update(
                            game_finished = True,
                            game_concluded = True,
                            game_reload = True
                        )
                        # update member
                        update_member = Members.objects.filter(id=int(user_id)).update(
                            game_started = False
                        )
                        # get and update mem_opp
                        mem_opp_id = User.objects.get(username=get_member.current_opponent).id
                        update_mem_opp = Members.objects.filter(id=int(mem_opp_id)).update(
                            game_started=False
                        )
                        # delete game
                        delete_game = Gtt_Whot.objects.filter(id=int(member_current_game_id)).delete()
                        return redirect("gttWhot_game_room_page")
                    else:
                        return redirect("gttWhot_game_room_page")
                else:
                    return redirect("home_page")
            else:
                return redirect("home_page")
        else:
            return redirect("login_page")


class Gtt_Whot_Member_Special_Service(View):
    def post(self,request):
        if request.user.is_authenticated:
            username = request.user.username
            user_id = request.user.id
            get_member = Members.objects.get(id=int(user_id))
            market_chosen_card_id = request.POST["special_general_market"]
            player_chosen_card_id = request.POST["special_player_card"]
            print(market_chosen_card_id)
            print(type(market_chosen_card_id))
            if market_chosen_card_id != "select-option" and player_chosen_card_id != "select-option":
                if get_member.is_special:
                    if get_member.game_started:
                        if get_member.current_game_type == "Golden Whot":
                            member_current_game_id = int(get_member.current_game_id)
                            get_game = Gtt_Whot.objects.get(id=int(member_current_game_id))
                            remove_market_chosen_card = get_game.general_market.remove(int(market_chosen_card_id))
                            if username == get_game.player_one:
                                add_market_chosen_card_to_player_one = get_game.player_one_cards.add(
                                    int(market_chosen_card_id))
                                remove_player_chosen_card = get_game.player_one_cards.remove(int(player_chosen_card_id))
                                add_player_chosen_card_to_market = get_game.general_market.add(
                                    int(player_chosen_card_id))
                            else:
                                add_market_chosen_card_to_player_two = get_game.player_two_cards.add(
                                    int(market_chosen_card_id))
                                remove_player_chosen_card = get_game.player_two_cards.remove(int(player_chosen_card_id))
                                add_player_chosen_card_to_market = get_game.general_market.add(
                                    int(player_chosen_card_id))
                            # Get Player Card Details
                            get_player_card_details = All_Gtt_Whot_Cards.objects.get(id=int(player_chosen_card_id))
                            player_card_number = get_player_card_details.card_number
                            player_card_shape = get_player_card_details.card_shape
                            # Get Exchanged Card Details
                            get_exchanged_card_details = All_Gtt_Whot_Cards.objects.get(id=int(market_chosen_card_id))
                            exchanged_card_number = get_exchanged_card_details.card_number
                            exchanged_card_shape = get_exchanged_card_details.card_shape
                            new_special_member_card_exchange = Special_Member.objects.create(
                                username = username,
                                opponent = get_member.current_opponent,
                                game_id = get_member.current_game_id,
                                user_card = f"{player_card_number}...{player_card_shape}",
                                exchanged_card = f"{exchanged_card_number}...{exchanged_card_shape}",
                                challenge_stake_amount = get_member.current_challenge_amount,
                                challenge_winning_amount = get_member.current_game_wining_amount
                            )
                            messages.info(request, f"Card Exchanged Successfully!!")
                            return redirect("gttWhot_game_room_page")
                        else:
                            return redirect("home_page")
                    else:\
                        return redirect("home_page")
                else:
                    return redirect("home_page")
            else:
                messages.info(request,f"Please Select Card!!!")
                return redirect("home_page")
        else:
            return redirect("home_page")
