from alm.lyrics import lyrics_extractor as lec

def test_extractor(file_path: str):
    lyrics_notes_map = lec.extract_lyrics(file_path)
    print(lyrics_notes_map)

test_extractor("tests/files/unpopular/人_S2.xml")