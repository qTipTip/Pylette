"""
Smoke test for Pylette library.
Tests basic functionality to ensure the library works correctly after installation.

This is here because I've pushed changes twice now that broke the library... :(
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

import pylette


def make_test_image(w: int = 64, h: int = 64) -> Image.Image:
    """Build a deterministic multi-color image.

    A solid-color image has only one distinct color, so clustering extractors
    (KMeans, OKLab) collapse to a single swatch and emit ConvergenceWarnings,
    while MedianCut pads to ``palette_size`` with duplicates. A gradient gives
    every method enough distinct colors to return a full, meaningful palette.
    """
    pixels = [((x * 4) % 256, (y * 4) % 256, ((x + y) * 2) % 256) for y in range(h) for x in range(w)]
    img = Image.new("RGB", (w, h))
    img.putdata(pixels)
    return img


def test_library_import():
    """Test that the library can be imported successfully."""
    print("✓ Testing library import...")
    # Import should work if we get here
    assert hasattr(pylette, "extract_colors"), "extract_colors function should be available"
    print("  Import successful")


def test_basic_color_extraction():
    """Test basic color extraction functionality."""
    print("✓ Testing basic color extraction...")

    # Create a multi-color test image so extraction returns a full palette
    test_img = make_test_image()
    palette = pylette.extract_colors(test_img, palette_size=5)

    assert len(palette) == 5, f"Expected 5 colors from a multi-color image, got {len(palette)}"

    print(f"  Extracted {len(palette)} colors successfully")


def test_cli_functionality():
    """Test CLI functionality."""
    print("✓ Testing CLI functionality...")

    # Create a temporary test image
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        test_img = make_test_image()
        test_img.save(tmp.name)

        # Test CLI command
        result = subprocess.run(
            [sys.executable, "-m", "pylette.cmd", tmp.name, "--palette-size", "3"], capture_output=True, text=True
        )

        if result.returncode != 0:
            raise RuntimeError(f"CLI test failed: {result.stderr}")

        # Clean up
        Path(tmp.name).unlink()

    print("  CLI test passed")


def test_extraction_methods():
    """Test every extraction method registered in the registry."""
    print("✓ Testing different extraction methods...")

    from pylette.src.extractors import available_methods

    test_img = make_test_image()

    methods = available_methods()
    assert methods, "Registry should expose at least one extraction method"

    for method in methods:
        palette = pylette.extract_colors(test_img, palette_size=3, mode=method)
        assert len(palette) == 3, f"{method.value} should extract 3 colors from a multi-color image, got {len(palette)}"
        print(f"  {method.value} extracted {len(palette)} colors")


def test_json_export():
    """Test JSON export functionality."""
    print("✓ Testing JSON export...")

    test_img = make_test_image()
    palette = pylette.extract_colors(test_img, palette_size=2)

    # Test JSON export
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        palette.to_json(tmp.name)

        # Verify JSON file was created and is valid
        with open(tmp.name, "r") as f:
            data = json.load(f)
            assert "colors" in data, "JSON should contain 'colors' key"
            assert len(data["colors"]) == 2, f"Should have 2 colors, got {len(data['colors'])}"

        # Clean up
        Path(tmp.name).unlink()

    print("  JSON export test passed")


def main():
    """Run all smoke tests."""
    print("🧪 Starting Pylette smoke test...")

    try:
        test_library_import()
        test_basic_color_extraction()
        test_cli_functionality()
        test_extraction_methods()
        test_json_export()

        print("✅ All smoke tests passed!")
        print("🎉 Pylette is working correctly")

    except Exception as e:
        print(f"❌ Smoke test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
