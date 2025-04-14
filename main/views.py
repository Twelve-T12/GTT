from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Members, Available_Players, Transfer_History,Challenges,Admin_Setup,About_Game,Term_Condition,All_Phone_Numbers
import datetime
from datetime import datetime as d
from django.core.mail import EmailMessage
from django.conf import settings


# home_page
class Home(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=user_id)
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
                return render(request,"index.html",context)
        else:
            return redirect("login_page")

class Profile(View):
    def get(self,request,user):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=user_id)
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
                member_first_name = request.user.first_name
                member_last_name = request.user.last_name
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
                member_phone_number = get_member.phone_number
                context = {
                    "username": username,
                    "first_name":member_first_name,
                    "last_name":member_last_name,
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
                    "phone_number":member_phone_number
                }
                return render(request,"profile.html",context)
        else:
            return redirect("login_page")


class Settings(View):
    def get(self,request,user):
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
            get_member = Members.objects.get(id=user_id)
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
            return redirect("login_page")


class Search_Player(View):
    def post(self,request):
        player_name = request.POST["player_name"].lower()
        if Available_Players.objects.filter(username=player_name).exists():
            print(player_name)
            get_user_id = int(User.objects.get(username=player_name).id)
            get_member_availability_id = Members.objects.get(id=get_user_id).available_id
            get_member_availability_details = Available_Players.objects.get(id=get_member_availability_id)
            data = {
                "player_name":player_name,
                "member_stake_amount":get_member_availability_details.stake_amount,
                "member_win_ratio":get_member_availability_details.win_ratio,
                "member_game_link":get_member_availability_details.game_link,
                "member_whatsapp_link":get_member_availability_details.whatsapp_link,
                "member_gender":get_member_availability_details.gender,
                "member_time_available":get_member_availability_details.time_available
            }
            return JsonResponse(data)
        else:
            print(False)
            return HttpResponse(f"Unavailable")


class About(View):
    def get(self,request):
        context = {
            "about_game":About_Game.objects.all()
        }
        return render(request,"about.html",context)

