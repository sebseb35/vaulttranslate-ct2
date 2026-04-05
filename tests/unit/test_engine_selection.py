from pathlib import Path

from packages.core.engine_selection import select_engine
from packages.core.mock_engine import MockTranslatorEngine


def test_select_engine_defaults_to_mock() -> None:
    engine = select_engine(model_path=None)
    assert isinstance(engine, MockTranslatorEngine)


def test_select_engine_builds_ct2_when_model_path_is_provided(
    monkeypatch,
    tmp_path: Path,
) -> None:
    captured: dict[str, object] = {}

    class _FakeCt2Engine:
        def __init__(
            self,
            model_path: str,
            *,
            inter_threads: int,
            intra_threads: int,
            compute_type: str,
        ) -> None:
            captured["model_path"] = model_path
            captured["inter_threads"] = inter_threads
            captured["intra_threads"] = intra_threads
            captured["compute_type"] = compute_type

    monkeypatch.setattr(
        "packages.core.engine_selection.CTranslate2TranslatorEngine",
        _FakeCt2Engine,
    )

    model_dir = tmp_path / "ct2-model"
    model_dir.mkdir()
    engine = select_engine(
        model_path=model_dir,
        inter_threads=2,
        intra_threads=4,
        compute_type="int8",
    )

    assert isinstance(engine, _FakeCt2Engine)
    assert captured == {
        "model_path": str(model_dir),
        "inter_threads": 2,
        "intra_threads": 4,
        "compute_type": "int8",
    }

