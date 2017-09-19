# INPUT ERROR
JSON_NOT_FOUND_400 = {
    "text": "JSON is required."
}

USER_ID_NOT_FOUND_400 = {
    "text": "user_id is required"
}

GROUP_NAME_NOT_FOUND_400 = {
    "text": "name is required"
}

GROUP_ID_NOT_FOUND_400 = {
    "text": "group_id is required"
}

EVENT_ID_NOT_FOUND_400 = {
    "text": "event_id is required"
}

START_DATE_NOT_FOUND_400 = {
    "text": "start_date is required and it must be integer"
}

END_DATE_NOT_FOUND_400 = {
    "text": "end_date is required and it must be integer"
}

START_DATE_LATER_THAN_END_DATE_400 = {
    "text": "start_date can't be later than end_date"
}

# QUERY ERROR
USER_NOT_FOUND_404 = {
    "text": "User of id {} is not found"
}

GROUP_NOT_FOUND_404 = {
    "text": "Group of id {} is not found"
}

EVENT_NOT_FOUND_404 = {
    "text": "Event of id {} is not found"
}

# AUTHORIZATION ERROR
USER_NOT_GROUP_CREATOR_301 = {
    "text": "User of id {user_id} is not the owner of group {group_id}"
}

USER_NOT_IN_GROUP_301 = {
    "text": "User {user_id} is not in group {group_id}"
}

EVENT_NOT_FROM_THIS_GROUP_301 = {
    "text": "Event {event_id} is not from group {group_id}"
}
