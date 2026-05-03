# ai_solver.py
from collections import deque

def get_solutions(initial_state, logic_checker):
    queue = deque([(initial_state, [])])
    visited = set()

    while queue:
        (current, path) = queue.popleft()
        state_tuple = tuple(current.items())
        
        if state_tuple in visited: continue
        visited.add(state_tuple)

        if logic_checker.is_win(current): return path + [current]

        # تجربة نقل كل عنصر متاح مع المزارع
        possible_moves = ['farmer', 'wolf', 'sheep', 'cabbage']
        for item in possible_moves:
            if item == 'farmer' or current[item] == current['farmer']:
                new_state = current.copy()
                new_state['farmer'] = 1 - current['farmer']
                if item != 'farmer':
                    new_state[item] = 1 - current[item]
                
                if logic_checker.is_valid(new_state):
                    queue.append((new_state, path + [current]))
    return None