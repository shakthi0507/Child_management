import os

from faster_whisper import WhisperModel


_model = None


def get_model():
    global _model
    if _model is None:
        _model = WhisperModel(
            os.getenv("WHISPER_MODEL", "base"),
            device=os.getenv("WHISPER_DEVICE", "cpu"),
            compute_type=os.getenv("WHISPER_COMPUTE_TYPE", "int8"),
        )
    return _model



def transcribe_audio(audio_path: str, language: str | None = None):


    options = {"beam_size": 5}
    if language:
        options["language"] = language

    segments, info = get_model().transcribe(

        audio_path,
        vad_filter=True,
        **options,

    )


    text = " ".join(

        segment.text

        for segment in segments

    )


    return {

        "text": text.strip(),

        "language": info.language

    }
