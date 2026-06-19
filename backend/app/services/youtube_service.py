def upload_to_youtube(video_path: str, channel_id: int) -> dict:
    return {
        "status": "queued",
        "video_path": video_path,
        "channel_id": channel_id,
    }
