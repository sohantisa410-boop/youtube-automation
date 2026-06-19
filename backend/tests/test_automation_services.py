from app.services.automation import (
    generate_script,
    generate_seo,
    generate_thumbnail,
    generate_video_asset,
    generate_voice,
)


def test_local_automation_outputs_are_deterministic():
    script = generate_script("retention", "education")
    title, description = generate_seo("retention")

    assert script == (
        "Today we are covering retention in the education niche with practical "
        "insights."
    )
    assert title == "retention: Complete Automation Guide"
    assert "retention" in description
    assert generate_voice(script) == "storage/videos/voice_sample.mp3"
    assert generate_video_asset() == "storage/videos/video_sample.mp4"
    assert generate_thumbnail() == "storage/thumbnails/thumb_sample.png"
