from django.db import models
from datetime import datetime

# Create your models here.

class All_Gtt_Whot_Cards(models.Model):
    card_number = models.CharField(max_length=100,null=True,blank=True)
    card_shape = models.CharField(max_length=100,null=True,blank=True)
    card_image = models.ImageField(upload_to="All_Gtt_Whot_Cards",null=True,blank=True)
    has_power = models.BooleanField(default=False,null=True,blank=True)
    requirement = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return f"{self.card_number}...{self.card_shape}"


class Gtt_Whot(models.Model):
    game_time = models.IntegerField(default=30, null=True, blank=True)
    general_market = models.ManyToManyField(All_Gtt_Whot_Cards,blank=True,related_name="General_Market")
    current_card = models.ManyToManyField(All_Gtt_Whot_Cards,blank=True,related_name="Current_Card")
    number_of_general_market = models.CharField(max_length=100,null=True,blank=True)
    player_one = models.CharField(max_length=100,null=True,blank=True)
    player_one_cards = models.ManyToManyField(All_Gtt_Whot_Cards,blank=True,related_name="Player_One")
    player_one_number_of_cards = models.CharField(max_length=1000,null=True,blank=True)
    player_two = models.CharField(max_length=100,null=True,blank=True)
    player_two_cards = models.ManyToManyField(All_Gtt_Whot_Cards,blank=True,related_name="Player_Two")
    player_two_number_of_cards = models.CharField(max_length=1000,null=True,blank=True)
    game_charges = models.IntegerField(default=0,null=True,blank=True)
    user_can_play = models.BooleanField(default=True,null=True,blank=True)
    to_play = models.CharField(max_length=1000,null=True,blank=True)
    game_reload = models.BooleanField(default=False,null=True,blank=True)
    required_to_pick = models.BooleanField(default=False,null=True,blank=True)
    hold_on = models.BooleanField(default=False,null=True,blank=True)
    how_many_required_to_pick = models.IntegerField(default=0,null=True,blank=True)
    player_required_to_pick = models.CharField(max_length=1000,null=True,blank=True)
    has_tie = models.BooleanField(default=False,null=True,blank=True)
    game_finished = models.BooleanField(default=False,null=True,blank=True)
    game_concluded = models.BooleanField(default=False,null=True,blank=True)
    game_winner = models.CharField(max_length=1000,null=True,blank=True)
    counted_cards = models.BooleanField(default=False,null=True,blank=True)
    player_one_amount_of_cards = models.IntegerField(default=0,null=True,blank=True)
    player_two_amount_of_cards = models.IntegerField(default=0, null=True, blank=True)
    player_won = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return f"{self.player_one} VS {self.player_two}"


class Special_Member(models.Model):
    username = models.CharField(max_length=100,null=True,blank=True)
    opponent = models.CharField(max_length=100,null=True,blank=True)
    game_id = models.IntegerField(default=0,null=True,blank=True)
    user_card = models.CharField(max_length=100,null=True,blank=True)
    exchanged_card = models.CharField(max_length=100,null=True,blank=True)
    challenge_stake_amount = models.CharField(max_length=100,null=True,blank=True)
    challenge_winning_amount = models.CharField(max_length=100,null=True,blank=True)
    time = models.DateTimeField(default=datetime.now,null=True,blank=True)

    def __str__(self):
        return f"{self.username}"