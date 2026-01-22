"""
Khanon Charoenphanupong
663040475-1
P1
"""

from room import Bedroom, Kitchen

bedroom = Bedroom(length=12, width=10, bed_size=5)
print(bedroom.describe_room())
print("Bedroom area:", bedroom.calculate_area())
print("Bed size (ft):", bedroom.bed_size)
print("Recommended lighting:", bedroom.get_recommended_lighting(), "lumens/sq ft")
print()

kitchen_with_island = Kitchen(length=15, width=12, has_island=True)
print(kitchen_with_island.describe_room())
print("Kitchen area:", kitchen_with_island.calculate_area())
print("Recommended lighting:", kitchen_with_island.get_recommended_lighting(), "lumens/sq ft")

island_area, wall_area = kitchen_with_island.calculate_counter_space()
print("Island counter area:", island_area)
print("Wall counter area:", wall_area)
print()

kitchen_no_island = Kitchen(length=15, width=12, has_island=False)
print(kitchen_no_island.describe_room())

island_area, wall_area = kitchen_no_island.calculate_counter_space()
print("Island counter area:", island_area)
print("Wall counter area:", wall_area)
