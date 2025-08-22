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

import Pylette


def test_library_import():
    """Test that the library can be imported successfully."""
    print("✓ Testing library import...")
    # Import should work if we get here
    assert hasattr(Pylette, "extract_colors"), "extract_colors function should be available"
    print("  Import successful")


def test_basic_color_extraction():
    """Test basic color extraction functionality."""
    print("✓ Testing basic color extraction...")

    # Create a simple test image
    test_img = Image.new("RGB", (100, 100), color="red")
    palette = Pylette.extract_colors(test_img, palette_size=5)

    assert len(palette) <= 5, f"Palette size should not exceed 5, got {len(palette)}"
    assert len(palette) > 0, "Should extract at least one color"

    print(f"  Extracted {len(palette)} colors successfully")


def test_cli_functionality():
    """Test CLI functionality."""
    print("✓ Testing CLI functionality...")

    # Create a temporary test image
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        test_img = Image.new("RGB", (50, 50), color="blue")
        test_img.save(tmp.name)

        # Test CLI command
        result = subprocess.run(
            [sys.executable, "-m", "Pylette.cmd", tmp.name, "--palette_size", "3"], capture_output=True, text=True
        )

        if result.returncode != 0:
            raise RuntimeError(f"CLI test failed: {result.stderr}")

        # Clean up
        Path(tmp.name).unlink()

    print("  CLI test passed")


def test_extraction_methods():
    """Test different extraction methods."""
    print("✓ Testing different extraction methods...")

    test_img = Image.new("RGB", (50, 50), color="green")

    # Test K-means extractor
    kmeans_palette = Pylette.extract_colors(test_img, palette_size=3, mode=Pylette.types.ExtractionMethod.KM)
    assert len(kmeans_palette) <= 3, "K-means should respect palette size"
    print(f"  K-means extracted {len(kmeans_palette)} colors")

    # Test Median cut extractor
    mediancut_palette = Pylette.extract_colors(test_img, palette_size=3, mode=Pylette.types.ExtractionMethod.MC)
    assert len(mediancut_palette) <= 3, "Median cut should respect palette size"
    print(f"  Median cut extracted {len(mediancut_palette)} colors")


def test_json_export():
    """Test JSON export functionality."""
    print("✓ Testing JSON export...")

    test_img = Image.new("RGB", (50, 50), color="purple")
    palette = Pylette.extract_colors(test_img, palette_size=2)

    # Test JSON export
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        palette.to_json(tmp.name)

        # Verify JSON file was created and is valid
        with open(tmp.name, "r") as f:
            data = json.load(f)
            assert "colors" in data, "JSON should contain 'colors' key"
            assert len(data["colors"]) <= 2, f"Should have at most 2 colors, got {len(data['colors'])}"

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
