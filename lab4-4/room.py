"""
Khanon Charoenphanupong
663040475-1
room
"""

from abc import ABC, abstractmethod


class Room(ABC):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    @abstractmethod
    def get_purpose(self):
        """Returns a string describing purposes of the room"""
        pass

    @abstractmethod
    def get_recommended_lighting(self):
        """Returns recommended lighting in lumens per square foot"""
        pass

    def calculate_area(self):
        return self.length * self.width

    def describe_room(self):
        area = self.calculate_area()
        return f"A {self.__class__.__name__} of {area} sq ft used for {self.get_purpose()}"


class Bedroom(Room):
    def __init__(self, length, width, bed_size):
        super().__init__(length, width)
        self.bed_size = bed_size

    def get_purpose(self):
        return "sleeping and relaxation"

    def get_recommended_lighting(self):
        return 15 


class Kitchen(Room):
    def __init__(self, length, width, has_island=True):
        super().__init__(length, width)
        self.has_island = has_island

    def get_purpose(self):
        return "cooking and food preparation"

    def get_recommended_lighting(self):
        return 35

    def calculate_counter_space(self):
        """
        Calculates the counter space areas for the kitchen.

        Returns:
            tuple: (island_counter_area, wall_counter_area) in square feet
        """
        area = self.calculate_area()

        if self.has_island:
            island_counter = area * 1 / 5
            wall_counter = area * 1 / 4
        else:
            island_counter = 0
            wall_counter = area * 1 / 2

        return island_counter, wall_counter