class Register(View):
    def get(self,request):
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
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"].lower()
        gender = request.POST["gender"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if not All_Phone_Numbers.objects.filter(phone_number=phone_number).exists():
                    if password == confirm_password:
                        create_new_user = User.objects.create_user(
                            first_name = first_name,
                            last_name = last_name,
                            username = username,
                            email = email,
                            password = password
                        )
                        new_member = Members.objects.create(
                            user = create_new_user,
                            initial_password = password,
                            gender = gender,
                            phone_number=phone_number,
                            user_game_link = f"/play/{username}/amount"
                        )
                        #updating number registered
                        get_number_registered = int(Admin_Setup.objects.get(id=1).number_registered_members)
                        new_registered_member = get_number_registered + 1
                        update_new_register = Admin_Setup.objects.filter(id=1).update(
                            number_registered_members = new_registered_member
                        )

                        # add phone number
                        add_phone_number = All_Phone_Numbers.objects.create(
                            username=username,
                            phone_number=phone_number
                        )

                        # logging in user directly
                        user = auth.authenticate(
                            username=username,
                            password=password
                        )
                        accept = auth.login(request, user)

                        get_user_id = User.objects.get(username=username).id
                        #Create Credit Transaction
                        new_credit_transaction = Transfer_History.objects.create(
                            transaction_type = "Credit",
                            sender_name = "Register Bonus",
                            amount = 200
                        )
                        #Getting And Updating Member
                        get_member = Members.objects.get(id=int(get_user_id))
                        update_member_transfer_history = get_member.transaction_history.add(new_credit_transaction)
                        update_member = Members.objects.filter(id=int(get_user_id)).update(
                            has_transfer = True
                        )
                        messages.success(request, f"You received #200 sign up bonus")
                        return redirect("home_page")
                    else:
                        messages.error(request,"password does not match")
                        return redirect("register_page")
                else:
                    messages.error(request, f"{phone_number} already exists")
                    return redirect("register_page")
            else:
                messages.error(request,f"{email} already exists")
                return redirect("register_page")
        else:
            messages.error(request,f"{username} already exists")
            return redirect("register_page")


class Available_Settings(View):
    def post(self,request,user):
        if request.user.is_authenticated:
            game_type = request.POST["game_type"]
            stake_amount = int(request.POST["stake_amount"])
            user_id = request.user.id
            get_member = Members.objects.get(id=user_id)
            member_balance = get_member.balance
            if not Available_Players.objects.filter(username=user).exists():
                if stake_amount >= 200:
                    if stake_amount <= member_balance:
                        member_gender = get_member.gender
                        member_win_ratio = get_member.win_ratio
                        member_phone_number = get_member.phone_number
                        get_user_whatsapp_number = "234" + member_phone_number[1:]
                        get_user_whatsapp_link = f"https://wa.me/{get_user_whatsapp_number}?text=Hi {get_member},I%20Am%20An%20Opponent%20From%20GTT%20,Are%20You%20Ready%20To%20Have%20A%20Match%20Now?"
                        member_game_link = f"play/{user}/amount/{stake_amount}/{game_type}"
                        update_member_game_link = Members.objects.filter(id=user_id).update(
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
                            whatsapp_link=get_user_whatsapp_link
                        )

                        # updating member availability
                        available_id = Available_Players.objects.get(username=user).id
                        update_player_availability = Members.objects.filter(id=user_id).update(
                            is_available=True,
                            available_id=available_id
                        )
                        messages.success(request,"Now Available")
                        return redirect("home_page")
                    else:
                        messages.info(request,f"Insufficient Balance")
                        return redirect(f"/{user}/settings")
                else:
                    messages.info(request, f"Minimum Stake Amount is #200")
                    return redirect(f"/{user}/settings")
            else:
                messages.info(request, f"Already Available")
                return redirect(f"home_page")
        else:
            return redirect("login_page")


class Unavailable_Settings(View):
    def post(self,request,user):
        if request.user.is_authenticated:
            user_id = request.user.id
            if Available_Players.objects.filter(username=user).exists():
                get_user = Available_Players.objects.get(username=user).id
                remove_payer = Available_Players.objects.filter(id=get_user).delete()

                update_user = Members.objects.filter(id=user_id).update(
                    is_available = False
                )
                messages.success(request,f"{user} now unavailable")
            else:
                messages.success(request, f"{user} not available")
            return redirect("home_page")
        else:
            return redirect("login_page")


class Transfer(View):
    def post(self,request,user):
        if request.user.is_authenticated:
            receiver_username = request.POST["receiver_name"].lower()
            if User.objects.filter(username=receiver_username).exists():
                if request.user.username != receiver_username:
                    amount = int(request.POST["amount"])
                    user_id = request.user.id
                    get_member = Members.objects.get(id=user_id)
                    member_balance = get_member.balance
                    charges = int(Admin_Setup.objects.get(id=1).transfer_charges)
                    checking_remaining_balance = member_balance - charges - amount
                    if checking_remaining_balance > 0:
                        get_receiver_user = User.objects.get(username=receiver_username)
                        receiver_id = get_receiver_user.id
                        receiver_first_name = get_receiver_user.first_name
                        receiver_last_name = get_receiver_user.last_name
                        receiver_email = get_receiver_user.email
                        get_receiver = Members.objects.get(id=receiver_id)
                        receiver_gender = get_receiver.gender
                        format_amount = "{:,}".format(amount)
                        admin_charges = charges
                        format_charges = "{:,}".format(admin_charges)
                        context = {
                            "receiver_gender":receiver_gender,
                            "receiver_username":receiver_username,
                            "receiver_first_name":receiver_first_name,
                            "receiver_last_name":receiver_last_name,
                            "receiver_email":receiver_email,
                            "amount":amount,
                            "charges":admin_charges,
                            "gender":receiver_gender,
                            "format_amount":format_amount,
                            "format_charges":format_charges
                        }
                        return render(request,"transfer.html",context)
                    else:
                        messages.info(request,f"not enough balance")
                        return redirect(f"/{user}/settings")
                else:
                    messages.info(request,f"Transfer Not Accepted...{request.user.username} to {user}")
                    return redirect("home_page")
            else:
                messages.info(request, f"{receiver_username} not found")
                return redirect("home_page")
        else:
            return redirect("login_page")

class Confirm_Transfer(View):
    def post(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            receiver_username = request.POST["receiver_username"]
            amount = int(request.POST["amount"])
            charges = int(request.POST["charges"])
            format_amount = "{:,}".format(amount)
            format_charges = "{:,}".format(charges)
            #getting receiver
            get_receiver_id = User.objects.get(username=receiver_username).id
            get_receiver = Members.objects.get(id=get_receiver_id)
            receiver_balance = int(get_receiver.balance)
            increase_receiver_balance = int(receiver_balance + amount)
            update_receiver = Members.objects.filter(id=get_receiver_id).update(
                balance = increase_receiver_balance,
                has_transfer = True
            )
            #Updating Transaction History
            create_credit_transaction = Transfer_History.objects.create(
                transaction_type = "Credit",
                sender_name = request.user.username,
                receiver_name = receiver_username,
                amount = format_amount,
                charges = format_charges,
                net_balance="{:,}".format(increase_receiver_balance)
            )
            #adding transaction to receiver
            add_credit_transaction = get_receiver.transaction_history.add(create_credit_transaction)

            #setting sender
            user_id = request.user.id
            get_member = Members.objects.get(id=user_id)
            member_balance = int(get_member.balance)
            member_admin_charge = get_member.admin_charge
            new_admin_charges = int(member_admin_charge + charges)
            decrease_sender_balance = member_balance - amount - charges
            update_sender = Members.objects.filter(id=user_id).update(
                balance = decrease_sender_balance,
                has_transfer = True,
                admin_charge = new_admin_charges
            )
            #Update Transaction History
            create_debit_transaction = Transfer_History.objects.create(
                transaction_type = "Debit",
                sender_name = request.user.username,
                receiver_name = receiver_username,
                amount = format_amount,
                charges = format_charges,
                net_balance="{:,}".format(decrease_sender_balance)
            )
            #add debit transaction
            add_debit_transaction = get_member.transaction_history.add(create_debit_transaction)
            messages.success(request,f"#{format_amount} sent to {receiver_username} Successfully!!")
            return redirect("home_page")
        else:
            return redirect("login_page")

class Player_Connection(View):
    def get(self,request,user,amount,game_type):
        if request.user.is_authenticated:
            if User.objects.filter(username=user).exists():
                if user != request.user.username:
                    get_challenged_id = User.objects.get(username=user).id
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
                                    get_challenged = Members.objects.get(id=get_challenged_id).my_challenges
                                    add_challenge = get_challenged.add(create_challenge)
                                    messages.success(request,f"Request Sent To '{user}'...Waiting For '{user}' Response,If No Respoonse In 30 Seconds '{user}' Probably Declined Or '{user}' Is Not Online. ")
                                    return redirect("home_page")
                                else:
                                    messages.info(request,f"{user} Not Available")
                                    return redirect("home_page")
                            else:
                                messages.info(request,f"Please Make Sure You are Available!!!")
                                return redirect("home_page")
                        else:
                            messages.info(request,f"user already in a game")
                            return redirect("home_page")
                    else:
                        messages.info(request,f"Insufficient Fund")
                        return redirect("home_page")
                else:
                    messages.info(request,f"Can't connect to You")
                    return redirect("home_page")
            else:
                messages.info(request,f"{user} not recognized")
                return redirect("home_page")
        else:
            return redirect("login_page")

class Challenge(View):
    def get(self,request,user):
        if request.user.is_authenticated:
            user_id = request.user.id
            get_member = Members.objects.get(id=user_id)
            member_challenges = get_member.my_challenges.all()
            now = datetime.datetime.now()
            today = datetime.datetime.today()
            for i in member_challenges:
                extra_time = datetime.timedelta(seconds=10) + i.time
                if extra_time > now:
                    return JsonResponse({"challenges": list(member_challenges.values())})
                else:
                    challenge_id = i.id
                    remove_challenge = get_member.my_challenges.remove(challenge_id)
                    add_missed_challenges = get_member.missed_challenges.add(challenge_id)
                    update_member_has_clicked_missed_challenges = Members.objects.filter(id=user_id).update(
                        has_clicked_missed_challenges = False
                    )
            return JsonResponse({"challenges": list(member_challenges.values())})
        else:
            return redirect("login_page")

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

class Accept_Challenge(View):
    def post(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            challenge_id = int(request.POST["challenge_id"])
            challenger_username = request.POST["username"]
            amount = int(request.POST["amount"])
            challenge_game_type = request.POST["game_challenge_type"]
            get_member = Members.objects.get(id=user_id)
            member_balance = int(get_member.balance)
            get_challenger_id = int(User.objects.get(username=challenger_username).id)
            check_challenger_available  = Members.objects.get(id=get_challenger_id).is_available
            check_challenged_available = Members.objects.get(id=user_id).is_available
            if check_challenged_available and check_challenger_available:
                if member_balance >= amount:
                    get_challenge_time = Challenges.objects.get(id=challenge_id).time
                    additional_time = datetime.timedelta(seconds=20)
                    challenge_expiry_time = get_challenge_time + additional_time

                    #updating challenger
                    get_challenger_id = int(User.objects.get(username=challenger_username).id)
                    remove_challenger_available_players = Available_Players.objects.filter(username=challenger_username).delete()
                    update_challenger = Members.objects.filter(id=get_challenger_id).update(
                        has_game = True,
                        current_opponent = request.user.username,
                        challenge_expiry_time = challenge_expiry_time,
                        is_challenger = True,
                        current_challenge_amount = amount,
                        is_available = False,
                        current_game_type = challenge_game_type
                    )

                    #update challenged
                    remove_challenged_available_players = Available_Players.objects.filter(
                        username=request.user.username).delete()
                    update_challenged = Members.objects.filter(id=user_id).update(
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
                messages.info(request,f"Insufficient Balance")
                return redirect("home_page")
            else:
                messages.info(request,f"Connection Broken")
                return redirect("home_page")
        else:
            return redirect("login_page")



class Decline_Challenge(View):
    def post(self,request):
        if request.user.is_authenticated:
            challenge_id = int(request.POST["challenge_id"])
            challenger_username = request.POST["username"]
            amount = int(request.POST["amount"])

            # removing challenge
            user_id = request.user.id
            get_member = Members.objects.get(id=user_id)
            member_challenge = get_member.my_challenges.remove(challenge_id)

            # deleting challenge
            delete_challenge = Challenges.objects.filter(id=challenge_id).delete()
            return HttpResponse("Challenge Decline")
        else:
            return redirect("login_page")

class Has_Challenge(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_id = request.user.id
            has_challenge = Members.objects.get(id=user_id).has_game
            return HttpResponse(has_challenge)
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
            elif get_member_current_game == "Golden Whot":
                return redirect("/gttWhott/gttWhott")
        else:
            return redirect("home_page")

class Terms_Conditions(View):
    def get(self,request):
        context = {
            "terms":Term_Condition.objects.all()
        }
        return render(request,"terms_conditions.html",context)



class Ajax_Check_Member_Gtt_Whot_Shuffle_Cards_In_Progress(View):
    def get(self, request):
        if request.user.is_authenticated:
            user_id = request.user.id
            get_member = Members.objects.get(id=user_id)
            has_shuffled = get_member.shuffling_check
            return HttpResponse(has_shuffled)
        else:
            return redirect("login_page")


class Ajax_Update_Member_Gtt_Whot_Shuffle_Cards_In_Progress(View):
    def get(self, request,challenger,challenge):
        if request.user.is_authenticated:
            user_id = request.user.id
            update_member = Members.objects.filter(id=int(user_id)).update(
                shuffling_check = True
            )
            get_member_opponent_id = User.objects.get(username=challenge).id
            update_mem_opp = Members.objects.filter(id=int(get_member_opponent_id)).update(
                shuffling_check =True
            )
            print("Updated Shuffle")
            return HttpResponse(True)
        else:
            return redirect("login_page")






class Login(View):
    def get(self,request):
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
            return redirect("home_page")
        else:
            messages.error(request,"Invalid Details")
            return redirect("login_page")

class Logout(View):
    def get(self,request):
        logout = auth.logout(request)
        return redirect("home_page")


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

