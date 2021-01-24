from django.contrib.auth.models import User as AuthUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from markdownx.models import MarkdownxField

from .users import User


class Event(models.Model):
    class QualifyingType(models.IntegerChoices):
        HIGHEST_SCORE = 1
        HIGHEST_3_SCORES = 2

    name = models.CharField(max_length=64)
    slug = models.SlugField(db_index=True)
    qualifying_type = models.IntegerField(choices=QualifyingType.choices)
    qualifying_open = models.BooleanField(default=False)
    qualifying_instructions = MarkdownxField(blank=True)
    event_info = MarkdownxField(blank=True)

    def is_user_eligible(self, user):
        return self.user_ineligible_reason(user) is None

    # Returns the reason a user is ineligible to qualify for this event. Returns None if they are
    # eligible.
    def user_ineligible_reason(self, user):
        if not self.qualifying_open:
            return "closed"
        if not user:
            return "logged_out"
        if Qualifier.objects.filter(event=self, user=user).exists():
            return "already_qualified"
        if not hasattr(user, "twitch_user"):
            return "link_twitch"
        if not hasattr(user, "discord_user"):
            return "link_discord"
        return None

    @property
    def form_class(self):
        from classic_tetris_project.private.forms import qualify as qualify_forms
        if self.qualifying_type == self.QualifyingType.HIGHEST_SCORE:
            return qualify_forms.HighestScoreForm
        elif self.qualifying_type == self.QualifyingType.HIGHEST_3_SCORES:
            return qualify_forms.Highest3ScoresForm
        else:
            raise Exception("invalid qualifying type")

    def get_absolute_url(self):
        return reverse("event:index", args=[self.slug])

    def __str__(self):
        return self.name


class Qualifier(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    event = models.ForeignKey(Event, related_name="qualifiers", on_delete=models.CASCADE)
    qualifying_type = models.IntegerField(choices=Event.QualifyingType.choices)
    qualifying_score = models.IntegerField()
    qualifying_data = models.JSONField()
    vod = models.URLField()
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    approved = models.BooleanField(default=None, null=True)
    reviewed_at = models.DateTimeField(null=True)
    reviewed_by = models.ForeignKey(AuthUser, on_delete=models.SET_NULL, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["event", "user"],
                                    name="unique_event_user"),
        ]

    def __str__(self):
        return f"{self.user.display_name} ({self.event.name})"