import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action

from django.contrib.auth.models import User

def create_action(user: User, verb: str, target=None) -> bool:
    # check for any similar action made in the last minute.
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id,
                                            verb= verb,
                                            created__gte=last_minute)
    
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct,
                                                 target_id=target.id)
    
    if not similar_actions:
        # No exsiting action found for this action.
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    
    return False