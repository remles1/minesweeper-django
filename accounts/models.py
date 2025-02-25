from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from minesweeper.models import Game


class ProfileModel(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)

    beginner_best_game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='beginner_best_game', blank=True, null=True)
    beginner_wins = models.IntegerField()

    intermediate_best_game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='intermediate_best_game', blank=True, null=True)
    intermediate_wins = models.IntegerField()

    expert_best_game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='expert_best_game', blank=True, null=True)
    expert_wins = models.IntegerField()


@receiver(post_save, sender=Game)
def update_profile_on_game_save(sender, instance, **kwargs):
    player = instance.player
    profile_model_from_db = ProfileModel.objects.get(player=player)

    difficulty = instance.difficulty
    best_game_field = f"{difficulty}_best_game"
    wins_field = f"{difficulty}_wins"

    current_best_game = getattr(profile_model_from_db, best_game_field)
    current_wins = getattr(profile_model_from_db, wins_field)

    if current_best_game is None or instance.time_spent < current_best_game.time_spent:
        setattr(profile_model_from_db, best_game_field, instance)

    setattr(profile_model_from_db, wins_field, current_wins + 1)
    profile_model_from_db.save()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.get_or_create(
            player=instance,
            defaults={
                'beginner_best_game': None,
                'beginner_wins': 0,
                'intermediate_best_game': None,
                'intermediate_wins': 0,
                'expert_best_game': None,
                'expert_wins': 0,
            }
        )
