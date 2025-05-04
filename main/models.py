from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class Admin_Setup(models.Model):
    number_registered_members = models.IntegerField(default=0,null=True,blank=True)
    min_game_charges = models.IntegerField(default=50,null=True,blank=True)
    max_game_charges = models.IntegerField(default=100, null=True, blank=True)
    transfer_charges = models.IntegerField(default=100,null=True,blank=True)
    withdrawal_charges = models.IntegerField(default=100,null=True,blank=True)
    deposit_link = models.CharField(default="https://wa.me/7019462683?text=Hi%20Please%20I%20Want%20To%20Deposit",max_length=1000,null=True,blank=True)
    withdrawal_link = models.CharField(default="https://wa.me/7019462683?text=Hi%20Please%20I%20Want%20To%20Withdraw",max_length=1000,null=True,blank=True)
    no_of_golden_number_played = models.IntegerField(default=0,null=True,blank=True)
    no_of_golden_Whot_played = models.IntegerField(default=0,null=True,blank=True)
    today = models.IntegerField(default=0,null=True,blank=True)
    today_number_of_games = models.IntegerField(default=0,null=True,blank=True)
    admin_whot_game_time = models.IntegerField(default=30, null=True, blank=True)
    admin_international_registration_link = models.CharField(default="https://wa.me/7019462683?text=Hi,Not%20A%20Nigerian,%20Please%20I%20Want%20To%20Register",max_length=1000,null=True,blank=True)

    def __str__(self):
        return str(self.number_registered_members)


class Term_Condition(models.Model):
    rule = models.CharField(max_length=1000,null=True,blank=True)
    terms = models.TextField(null=True,blank=True)

    def __str__(self):
        return str(self.rule)

class About_Game(models.Model):
    step = models.CharField(max_length=1000,null=True,blank=True)
    about = models.TextField(null=True,blank=True)

    def __str__(self):
        return str(self.step)

class Available_Players(models.Model):
    username = models.CharField(max_length=1000,null=True,blank=True)
    stake_amount = models.IntegerField(default=0,null=True,blank=True)
    win_ratio = models.IntegerField(default=0,null=True,blank=True)
    game_link = models.CharField(max_length=1000,null=True,blank=True)
    gender = models.CharField(max_length=100,null=True,blank=True)
    time_available = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    game_type = models.CharField(max_length=1000,null=True,blank=True)
    chat_link = models.CharField(max_length=10000,null=True,blank=True)
    allow_player_search = models.BooleanField(default=False,null=True,blank=True)
    country = models.CharField(default="Nigeria",max_length=10000,null=True,blank=True)
    format_stake_amount = models.CharField(default=0, max_length=10000, null=True, blank=True)

    def __str__(self):
        return str(self.username)

