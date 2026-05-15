from cognition.models import CognitionFrame
from django.db import models
from common.models import Log


class BehaviorOption(models.Model):
    """
    Model for storing Xabsl Options e.g.
    option search_ball
    {
        <states here>
    }
    Each log could have a different implementation of the behavior while the names of the options are still the same
    TODO: deduplicate later if we can determine logs to from the same commit without changes in working tree
    """
    log = models.ForeignKey(
        Log, on_delete=models.CASCADE, related_name="behavior_options"
    )
    # xabsl_internal_option_id depends on the order it appears in the BehaviorStateComplete representation in the log
    # we need this to get the actual option id during insertion of BehaviorStateSparse
    # lookup looks like this: client.list(log_id=log_id, xabsl_internal_id=<id in BehaviorStateSparse>)
    xabsl_internal_option_id = models.IntegerField(blank=True, null=True)
    option_name = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return f"{self.log}-{self.option_name}"


class BehaviorOptionState(models.Model):
    """
    Model for storing Xabsl States e.g.
    option walk_forward
    {
        initial state idle{
            decision{}
            action{}
        }
        state forward{
            decision {}
            action{}
        }
        target state stand{
            decision{}
            action{}
        }
    }
    """

    log = models.ForeignKey(
        Log, on_delete=models.CASCADE, related_name="behavior_options_states"
    )
    # e.g. forward in the example
    name = models.CharField(max_length=40, blank=True, null=True)
    # id of option walk_forward for the given log 
    option = models.ForeignKey(
        BehaviorOption, on_delete=models.CASCADE, related_name="behavior_options_states"
    )
    # state id within an option - this is the id BehaviorFrameOption.activeState refers to
    xabsl_internal_state_id = models.IntegerField(blank=True, null=True)
    # wether the state is a target state e.g stand state would be a target state in the example
    target = models.BooleanField(blank=True, null=True)
    # TODO: can we figure out if a state is an initial state?

    def __str__(self):
        return f"{self.log}-{self.name}"


class BehaviorFrameOption(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="behavior_frame_option"
    )
    option = models.ForeignKey(
        BehaviorOption, on_delete=models.CASCADE, related_name="behavior_frame_option"
    )
    active_state = models.ForeignKey(
        BehaviorOptionState,
        on_delete=models.CASCADE,
        related_name="behavior_frame_option",
    )

    # parent can't be a foreign key for now because we identify the root option with -1.
    # TODO add root option with id -1 => would mean we manually need to create the id column and handle the primary key behavior
    # parent = models.ForeignKey(BehaviorOption,to_field='id', on_delete=models.CASCADE, related_name='behavior_frame_options_parent')
    # parent = models.IntegerField(blank=True, null=True)
    # frame = models.IntegerField(blank=True, null=True)
    # time = models.IntegerField(blank=True, null=True)
    # time_of_execution = models.IntegerField(blank=True, null=True)
    # state_time = models.IntegerField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["frame", "option"]),
        ]
        unique_together = ("option", "frame", "active_state")


class XabslSymbolComplete(models.Model):
    log = models.OneToOneField(
        Log,
        on_delete=models.CASCADE,
        related_name="xabsl_symbol_complete",
        primary_key=True,
    )
    data = models.JSONField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["log"]),
        ]
        verbose_name_plural = "XabslSymbolComplete"


class XabslSymbolSparse(models.Model):
    frame = models.ForeignKey(
        CognitionFrame, on_delete=models.CASCADE, related_name="xabsl_symbol_sparse"
    )
    data = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "XabslSymbolSparse"
        constraints = [
            models.UniqueConstraint(
                fields=["frame"], name="unique_frame_id_xabslsymbolsparse"
            )
        ]
