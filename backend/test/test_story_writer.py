from backend.schemas.story import StoryRequest
from backend.services.story_writer import generate_story

def test_story_writer():
    request = StoryRequest(
        title="The Hidden Forest",
        genre="Adventure",
        outline="A young girl discovers a magical forest and uncovers its secrets."
    )
    response = generate_story(request)
    assert isinstance(response.story, str)
    assert len(response.story) > 50
