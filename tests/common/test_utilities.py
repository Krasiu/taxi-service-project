import pytest

from common.schemas import Coordinates
from common.utilities import calculate_manhattan_distance


@pytest.mark.parametrize(
    ("coordinates1", "coordinates2", "expected_manhattan_distance"),
    [
        (Coordinates(x=0, y=0), Coordinates(x=0, y=1), 1),
        (Coordinates(x=0, y=0), Coordinates(x=1, y=1), 2),
        (Coordinates(x=1, y=1), Coordinates(x=4, y=5), 7),
        (Coordinates(x=0, y=0), Coordinates(x=10, y=10), 20),
    ],
)
def test_calculate_manhattan_distance(
    coordinates1: Coordinates, coordinates2: Coordinates, expected_manhattan_distance: int
) -> None:
    # when
    manhattan_distance = calculate_manhattan_distance(coordinates1, coordinates2)

    # then
    assert manhattan_distance == expected_manhattan_distance
