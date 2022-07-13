from dataclasses import dataclass, field

@dataclass(order=True)
class Poet:

    first_name: str
    last_name: str
    bio: str
    poems: list
    quotes: list
    sort_index: int = field(init=False, repr=False)

    def __post_init__(self):
        self.sort_index = self.last_name

@dataclass
class Poem:

    title: str
    poem: str