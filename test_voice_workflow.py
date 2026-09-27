import unittest
from types import SimpleNamespace
from unittest.mock import patch

from app.schemas.voice_notes import VoiceNoteResponse
from app.services.voice_ai_service import generate_voice_insights
from app.services.voice_matching_service import match_voice_note
from app.services.transcription import transcribe_audio


class VoiceWorkflowTests(unittest.TestCase):
    def test_matching_returns_goal_and_confidence(self):
        goal = SimpleNamespace(
            id=7,
            domain="Speech",
            short_term_goal="Use words",
            long_term_goal="Speak clearly",
        )
        result = match_voice_note("speech use words", [goal])
        self.assertEqual(result["goal_id"], 7)
        self.assertGreater(result["confidence"], 0)
        self.assertEqual(result["title"], "Use words")

    def test_insights_have_explicit_fallback_content(self):
        result = generate_voice_insights("child said hello", "Speech", "Use words")
        self.assertIn("ai_summary", result)
        self.assertIn("ai_suggestion", result)
        self.assertTrue(result["ai_summary"])
        self.assertTrue(result["ai_suggestion"])

    def test_transcription_success_and_language(self):
        segments = [SimpleNamespace(text="hello"), SimpleNamespace(text="world")]
        info = SimpleNamespace(language="en")
        fake_model = SimpleNamespace(transcribe=lambda path, **kwargs: (segments, info))
        with patch("app.services.transcription.get_model", return_value=fake_model):
            result = transcribe_audio("sample.wav")
        self.assertEqual(result, {"text": "hello world", "language": "en"})

    def test_transcription_failure_is_propagated_for_api_cleanup(self):
        fake_model = SimpleNamespace(
            transcribe=lambda path, **kwargs: (_ for _ in ()).throw(RuntimeError("decoder failed"))
        )
        with patch("app.services.transcription.get_model", return_value=fake_model):
            with self.assertRaises(RuntimeError):
                transcribe_audio("sample.wav")

    def test_response_contract_contains_voice_workflow_fields(self):
        payload = {
            "id": 1,
            "child_id": 2,
            "parent_id": 3,
            "goal_id": 7,
            "domain": "Speech",
            "confidence": 80,
            "audio_path": "uploads/audio/example.wav",
            "language": "en",
            "transcribed_text": "hello",
            "ai_match_status": "MATCHED",
            "therapist_review": "Good progress",
            "ai_summary": "Speech observation recorded.",
            "ai_suggestion": "Continue practice.",
            "review_status": "REVIEWED",
            "therapist_comment": "Good progress",
            "created_at": "2026-09-23T00:00:00",
        }
        model = VoiceNoteResponse.model_validate(payload)
        self.assertEqual(model.ai_suggestion, "Continue practice.")
        self.assertEqual(model.review_status, "REVIEWED")


if __name__ == "__main__":
    unittest.main()
