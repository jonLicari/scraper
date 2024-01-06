import pandas as pd
import pytest

from main import FilteredTable


@pytest.fixture
def sample_data():
    return {"A": [1, 2, 3], "B": ["X", "Y", "Z"]}


def test_initialization(sample_data):
    ft = FilteredTable(columns=sample_data.keys())
    assert isinstance(ft, pd.DataFrame)
    assert ft.columns.tolist() == list(sample_data.keys())


def test_assign_row(sample_data):
    ft = FilteredTable(columns=sample_data.keys())
    row_data = [4, "W"]
    ft.assign_row(row=row_data, index=0)
    assert ft.iloc[0].tolist() == row_data


def test_inheritance():
    ft = FilteredTable()
    assert isinstance(ft, pd.DataFrame)


def test_edge_cases():
    empty_ft = FilteredTable()
    assert len(empty_ft) == 0


def test_type_checking():
    with pytest.raises(TypeError):
        FilteredTable(columns="InvalidType")


def test_assign_row_with_negative_index():
    ft = FilteredTable()
    row_data = [4, "W"]
    with pytest.raises(IndexError):
        ft.assign_row(row=row_data, index=-1)
