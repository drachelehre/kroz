import gym
from gym import spaces
import numpy as np
from player import Player  # Import your player class
from monster import Monster  # Import your monster class


class GameEnv(gym.Env):
    def __init__(self):
        super(GameEnv, self).__init__()

        # Define action space: Strike, Defend, Cast Spell, etc.
        self.action_space = spaces.Discrete(3)  # Example: 0 = Strike, 1 = Defend, 2 = Cast Spell

        # Define observation space (Player HP, MP, Enemy HP, etc.)
        self.observation_space = spaces.Box(low=0, high=100, shape=(4,), dtype=np.float32)

        # Initialize player and monster
        self.player = Player('AI_Player', 'warrior')
        self.enemy = Monster('Enemy', 'goblin')

    def reset(self):
        """Reset the environment at the start of a new episode."""
        self.player.hp = self.player.hp_max
        self.enemy.hp = self.enemy.hp_max
        return self._get_observation()

    def step(self, action):
        """Apply action and return new state, reward, and done flag."""
        if action == 0:  # Strike
            self.player.strike(self.enemy)
        elif action == 1:  # Defend
            self.player.action('defend')
        elif action == 2:  # Cast Spell (random spell for now)
            if self.player.spellbook:
                self.player.cast_spell(self.player.spellbook[0], self.enemy)

        # Calculate reward (e.g., damage dealt, surviving longer)
        reward = self.enemy.hp_max - self.enemy.hp  # Reward for damage dealt
        done = self.enemy.hp <= 0 or self.player.hp <= 0  # Episode ends if someone dies

        return self._get_observation(), reward, done, {}

    def _get_observation(self):
        """Return current state as an observation."""
        return np.array([self.player.hp, self.player.mp, self.enemy.hp, self.enemy.mp], dtype=np.float32)

