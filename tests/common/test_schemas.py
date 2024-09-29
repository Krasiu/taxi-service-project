import pytest
from pydantic import ValidationError

from common.schemas import Coordinates


@pytest.mark.parametrize(("x", "y"), [(-1, 0), (0, -1), (101, 50), (50, 101), (-1, 101), (101, -1)])
def test_Coordinates_x_and_y_outside_allowed_range(x: int, y: int) -> None:
    with pytest.raises(ValidationError):
        Coordinates(x=x, y=y)


@pytest.mark.parametrize(("x", "y"), [(0, 100), (100, 0), (50, 10), (10, 50), (99, 77), (77, 99)])
def test_Coordinates_x_and_y_within_allowed_range(x: int, y: int) -> None:
    assert Coordinates(x=x, y=y)
