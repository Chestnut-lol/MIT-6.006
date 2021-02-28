import rubik

def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    
    Each move can be applied using rubik.perm_apply
    """
    if start == end:
        return []
    
    # keep track of states that have been expanded from the start
    parent = {start:None} # child_node: (parent_node, perm) 
    # where perm_apply(parent_node) = child_node
    
    # keep track of states that have been expanded from the end
    child = {end:None} # parent_node: (child_node, perm)
    # where perm_appry(parent_node) = child_node
    
    level = 1
    frontier = [start]
    backtier = [end]
    found = None
    while level <= 7:
        # expand from end
        next = []
        for current_state in backtier:
            for twist in rubik.quarter_twists:
                state = rubik.perm_apply(rubik.perm_inverse(twist), current_state)
                if state not in child:
                    child[state] = (current_state, twist)
                    next.append(state)
                if state in parent:
                    found = state
                    break
            if found:
                break
        if found:
            break
        backtier = next
        
        mext = []
        for current_state in frontier:
            for twist in rubik.quarter_twists:
                state = rubik.perm_apply(twist, current_state)
                if state not in parent:
                    parent[state] = (current_state, twist)
                    mext.append(state)
                if state in child:
                    found = state
                    break
            if found:
                break
        if found:
            break
        frontier = mext
        
        level += 1
    
    if found is None:
        return None
    else:
        result = []
        current_state = found
        while current_state != start:
            pred_pair = parent[current_state]
            result = [pred_pair[1]] + result
            current_state = pred_pair[0]
            
        current_state = found
        while current_state != end:
            succ_pair = child[current_state]
            result = result + [succ_pair[1]]
            current_state = succ_pair[0]        
    
    return result
                    