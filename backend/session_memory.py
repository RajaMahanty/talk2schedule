proposed_slot = None

def set_proposed_slot(start, end):
    global proposed_slot
    proposed_slot = (start, end)

def get_proposed_slot():
    return proposed_slot

def clear_proposed_slot():
    global proposed_slot
    proposed_slot = None
