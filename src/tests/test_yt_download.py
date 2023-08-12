from unittest.mock import MagicMock, Mock, patch

from src.yt_download import download_yt_video, get_clips, get_random_subclip_start_times


class TestDownloadYTVideo:
    @patch("src.yt_download._search_and_dl_yt_video", autospec=True)
    @patch("src.yt_download.get_clips", autospec=True)
    def test_download_yt_video(self, mock_get_clips, mock_search_and_dl):
        credentials = Mock()
        file_output_dir = "output_dir"
        n_paragraph = 1
        query = "test_query"

        download_yt_video(7, file_output_dir, n_paragraph, query)

        mock_search_and_dl.assert_called_once_with(
            query, f"{file_output_dir}/videos/yt"
        )
        mock_get_clips.assert_called_once_with(
            mock_search_and_dl.return_value, 1, 7, file_output_dir, n_paragraph
        )


class TestGetClips:
    @patch(
        "src.yt_download.get_random_subclip_start_times",
        return_value=[10, 20, 30],
        autospec=True,
    )
    @patch("src.yt_download.VideoFileClip", autospec=True)
    def test_get_clips(self, mock_video_clip, mock_random_subclip_start_times):
        mock_video_clip.return_value.__enter__.return_value = (
            mock_video_clip_cm
        ) = MagicMock(duration=60)
        mock_video_clip_cm.subclip.__enter__.return_value = (
            mock_subclip_cm
        ) = MagicMock()
        mock_subclip_cm.write_videofile.return_value = MagicMock()

        get_clips("test_video.mp4", 3, 7, "output_dir", 1)

        mock_video_clip.assert_called_once_with("test_video.mp4")
        mock_random_subclip_start_times.assert_called_once_with(
            mock_video_clip_cm, 3, 7
        )

        assert mock_video_clip_cm.subclip.call_count == 3


class TestGetRandomSubclipStartTimes:
    def test_get_random_subclip_start_times(self):
        clip_instance = Mock()
        clip_instance.duration = 100
        n_clips = 5
        clips_duration = 7

        start_times = get_random_subclip_start_times(
            clip_instance, n_clips, clips_duration
        )

        assert len(start_times) == n_clips
        assert all(
            [
                start_times[i] + clips_duration <= start_times[i + 1]
                for i in range(n_clips - 1)
            ]
        )
