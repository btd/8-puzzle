#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from collections import deque
import heapq
import time
#import resource

N = 3
GOAL = tuple(range(0, N * N))

def row(index):
    return int(index / N)

def col(index):
    return int(index % N)

def manhattan_distance(state):
    s = 0
    for i in range(0, N * N):
        v = state[i]
        if v != 0:
            s += abs(row(i) - row(v)) + abs(col(i) - col(v))

    return s


# print('Goal', GOAL)
class Cons:
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

        self.size = tail.size + 1

    def __repr__(self):
        s = repr(self.head)
        tail = self.tail
        while tail != Nil:
            s += ' :: '
            s += repr(tail.head)
            tail = tail.tail
        s += ' :: Nil'
        return s

    def __len__(self):
        return self.size

    def to_list(self):
        l = [self.head]
        tail = self.tail
        while tail != Nil:
            l.append(tail.head)
            tail = tail.tail
        return l


class NilCons:
    def __init__(self):
        self.size = 0;

    def __repr__(self):
        return 'Nil'

    def __len__(self):
        return self.size

    def to_list(self):
        return []

Nil = NilCons()

class State:
    def __init__(self, data, emptyIndex, history = Nil):
        self.history = history
        self.data = data
        self.emptyIndex = emptyIndex

    def __repr__(self):
        if self.history:
            return '%s: %r' % (self.history[-1], self.data)

        return str(self.data)

    def nextStates(self):
        data = self.data
        history = self.history

        emptySpaceIndex = self.emptyIndex

        emptySpaceRow = int(emptySpaceIndex / N)
        emptySpaceCol = int(emptySpaceIndex % N)

        newStates = list()

        if emptySpaceRow != 0:
            newData = list(data)
            newData[emptySpaceIndex], newData[emptySpaceIndex - N] = newData[emptySpaceIndex - N], newData[
                emptySpaceIndex]

            newStates.append(State(tuple(newData), emptySpaceIndex - N, Cons('Up', history)))

        if emptySpaceRow != N - 1:
            newData = list(data)
            newData[emptySpaceIndex], newData[emptySpaceIndex + N] = newData[emptySpaceIndex + N], newData[
                emptySpaceIndex]

            newStates.append(State(tuple(newData), emptySpaceIndex + N, Cons('Down', history)))

        if emptySpaceCol != 0:
            newData = list(data)
            newData[emptySpaceIndex], newData[emptySpaceIndex - 1] = newData[emptySpaceIndex - 1], newData[
                emptySpaceIndex]

            newStates.append(State(tuple(newData), emptySpaceIndex - 1, Cons('Left', history)))

        if emptySpaceCol != N - 1:
            newData = list(data)
            newData[emptySpaceIndex], newData[emptySpaceIndex + 1] = newData[emptySpaceIndex + 1], newData[
                emptySpaceIndex]

            newStates.append(State(tuple(newData), emptySpaceIndex + 1,  Cons('Right', history)))

        return newStates

    def isFinal(self):
        return self.data == GOAL

    def __lt__(self, other):
        return self.distance() < other.distance()

    def distance(self):
        return manhattan_distance(self.data) + len(self.history)


def bfs(initialState):
    states = deque([initialState])

    statesSet = {initialState.data}
    explored = set()

    maxFringeSize = 0
    maxSearchDepth = 0

    while len(states) != 0:
        fringeSize = len(states)
        if maxFringeSize < fringeSize:
            maxFringeSize = fringeSize

        # print('fringeSize', fringeSize)
        state = states.popleft()
        statesSet.discard(state.data)
        explored.add(state.data)

        searchDepth = len(state.history)
        if maxSearchDepth < searchDepth:
            maxSearchDepth = searchDepth

        # print('Current state', state)
        if state.isFinal():
            return {
                'path_to_goal': state.history,
                'cost_of_path': len(state.history),
                'nodes_expanded': len(explored) - 1,
                'fringe_size': fringeSize - 1,
                'max_fringe_size': maxFringeSize,
                'search_depth': searchDepth,
                'max_search_depth': maxSearchDepth + 1
            }

        nextStates = [x for x in state.nextStates() if x.data not in explored and x.data not in statesSet]
        # print('nextStates', nextStates)

        for s in nextStates:
            statesSet.add(s.data)
            states.append(s)


