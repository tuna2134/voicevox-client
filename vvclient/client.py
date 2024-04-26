# vvclient - client.py

from typing import Optional

from .http import HTTPClient
from .audio_query import AudioQuery


class Client:
    """VOICEVOX Engine client
    
    Parameters
    ----------
    base_uri : str
        Base URI of the VOICEVOX Engine"""
    def __init__(self, base_uri: str = "http://localhost:50021") -> None:
        self.http = HTTPClient(base_uri)

    async def __aenter__(self) -> "Client":
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def close(self) -> None:
        await self.http.close()

    async def create_audio_query(
        self, text: str, speaker: int, *, core_version: Optional[str] = None
    ) -> AudioQuery:
        """
        Create audio query

        Parameters
        ----------
        text: str
            Voice text
        speaker: int
            speaker type
        core_version: Optional[str]
            voicevox_core version

        Returns
        -------
        audio_query: AudioQuery
            Audio query
        """
        params = {"text": text, "speaker": speaker}
        if core_version:
            params["core_version"] = core_version
        return AudioQuery(self.http, await self.http.create_audio_query(params))

    async def fetch_engine_version(self) -> str:
        "Show VOICEVOX Engine version"
        return await self.http.engine_version()

    async def fetch_core_versions(self) -> List[str]:
        return await self.http.core_versions()
