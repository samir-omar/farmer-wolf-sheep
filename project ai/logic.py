# logic.py
class GameLogic:
    def __init__(self):
        # الحالة: المزارع، الذئب، الخروف، الكرنب (0 لليسار، 1 لليمين)
        self.state = {'farmer': 0, 'wolf': 0, 'sheep': 0, 'cabbage': 0}

    def is_valid(self, state):
        # الذئب مع الخروف بدون المزارع
        if state['wolf'] == state['sheep'] and state['farmer'] != state['wolf']:
            return False
        # الخروف مع الكرنب بدون المزارع
        if state['sheep'] == state['cabbage'] and state['farmer'] != state['sheep']:
            return False
        return True

    def is_win(self, state):
        return all(v == 1 for v in state.values())