def dfs(initialState):
    states = [initialState]

    statesSet = {initialState.data}
    explored = set()

    maxFringeSize = 0
    maxSearchDepth = 0

    while len(states) != 0:
        fringeSize = len(states)
        if maxFringeSize < fringeSize:
            maxFringeSize = fringeSize

        # print('fringeSize', fringeSize)
        state = states.pop()
        statesSet.discard(state.data)
        explored.add(state.data)

        searchDepth = len(state.history)
        if maxSearchDepth < searchDepth:
            maxSearchDepth = searchDepth

        # print('Current state', state)
        if state.isFinal():
            return {
                'path_to_goal': state.history,
                'cost_of_path': len(state.history),
                'nodes_expanded': len(explored) - 1,
                'fringe_size': fringeSize - 1,
                'max_fringe_size': maxFringeSize,
                'search_depth': searchDepth,
                'max_search_depth': maxSearchDepth
            }

        nextStates = [x for x in state.nextStates()[::-1] if x.data not in explored and x.data not in statesSet]
        # print('nextStates', nextStates)

        for s in nextStates:
            statesSet.add(s.data)
            states.append(s)


def ast(initialState):
    states = []
    heapq.heappush(states, initialState)

    statesSet = {initialState.data}
    explored = set()

    maxFringeSize = 0
    maxSearchDepth = 0

    while len(states) != 0:
        fringeSize = len(states)
        if maxFringeSize < fringeSize:
            maxFringeSize = fringeSize

        # print('fringeSize', fringeSize)
        state = heapq.heappop(states)
        if state.data in explored:
            continue

        statesSet.discard(state.data)
        explored.add(state.data)


        searchDepth = len(state.history)
        if maxSearchDepth < searchDepth:
            maxSearchDepth = searchDepth

        # print('Current state', state)
        if state.isFinal():
            return {
                'path_to_goal': state.history,
                'cost_of_path': len(state.history),
                'nodes_expanded': len(explored) - 1,
                'fringe_size': fringeSize - 1,
                'max_fringe_size': maxFringeSize,
                'search_depth': searchDepth,
                'max_search_depth': maxSearchDepth
            }

        nextStates = [x for x in state.nextStates()[::-1] if x.data not in explored]
        # print('nextStates', nextStates)

        for s in nextStates:
            statesSet.add(s.data)
            heapq.heappush(states, s)


def ida(initialState):
    limit = initialState.distance()
    while True:
        print('Try search with limit ' + str(limit))
        newLimit, result = dls(initialState, limit)
        if result != None:
            return result

        limit = newLimit

def dls(initialState, limit):
    states = [initialState]

    statesSet = {initialState.data}
    explored = set()

    maxFringeSize = 0
    maxSearchDepth = 0


    minDistance = sys.maxint

    while len(states) != 0:
        fringeSize = len(states)
        if maxFringeSize < fringeSize:
            maxFringeSize = fringeSize

        # print('fringeSize', fringeSize)
        state = states.pop()
        statesSet.discard(state.data)
        explored.add(state.data)

        searchDepth = len(state.history)
        if maxSearchDepth < searchDepth:
            maxSearchDepth = searchDepth

        distance = state.distance()

        if distance > limit:
            #print('State limit exceed ' + str(distance) + ' > ' + str(limit))
            if distance < minDistance:
                minDistance = distance

            continue

        # print('Current state', state)
        if state.isFinal():
            return (None, {
                'path_to_goal': state.history,
                'cost_of_path': len(state.history),
                'nodes_expanded': len(explored) - 1,
                'fringe_size': fringeSize - 1,
                'max_fringe_size': maxFringeSize,
                'search_depth': searchDepth,
                'max_search_depth': maxSearchDepth
            })

        nextStates = [x for x in state.nextStates()[::-1] if x.data not in explored and x.data not in statesSet]
        # print('nextStates', nextStates)

        for s in nextStates:
            statesSet.add(s.data)
            states.append(s)

    #print('Not found, will try new limit')
    return (minDistance, None)


if __name__ == "__main__":
    start_time = time.time()
    [algo, initialState] = sys.argv[1:]
    state = tuple([int(x) for x in initialState.split(',')])
    emptyIndex = state.index(0)

    state = State(state, emptyIndex)

    if algo == 'bfs':
        result = bfs(state)

    if algo == 'dfs':
        result = dfs(state)

    if algo == 'ast':
        result = ast(state)

    if algo == 'ida':
        result = ida(state)

    end_time = time.time()

    print(algo)
    print(result)

    if result:

        with open('output.txt', 'w') as f:
            path = result['path_to_goal'].to_list()
            path.reverse()
            f.write('path_to_goal: %r\n' % path)
            f.write('cost_of_path: %r\n' % result['cost_of_path'])
            f.write('nodes_expanded: %r\n' % result['nodes_expanded'])
            f.write('fringe_size: %r\n' % result['fringe_size'])
            f.write('max_fringe_size: %r\n' % result['max_fringe_size'])
            f.write('search_depth: %r\n' % result['search_depth'])
            f.write('max_search_depth: %r\n' % result['max_search_depth'])
            f.write('running_time: %r\n' % (end_time - start_time))
            #f.write('max_ram_usage: %r\n' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
