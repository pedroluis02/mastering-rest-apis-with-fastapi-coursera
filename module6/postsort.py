from enum import Enum


class UserPostSorting(str, Enum):
    new = "new"
    old = "old"
    most_likes = "most_likes"
