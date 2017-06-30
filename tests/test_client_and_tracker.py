from unittest.mock import MagicMock


# noinspection PyTypeChecker
from common.tvshow import TVShow
from tracker.tveebot_tracker.episode_manager import EpisodeManager
from tracker.tveebot_tracker.tracker import Tracker
from tracker.tveebot_tracker.tracker_service import TrackerService
from tracker_cli.tveebot_tracker_cli.client import Client


class TestClient:

    def test_AddsANewTVShow_TVShowIsListedInTheTrackedList(self, tmpdir):

        source = MagicMock()
        prison_break = TVShow('Prison Break', '801')
        source.get_tvshow.return_value = prison_break
        manager = EpisodeManager(str(tmpdir.join("episodes.db")))
        tracker = Tracker(source, manager, downloader=None)
        service = TrackerService(tracker, bind_address=('localhost', 31014))
        service.start()

        client = Client('http://localhost:31014')
        added_tvshow = client.add_tvshow('801')

        assert prison_break == added_tvshow
        assert prison_break in client.tvshows()

        service.stop()
        service.join()

    def test_RemovesATVShow_TVShowIsNotListedInTheTrackedList(self, tmpdir):

        source = MagicMock()
        prison_break = TVShow('Prison Break', '801')
        source.get_tvshow.return_value = prison_break
        manager = EpisodeManager(str(tmpdir.join("episodes.db")))
        tracker = Tracker(source, manager, downloader=None)
        service = TrackerService(tracker, bind_address=('localhost', 31014))
        service.start()
        service.add_tvshow('801')

        client = Client('http://localhost:31014')
        client.remove_tvshow('801')

        assert prison_break not in client.tvshows()

        service.stop()
        service.join()
