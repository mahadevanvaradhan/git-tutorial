import io
import sys
import pandas as pd
import pytest
from developer_two.third import explore_csv

@pytest.fixture
def sample_csv(tmp_path):
    data = (
        "name,age,score\n"
        "Alice,30,85.5\n"
        "Bob,25,90.0\n"
        "Charlie,,78.0\n"
    )
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text(data)
    return str(csv_file)

def test_explore_csv_output(sample_csv, capsys):
    explore_csv(sample_csv)
    captured = capsys.readouterr().out

    assert "Shape: (3, 3)" in captured
    assert "Columns: ['name', 'age', 'score']" in captured
    assert "Data Types:" in captured
    assert "Missing Values:" in captured
    assert "Summary Statistics:" in captured
    assert "First 5 Rows:" in captured
    assert "Alice" in captured
    assert "Charlie" in captured

def test_explore_csv_with_missing_values(tmp_path, capsys):
    data = (
        "a,b,c\n"
        "1,2,3\n"
        "4,,6\n"
        "7,8,\n"
    )
    csv_file = tmp_path / "missing.csv"
    csv_file.write_text(data)
    explore_csv(str(csv_file))
    captured = capsys.readouterr().out
    assert "Missing Values:" in captured
    assert "b    1" in captured
    assert "c    1" in captured

# To run the tests, use the following command in your terminal:
# pytest developer_two/test_third.py