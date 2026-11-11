from buildings import create_house, create_producer
from models import Kind, State

STARTING_STATE = State(
    (24, 4, 12, 3, 0, 0),
    (
        create_producer(Kind.CENTER, deletable=True),
        create_house(residents=8, deletable=True),
        create_house(residents=8, deletable=True),
        create_house(residents=8, deletable=True),
        create_producer(Kind.FISHER, deletable=True),
        create_producer(Kind.LUMBER, deletable=True),
    ),
)