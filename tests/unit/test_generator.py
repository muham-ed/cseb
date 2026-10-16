"""Unit tests for synthetic template generator."""
from __future__ import annotations

from src.generation.template_generator import generate, _DOMAINS


def test_generator_determinism():
    """Test that generator produces identical output for the same seed."""
    run1 = generate(10, seed=42)
    run2 = generate(10, seed=42)

    assert len(run1) == 10
    assert len(run2) == 10

    for p1, p2 in zip(run1, run2):
        assert p1.program_id == p2.program_id
        assert p1.domain == p2.domain
        assert p1.source == p2.source
        assert p1.expected_output == p2.expected_output


def test_generated_program_validity():
    """Test that all generated programs have valid non-empty fields."""
    programs = generate(20, seed=123)
    assert len(programs) == 20

    for p in programs:
        assert p.program_id.isalnum()
        assert p.domain in _DOMAINS
        assert len(p.source.strip()) > 0
        assert len(p.expected_output.strip()) > 0
        assert "IDENTIFICATION DIVISION" in p.source
