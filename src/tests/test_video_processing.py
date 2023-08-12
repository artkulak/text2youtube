from unittest.mock import Mock, patch

from src.video_processing import (
    Elem,
    Video,
    download_storyblocks_video,
    get_storyblocks_video_urls,
    save_storyblocks,
    save_videos,
)


class TestVideoFunctions:
    @patch(
        "src.video_processing.get",
        return_value=Mock(status_code=200, json=lambda: {"data": {"stockItems": []}}),
    )
    def test_get_storyblocks_video_urls_empty(self, mock_get):
        cookies = {}
        result = get_storyblocks_video_urls(["query"], 5, cookies)
        assert result == []

    @patch(
        "src.video_processing.get",
        return_value=Mock(
            status_code=200,
            json=lambda: {
                "data": {
                    "stockItems": [
                        {
                            "stockItem": {"title": "Video 1", "duration": 10},
                            "stockItemFormats": [{"downloadUrl": "/download/123"}],
                        }
                    ]
                }
            },
        ),
    )
    @patch(
        "src.video_processing.sample",
        return_value=[Video("Video 1", 10, "https://www.storyblocks.com/download/123")],
    )
    def test_get_storyblocks_video_urls(self, mock_sample, mock_get):
        cookies = {}
        result = get_storyblocks_video_urls(["query"], 1, cookies)
        assert len(result) == 1
        assert result[0].title == "Video 1"
        assert result[0].duration == 10
        assert result[0].url == "https://www.storyblocks.com/download/123"

    @patch("src.video_processing.get_storyblocks_video_urls", return_value=[])
    @patch("src.video_processing.download_yt_video")
    def test_save_storyblocks_no_videos(
        self, mock_download_yt_video, mock_get_storyblocks_video_urls
    ):
        cookies = {}
        save_storyblocks(cookies, 10, "output_dir", 1, "query")
        mock_download_yt_video.assert_called_once_with(10, "output_dir", 1, "query")

    @patch(
        "src.video_processing.get_storyblocks_video_urls",
        return_value=[Video("Video 1", 10, "https://www.storyblocks.com/download/123")],
    )
    @patch("src.video_processing.download_storyblocks_video")
    def test_save_storyblocks_with_videos(
        self, mock_download_storyblocks_video, mock_get_storyblocks_video_urls
    ):
        cookies = {}
        save_storyblocks(cookies, 10, "output_dir", 1, "query")
        mock_download_storyblocks_video.assert_called_once_with(
            "https://www.storyblocks.com/download/123",
            cookies,
            "output_dir/videos/1_0.mp4",
        )

    @patch(
        "src.video_processing.get",
        return_value=Mock(status_code=200, content=b"video_content"),
    )
    def test_download_storyblocks_video(self, mock_get, tmpdir):
        cookies = {}
        output_path = tmpdir.join("video.mp4")

        download_storyblocks_video(
            "https://www.storyblocks.com/download/123", cookies, str(output_path)
        )

        mock_get.assert_called_once_with(
            "https://www.storyblocks.com/download/123", cookies=cookies
        )

        assert output_path.exists()

        with open(output_path, "rb") as f:
            content = f.read()
        assert content == b"video_content"

    @patch("src.video_processing.download_yt_video")
    @patch("src.video_processing.save_storyblocks")
    def test_save_videos_by_storyblocks(
        self, mock_save_storyblocks: Mock, mock_download_yt_video
    ):
        elements = [
            Elem("text", "text1", 0.3),
            Elem("query", "query_text"),
            Elem("text", "text2", 0.2),
            Elem("query", "query_text2"),
        ]
        total_duration = 20.0
        cookies = {}
        yt_proba = -1
        save_videos(elements, total_duration, "output_dir", cookies, yt_proba)
        mock_download_yt_video.assert_not_called()
        mock_save_storyblocks.assert_called_with(
            {}, 4.0, "output_dir", 1, "query_text2"
        )
        assert mock_save_storyblocks.call_count == 2

    @patch("src.video_processing.download_yt_video")
    @patch("src.video_processing.save_storyblocks")
    def test_save_videos_by_storyblocks(
        self, mock_save_storyblocks: Mock, mock_download_yt_video
    ):
        elements = [
            Elem("text", "text1", 0.3),
            Elem("query", "query_text"),
            Elem("text", "text2", 0.2),
            Elem("query", "query_text2"),
        ]
        total_duration = 20.0
        cookies = {}
        yt_proba = 100
        save_videos(elements, total_duration, "output_dir", cookies, yt_proba)
        mock_save_storyblocks.assert_not_called()
        mock_download_yt_video.assert_called_with(4.0, "output_dir", 1, "query_text2")
        assert mock_download_yt_video.call_count == 2
