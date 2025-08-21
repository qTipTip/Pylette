import json
import tempfile
from pathlib import Path

import pytest
from typer.testing import CliRunner

from Pylette.cmd import pylette_app


class TestJSONExport:
    """Integration tests for JSON export functionality."""

    @pytest.fixture
    def runner(self):
        """CLI test runner."""
        return CliRunner()

    @pytest.fixture
    def test_image(self):
        """Path to test image."""
        return "tests/data/test_image.png"

    def test_json_export_individual_files(self, runner, test_image):
        """Test exporting individual JSON files to a directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "palettes"

            result = runner.invoke(
                pylette_app, [test_image, "--export-json", "--output", str(output_dir), "--no-stdout", "--n", "3"]
            )

            assert result.exit_code == 0
            assert "✓ Exported 1 palettes to" in result.stdout

            # Check that file was created
            json_files = list(output_dir.glob("*.json"))
            assert len(json_files) == 1
            assert json_files[0].name == "palette_001.json"

            # Verify JSON content
            with open(json_files[0]) as f:
                data = json.load(f)

            assert "colors" in data
            assert "palette_size" in data
            assert "colorspace" in data
            assert "metadata" in data
            assert data["palette_size"] == 3
            assert len(data["colors"]) == 3
            assert data["colorspace"] == "rgb"
            assert data["metadata"]["image_source"] == test_image

    def test_json_export_multiple_individual_files(self, runner, test_image):
        """Test exporting multiple individual JSON files to a directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "palettes"

            result = runner.invoke(
                pylette_app,
                [
                    test_image,
                    test_image,  # Process same image twice
                    "--export-json",
                    "--output",
                    str(output_dir),
                    "--no-stdout",
                    "--n",
                    "2",
                ],
            )

            assert result.exit_code == 0
            assert "✓ Exported 2 palettes to" in result.stdout

            # Check that files were created
            json_files = sorted(output_dir.glob("*.json"))
            assert len(json_files) == 2
            assert json_files[0].name == "palette_001.json"
            assert json_files[1].name == "palette_002.json"

            # Verify both files have valid content
            for json_file in json_files:
                with open(json_file) as f:
                    data = json.load(f)
                assert data["palette_size"] == 2
                assert len(data["colors"]) == 2

    def test_json_export_combined_file(self, runner, test_image):
        """Test exporting to a combined JSON file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "combined_palettes.json"

            result = runner.invoke(
                pylette_app,
                [
                    test_image,
                    test_image,  # Process same image twice
                    "--export-json",
                    "--output",
                    str(output_file),
                    "--no-stdout",
                    "--n",
                    "2",
                ],
            )

            assert result.exit_code == 0
            assert f"✓ Exported 2 palettes to {output_file}" in result.stdout

            # Check that combined file was created
            assert output_file.exists()

            # Verify combined JSON content
            with open(output_file) as f:
                data = json.load(f)

            assert "palettes" in data
            assert "total_count" in data
            assert "colorspace" in data
            assert data["total_count"] == 2
            assert data["colorspace"] == "rgb"
            assert len(data["palettes"]) == 2

            # Verify each palette in the combined file
            for palette in data["palettes"]:
                assert "colors" in palette
                assert "palette_size" in palette
                assert palette["palette_size"] == 2
                assert len(palette["colors"]) == 2

    def test_json_export_different_colorspaces(self, runner, test_image):
        """Test JSON export with different colorspaces."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "hsv_palette.json"

            result = runner.invoke(
                pylette_app,
                [
                    test_image,
                    "--export-json",
                    "--output",
                    str(output_file),
                    "--colorspace",
                    "hsv",
                    "--no-stdout",
                    "--n",
                    "3",
                ],
            )

            assert result.exit_code == 0

            # Verify HSV colorspace
            with open(output_file) as f:
                data = json.load(f)

            assert data["palettes"][0]["colorspace"] == "hsv"
            # HSV values should be floats between 0 and 1
            first_color = data["palettes"][0]["colors"][0]
            assert all(isinstance(v, float) for v in first_color["values"])
            # Should include RGB reference values
            assert "rgb" in first_color

    def test_json_export_creates_parent_directories(self, runner, test_image):
        """Test that JSON export creates parent directories if they don't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = Path(tmpdir) / "deep" / "nested" / "path" / "palette.json"

            result = runner.invoke(
                pylette_app, [test_image, "--export-json", "--output", str(nested_path), "--no-stdout", "--n", "2"]
            )

            assert result.exit_code == 0
            assert nested_path.exists()

            # Verify content
            with open(nested_path) as f:
                data = json.load(f)
            assert data["total_count"] == 1

    def test_json_export_error_without_output(self, runner, test_image):
        """Test that JSON export requires --output parameter."""
        result = runner.invoke(pylette_app, [test_image, "--export-json", "--no-stdout"])

        assert result.exit_code == 1
        assert "Error: --output is required when using --export-json" in result.stderr

    def test_json_export_preserves_metadata(self, runner, test_image):
        """Test that JSON export preserves all metadata."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "metadata_test.json"

            result = runner.invoke(
                pylette_app,
                [
                    test_image,
                    "--export-json",
                    "--output",
                    str(output_file),
                    "--mode",
                    "MedianCut",
                    "--alpha-mask-threshold",
                    "128",
                    "--no-stdout",
                    "--n",
                    "4",
                ],
            )

            assert result.exit_code == 0

            with open(output_file) as f:
                data = json.load(f)

            palette = data["palettes"][0]
            metadata = palette["metadata"]

            # Check extraction parameters
            assert metadata["extraction_params"]["palette_size"] == 4
            assert metadata["extraction_params"]["mode"] == "MedianCut"
            assert metadata["extraction_params"]["alpha_mask_threshold"] == 128

            # Check image info
            assert "image_info" in metadata
            assert "original_size" in metadata["image_info"]
            assert "processed_size" in metadata["image_info"]

            # Check processing stats
            assert "processing_stats" in metadata
            assert "extraction_time" in metadata["processing_stats"]
            assert "timestamp" in metadata["processing_stats"]

    def test_fallback_to_csv_when_no_export_json(self, runner, test_image):
        """Test that CLI falls back to CSV behavior when --export-json is not used."""
        result = runner.invoke(pylette_app, [test_image, "--n", "2"])

        assert result.exit_code == 0
        # Should output CSV-style data to stdout
        lines = result.stdout.strip().split("\n")
        # Look for CSV-like output (numbers separated by commas)
        csv_lines = [line for line in lines if "," in line and line.replace(",", "").replace(".", "").isdigit()]
        assert len(csv_lines) > 0  # Should have some CSV output
