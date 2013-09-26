def _get_category_score(avatar, categ, attended_events):
    idx = IndexesHolder().getById('categoryDateAll')
    attended_events_set = set(attended_events)
    # We care about events in the whole timespan where the user attended some events. However, this might result in some missed events e.g. if the user was not working for a year and then returned. So we throw away old blocks (or rather adjust the start time to the start time of the newest block)
    first_event_date = attended_events[0].getStartDate().replace(hour=0, minute=0)
    last_event_date = attended_events[-1].getStartDate().replace(hour=0, minute=0) + timedelta(days=1)
    blocks = _get_blocks(_unique_events(idx.iterateObjectsIn(
                 categ.getId(), first_event_date, last_event_date
             )), attended_events_set)
    for a, b in _window(blocks):
        # More than 3 months between blocks? Ignore the old block!
        if b[0].getStartDate() - a[-1].getStartDate() > timedelta(weeks=12):
            first_event_date = b[0].getStartDate().replace(hour=0, minute=0)

    # Favorite categories get a higher base score
    favorite = categ in avatar.getLinkTo('category', 'favorite')
    score = 1 if favorite else 0
    # Attendance percentage goes to the score directly. If the attendance is high chances are good that the user is either very interested in whatever goes on in the category or it's something he has to attend regularily.
    total = sum(1 for _ in _unique_events(idx.iterateObjectsIn(categ.getId(), first_event_date, last_event_date)))
    attended_block_event_count = sum(1 for e in attended_events_set if e.getStartDate() >= first_event_date)
    score += attended_block_event_count / total
    # If there are lots/few unattended events after the last attended one we also update the score with that
    total_after = sum(1 for _ in _unique_events(idx.iterateObjectsIn(categ.getId(), last_event_date + timedelta(days=1), None)))
    if total_after < total * 0.05:
        score += 0.25
    elif total_after > total * 0.25:
        score -= 0.5
    # Lower the score based on how long ago the last attended event was if there are no future events. We start applying this modifier only if the event has been more than 40 days in the past to avoid it from happening in case of monthly events that are not created early enough.
    days_since_last_event = (date.today() - last_event_date.date()).days
    if days_since_last_event > 40:
        score -= 0.025 * days_since_last_event
    # For events in the future however we raise the score
    now_local = utc2server(nowutc(), False)
    attending_future = [e for e in _unique_events(idx.iterateObjectsIn(categ.getId(), now_local, last_event_date)) if e in attended_events_set]
    if attending_future:
        score += 0.25 * len(attending_future)
        days_to_future_event = (attending_future[0].getStartDate().date() - date.today()).days
        score += max(0.1, -(max(0, days_to_future_event - 2) / 4) ** (1 / 3) + 2.5)
    return score
