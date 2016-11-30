# -*- coding:utf-8 -*-
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import HMMmodule.char_state_tab as state
import HMMmodule.prob_trans as trans
import HMMmodule.prob_start as init
import HMMmodule.prob_emit as emit

MIN_FLOAT = -3.14e100
MIN_INF = float("-inf")

def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]  # tabular
    mem_path = [{}]
    all_states = trans_p.keys()
    for y in states.get(obs[0], all_states):  # init
        V[0][y] = start_p[y] + emit_p[y].get(obs[0], MIN_FLOAT)
        mem_path[0][y] = ''
    for t in xrange(1, len(obs)):
        V.append({})
        mem_path.append({})
        #prev_states = get_top_states(V[t-1])
        prev_states = [
            x for x in mem_path[t - 1].keys() if len(trans_p[x]) > 0]

        prev_states_expect_next = set(
            (y for x in prev_states for y in trans_p[x].keys()))
        obs_states = set(
            states.get(obs[t], all_states)) & prev_states_expect_next

        if not obs_states:
            obs_states = prev_states_expect_next if prev_states_expect_next else all_states

        for y in obs_states:
            prob, state = max((V[t - 1][y0] + trans_p[y0].get(y, MIN_INF) +
                               emit_p[y].get(obs[t], MIN_FLOAT), y0) for y0 in prev_states)
            V[t][y] = prob
            mem_path[t][y] = state

    last = [(V[-1][y], y) for y in mem_path[-1].keys()]
    # if len(last)==0:
    #     print obs
    prob, state = max(last)

    route = [None] * len(obs)
    i = len(obs) - 1
    while i >= 0:
        route[i] = state
        state = mem_path[i][state]
        i -= 1
    return (prob, route)

def HMMCut(sentence):
    p,r = viterbi(sentence,state.P,init.P,trans.P,emit.P)
    # print r
    line = ''
    s = -1
    isword = False
    for i in xrange(len(r)):
        if r[i][0] == u'S':
            if isword:
                line += sentence[s:i + 1]
                line += " "
                isword = False
                continue
            line += sentence[i]
            line += " "
        if r[i][0] == u'B':
            s = i
            isword = True
        elif r[i][0] == u'E':
            line += sentence[s:i+1]
            line += " "
            isword = False
    if r[-1][0] == u'B' or r[-1][0] == u'M':
        line += sentence[s:i+1]
    line = line.strip()
    return line

if __name__ == "__main__":
    print HMMCut(u"中文")