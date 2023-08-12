import json
from pathlib import Path
from unittest.mock import mock_open, patch

from src.utils import (
    Elem,
    generate_video_meta,
    get_cookies,
    get_source_files,
    prep_directories,
    split_openai_output,
)


class TestUtils:
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps([{"name": "cookie_name", "value": "cookie_value"}]),
    )
    def test_get_cookies(self, mock_file):
        cookies = get_cookies()
        assert "cookie_name" in cookies
        assert cookies["cookie_name"] == "cookie_value"

    def test_get_source_files(self):
        source_dir = "test_dir"
        f_names = [
            "file1.txt",
            "file2.TXT",
            "file3.jpg",
            "directory",
        ]
        path_objects = list(map(Path, f_names))
        with patch("pathlib.Path.iterdir", return_value=path_objects):
            files = get_source_files(source_dir)
            assert files == [Path("file1.txt"), Path("file2.TXT")]

    def test_split_openai_output(self):
        raw_text = (
            "TITLE: Title Text "
            "### TEXT: Text ### QUERY: Query Text "
            "### TEXT: Text 2 ### QUERY: Query Text 2 "
            "### DESCRIPTION: Description Text"
        )
        elements = split_openai_output(raw_text)
        assert len(elements) == 6
        assert elements[0] == Elem("title", "Title Text")
        assert elements[1] == Elem("text", "Text", 0.4)
        assert elements[2] == Elem("query", "Query Text")
        assert elements[3] == Elem("text", "Text 2", 0.6)
        assert elements[4] == Elem("query", "Query Text 2")
        assert elements[5] == Elem("description", "Description Text")

    def test_generate_video_meta(self, tmpdir):
        splitted_output = [
            Elem("title", "Title Text"),
            Elem("description", "Description Text"),
            Elem("text", "Content Text"),
        ]
        file_output_dir = tmpdir.mkdir("test_output_dir")
        generate_video_meta(splitted_output, str(file_output_dir))
        assert (file_output_dir / "meta.txt").read_text(
            encoding="UTF-8"
        ) == "Title Text\n\nDescription Text"
        assert (file_output_dir / "video_text.txt").read_text(
            encoding="UTF-8"
        ) == "Content Text"

    @patch("os.makedirs")
    def test_prep_directories(self, mock_makedirs):
        prep_directories()
        assert mock_makedirs.call_count == 2
