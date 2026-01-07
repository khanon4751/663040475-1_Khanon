"""
Khanon Charoenphanupong
663040475-1
Lab 4-2 :videogames
P3
"""

from datetime import datetime

class VideoGame:
    # class attributes
    total_players = 0
    difficulty_levels = ["Easy", "Medium", "Hard"]
    max_level = 100
    server_start_time = datetime.now()
    active_players = []
    leaderboard = {}

    def __init__(self, player_name, character_type):
        if not VideoGame.is_valid_character_name(player_name):
            print("Invalid name")
            return

        self.player_name = player_name
        self.character_type = character_type
        self.level = 1
        self.health = 100
        self.exp = 0
        self.coins = 0
        self.inventory = []
        self.is_alive = True

        VideoGame.total_players += 1
        VideoGame.active_players.append(player_name)
        VideoGame.leaderboard[player_name] = 0


    # instance methods
    def level_up(self):
        if self.level < VideoGame.max_level:
            self.level += 1
            self.health = 100

        VideoGame.leaderboard[self.player_name] = self.level * 100 + self.coins
        print(self.player_name, "level up!")
        print("Level:", self.level)
        print("Health:", self.health)
        print("Score:", VideoGame.leaderboard[self.player_name])

    def collect_coins(self, amount):
        self.coins += amount
        VideoGame.leaderboard[self.player_name] = self.level * 100 + self.coins
        print(self.player_name, "coins:", self.coins)

    def take_damage(self, damage):
        self.health -= damage

        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            if self.player_name in VideoGame.active_players:
                VideoGame.active_players.remove(self.player_name)
            print(self.player_name, "is dead")
        else:
            print(self.player_name, "HP left:", self.health)

    def fight_monster(self, monster_name, monster_level):
        print(self.player_name, "fights", monster_name)

        damage = VideoGame.calculate_damage(10, 5, monster_level)
        self.take_damage(damage)

        if not self.is_alive:
            return

        self.exp += 10 * monster_level
        self.collect_coins(3 * monster_level)

        if self.exp >= VideoGame.calculate_exp_needed(self.level):
            self.exp = 0
            self.level_up()

    def get_stats(self):
        return (
            "Name: " + self.player_name +
            ", Type: " + self.character_type +
            ", Level: " + str(self.level) +
            ", HP: " + str(self.health) +
            ", Coins: " + str(self.coins) +
            ", Alive: " + str(self.is_alive)
        )


    # class methods
    @classmethod
    def create_party(cls, players, player_type):
        party = []
        for name in players:
            party.append(cls(name, player_type))
        return party

    @classmethod
    def get_server_stats(cls):
        up_time = datetime.now() - cls.server_start_time
        print("Total players:", cls.total_players)
        print("Active players:", cls.active_players)
        print("Leaderboard:", cls.leaderboard)
        print("Server up time:", up_time)

    @classmethod
    def get_leaderboard(cls):
        print("Leaderboard:")
        sorted_board = sorted(cls.leaderboard.items(), key=lambda x: x[1], reverse=True)
        for name, score in sorted_board:
            print(name, score)

    @classmethod
    def reset_server(cls):
        cls.total_players = 0
        cls.active_players = []
        cls.leaderboard = {}
        cls.server_start_time = datetime.now()


    #static methods
    @staticmethod
    def calculate_damage(attack_power, defense, level):
        damage = (attack_power * level) - defense
        if damage < 0:
            damage = 0
        return damage

    @staticmethod
    def calculate_exp_needed(level):
        return 100 * level

    @staticmethod
    def is_valid_character_name(name):
        if len(name) < 3 or len(name) > 20:
            return False
        return name.isalnum()

    @staticmethod
    def get_rank_title(level):
        if level < 20:
            return "Beginner"
        elif level < 50:
            return "Advanced"
        elif level < 80:
            return "Expert"
        else:
            return "Legend"
