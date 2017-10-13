import random
from xworld_task import XWorldTask

"""
This file implements an xworld teaching task.
The task class contains several stage functions.

Each stage function must return three outputs:

next_stage  - the name of the next stage function
reward      - the reward of the current stage
sentence    - the sentence generated by the current stage

Finally, the function get_stage_names() return all the stage functions the
user wants to register.
"""

class XWorldNavTarget(XWorldTask):
    def __init__(self, env):
        super(XWorldNavTarget, self).__init__(env)
        self.target_location = (-1, -1)

    def idle(self):
        """
        Start a task
        """
        goals = self.env.get_goals()
        assert len(goals) > 0, "there is no goal on the map!"
        sel_goal = random.choice(goals)
        self.target_location = sel_goal.loc;
        self.cfg.bind("S -> start")
        self.cfg.bind("G -> '" + sel_goal.name + "'")
        return ["reward", 0.0, self.cfg.generate()]

    def reward(self):
        """
        Giving reward to the agent
        """
        agent, _, _ = self.env.get_agent()
        reward = XWorldTask.time_penalty
        next_stage = "reward" # self loop
        sentence = ""
        if agent.loc == self.target_location:
            reward += XWorldTask.correct_reward # correct goal
            next_stage = "idle" # task end
            self.cfg.bind("S -> end")
            sentece = self.cfg.generate()
            self.record_success()
        return [next_stage, reward, sentence]

    def get_stage_names(self):
        """
        return all the stage names; does not have to be in order
        """
        return ["idle", "reward"]

    def _define_grammar(self):
        all_goal_names = self.env.get_all_possible_names("goal")
        all_goal_names = "|".join(["'" + g + "'" for g in all_goal_names])
        grammar_str = """
        S -> end | start
        start -> 'Please' 'go' 'to' 'the' G '.'
        end -> 'Well' 'done' '!'
        G -> %s
        """ % all_goal_names
        return grammar_str, "S"