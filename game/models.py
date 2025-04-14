from django.db import models

# Create your models here.

class GTT(models.Model):
    game_amount = models.IntegerField(default=0,null=True,blank=True)
    game_round = models.IntegerField(default=1,null=True,blank=True)
    player_one = models.CharField(max_length=1000,null=True,blank=True)
    player_two = models.CharField(max_length=1000,null=True,blank=True)
    player_one_count = models.IntegerField(default=0,null=True,blank=True)
    player_two_count = models.IntegerField(default=0,null=True, blank=True)
    to_send = models.CharField(max_length=1000,null=True,blank=True)
    has_sent = models.BooleanField(default=False,null=True,blank=True)
    to_receive = models.CharField(max_length=1000, null=True, blank=True)
    has_received = models.BooleanField(default=False,null=True,blank=True)
    receiver_number = models.IntegerField(default=0,null=True, blank=True)
    not_found_winner = models.BooleanField(default=True,null=True,blank=True)
    game_winner = models.CharField(max_length=1000,default="unknown",null=True,blank=True)
    game_charges = models.IntegerField(default=0,null=True,blank=True)
    game_wining_amount = models.IntegerField(default=0,null=True,blank=True)
    current_first_number = models.IntegerField(default=0,null=True,blank=True)
    current_game_sign = models.CharField(max_length=1000, null=True, blank=True)
    current_second_number = models.IntegerField(default=0, null=True, blank=True)
    current_golden_number = models.IntegerField(default=0, null=True, blank=True)
    current_random_number = models.IntegerField(default=0, null=True, blank=True)
    current_second_random_number = models.IntegerField(default=0, null=True, blank=True)
    current_third_random_number = models.IntegerField(default=0, null=True, blank=True)
    has_tie = models.BooleanField(default=False,null=True,blank=True)
    has_finished = models.BooleanField(default=False,null=True,blank=True)
    result_collated = models.BooleanField(default=False,null=True,blank=True)
    game_reload = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return f"{self.player_one} vs {self.player_two}...round:{self.game_round}"