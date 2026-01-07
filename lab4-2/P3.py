"""
Khanon Charoenphanupong
663040475-1
Lab 4-2
P3
"""

from videogame import VideoGame

p1 = VideoGame("Hero123", "Ninja")
p2 = VideoGame("Mage01", "Wizard")

p1.collect_coins(10)
p1.fight_monster("Slime", 2)
p1.fight_monster("Orc", 3)

print(p1.get_stats())
print("Rank:", VideoGame.get_rank_title(p1.level))

print("----------------")

party = VideoGame.create_party(["Doc1", "Doc2"], "Doctor")
print("Party members:")
for p in party:
    print(p.player_name)

print("----------------")

VideoGame.get_server_stats()
VideoGame.get_leaderboard()
