import unittest
from types import SimpleNamespace
from unittest.mock import patch

from app.services.transcription import transcribe_audio


class TranscriptionTests(unittest.TestCase):
    def test_transcription_uses_vad_and_returns_detected_language(self):
        class Model:
            def transcribe(self, path, **options):
                self.path = path
                self.options = options
                return [SimpleNamespace(text="hello world")], SimpleNamespace(language="en")

        model = Model()
        with patch("app.services.transcription.get_model", return_value=model):
            result = transcribe_audio("sample.wav")

        self.assertTrue(model.options["vad_filter"])
        self.assertEqual(model.options["beam_size"], 5)
        self.assertEqual(result, {"text": "hello world", "language": "en"})


if __name__ == "__main__":
    unittest.main()
