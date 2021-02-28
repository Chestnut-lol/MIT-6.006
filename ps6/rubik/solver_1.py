# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 14:16:51 2021

@author: LH
"""

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
    
    Q = [start] # first in, first out queue for forward expansion
    R = [end] # first in, first out queue for backward expansion
    
    count = 0
    found = None
    while count < 6000:
        # forward expansion
        current_state = Q.pop() # dequeue 
        for twist in rubik.quarter_twists: # explore current_state
            state = rubik.perm_apply(twist, current_state)
            if state not in parent:
                parent[state] = (current_state, twist)
                Q = [state] + Q
        # forward expansion done once
        
        # if end node is found
        if end in parent:
            return [parent[end][1]]
        
        # backward expansion
        current_state = R.pop() # dequeue
        for twist in rubik.quarter_twists:
            state = rubik.perm_apply(rubik.perm_inverse(twist), current_state)
            if state not in child:
                child[state] = (current_state, twist)
                R = [state] + R
            if state in parent:
                found = state
                break
                
        # backward expansion done once
        if found is not None:
            break
        count += 1
    
    if found is None:
        return None
    
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
    
    