class Transfer_History(models.Model):
    transaction_type = models.CharField(max_length=1000,null=True,blank=True)
    transaction_topic = models.CharField(max_length=1000,null=True,blank=True)
    sender_name = models.CharField(max_length=1000,null=True,blank=True)
    receiver_name = models.CharField(max_length=1000,null=True,blank=True)
    amount = models.CharField(max_length=1000,null=True,blank=True)
    charges = models.CharField(max_length=1000,null=True,blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    net_balance = models.CharField(default="Out-Dated", max_length=1000, null=True, blank=True)

    def __str__(self):
        return str(self.transaction_type)


class Challenges(models.Model):
    challenger = models.CharField(max_length=1000,null=True,blank=True)
    amount = models.IntegerField(default=0,null=True,blank=True)
    challenge_game_type = models.CharField(max_length=1000,null=True,blank=True)
    challenged = models.CharField(max_length=1000,null=True, blank=True)
    time = models.DateTimeField(default=datetime.now,null=True, blank=True)

    def __str__(self):
        return str(f"'{self.challenger}' challenges '{self.challenged}' at {self.time}")



class Game_Delay_Report(models.Model):
    reporter = models.CharField(max_length=1000,null=True,blank=True)
    report = models.CharField(max_length=1000,null=True,blank=True)
    time_reported = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(f"'{self.reporter}' Reported '{self.report}' at '{self.time_reported}' For Game Delay")






class Notifications(models.Model):
    notification_type = models.CharField(max_length=1000,null=True,blank=True)
    notification_message = models.TextField(default=None, null=True, blank=True)
    notification_time = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return str(self.notification_type)




class Leaderboard(models.Model):
    position = models.IntegerField(default=0,null=True,blank=True)
    username = models.CharField(max_length=1000,null=True,blank=True)
    game = models.CharField(max_length=1000,null=True,blank=True)
    amount = models.IntegerField(default=0,null=True,blank=True)


    def __str__(self):
        return str(self.position)



class Tournaments(models.Model):
    tournament_title = models.CharField(max_length=1000,null=True,blank=True)
    tournament_prize = models.IntegerField(default=0,null=True,blank=True)
    tournament_entry_fee = models.IntegerField(default=0,null=True,blank=True)
    number_slot = models.IntegerField(default=0,null=True,blank=True)
    number_slot_taken = models.IntegerField(default=0,null=True,blank=True)
    tournament_date = models.DateTimeField(auto_now_add=True)
    tournament_link = models.CharField(max_length=1000,null=True,blank=True)


    def __str__(self):
        return str(self.tournament_title)


class All_Messages(models.Model):
    sender = models.CharField(max_length=1000,null=True,blank=True)
    receiver = models.CharField(max_length=1000,null=True,blank=True)
    message = models.TextField(default="Hey,Let's Play Gold...",null=True,blank=True)
    is_seen = models.BooleanField(default=False,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"


class All_Chats(models.Model):
    chat_one = models.CharField(max_length=1000,null=True,blank=True)
    chat_two = models.CharField(max_length=1000,null=True,blank=True)
    messages = models.ManyToManyField(All_Messages,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_message_seen = models.BooleanField(default=False,null=True,blank=True)
    last_sender = models.CharField(max_length=1000,null=True,blank=True)

    def __str__(self):
        return f"{self.chat_one}/{self.chat_two}"



class Withdrawals(models.Model):
    user = models.CharField(max_length=1000,null=True,blank=True)
    amount = models.CharField(max_length=1000,null=True,blank=True)
    status = models.CharField(default="Pending",max_length=1000,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user}...{self.amount}"



class Members(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    initial_password = models.TextField(default=None, null=True, blank=True)
    is_special = models.BooleanField(default=False, null=True, blank=True)
    gender = models.CharField(max_length=1000,null=True,blank=True)
    country = models.TextField(default=None, null=True, blank=True)
    balance = models.FloatField(default=0,null=True,blank=True)
    number_of_play = models.IntegerField(default=0,null=True,blank=True)
    number_of_draw = models.IntegerField(default=0,null=True,blank=True)
    number_of_win = models.IntegerField(default=0,null=True,blank=True)
    number_of_loss = models.IntegerField(default=0,null=True,blank=True)
    win_ratio = models.IntegerField(default=0,null=True,blank=True)
    transaction_history = models.ManyToManyField(Transfer_History,blank=True)
    is_available = models.BooleanField(default=False,null=True,blank=True)
    available_id = models.IntegerField(default=0,null=True,blank=True)
    has_transfer = models.BooleanField(default=False,null=True,blank=True)
    admin_charge = models.FloatField(default=0,null=True,blank=True)
    user_game_link = models.CharField(max_length=1000,null=True,blank=True)
    my_challenges = models.ManyToManyField(Challenges,blank=True,related_name="My_Challenges")
    missed_challenges = models.ManyToManyField(Challenges,blank=True,related_name="Missed_Challenges")
    has_clicked_missed_challenges = models.BooleanField(default=False,null=True,blank=True)
    has_game = models.BooleanField(default=False,null=True,blank=True)
    is_challenger = models.BooleanField(default=False,null=True,blank=True)
    current_opponent = models.CharField(max_length=1000,null=True,blank=True)
    challenge_expiry_time = models.DateTimeField(null=True,blank=True)
    current_challenge_amount = models.FloatField(default=0,null=True,blank=True)
    current_game_id = models.IntegerField(default=0,null=True,blank=True)
    game_started = models.BooleanField(default=False,null=True,blank=True)
    current_game_wining_amount = models.IntegerField(default=0,null=True,blank=True)
    report_history = models.ManyToManyField(Game_Delay_Report,blank=True)
    number_of_reports = models.IntegerField(default=0,null=True,blank=True)
    is_blacklisted = models.BooleanField(default=False,null=True,blank=True)
    current_game_type = models.CharField(max_length=1000,null=True,blank=True)
    current_number_of_whott_cards = models.IntegerField(default=0,null=True,blank=True)
    shuffling_starting_game_on_progress = models.BooleanField(default=False, null=True, blank=True)
    shuffling_check = models.BooleanField(default=False, null=True, blank=True)
    notifications = models.ManyToManyField(Notifications,blank=True)
    allow_system_alert = models.BooleanField(default=True, null=True, blank=True)
    allow_missed_challenge_alert = models.BooleanField(default=True, null=True, blank=True)
    allow_tournament_alert = models.BooleanField(default=False, null=True, blank=True)
    allow_bonus_alert = models.BooleanField(default=True, null=True, blank=True)
    game_invite_privacy = models.BooleanField(default=True,max_length=1000,null=True,blank=True)
    profile_visibility_privacy = models.BooleanField(default=True,max_length=1000,null=True,blank=True)
    username_search_visibility_privacy = models.BooleanField(default=True, null=True, blank=True)
    balance_visibility_privacy = models.BooleanField(default=False, null=True, blank=True)
    can_transfer = models.BooleanField(default=True, null=True, blank=True)
    highest_win = models.IntegerField(default=0,null=True,blank=True)
    highest_loss = models.IntegerField(default=0,null=True,blank=True)
    my_chats = models.ManyToManyField(All_Chats,blank=True)
    current_room_id = models.IntegerField(default=0,null=True,blank=True)
    deposit_in_progress = models.BooleanField(default=False, null=True, blank=True)
    allow_game_reload = models.BooleanField(default=True, null=True, blank=True)
    my_withdrawals = models.ManyToManyField(Withdrawals,blank=True)


    def __str__(self):
        return str(self.user)





