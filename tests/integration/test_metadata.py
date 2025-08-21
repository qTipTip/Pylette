import pytest
from PIL import Image

from Pylette import extract_colors
from Pylette.src.types import BytesImage, ExtractionMethod, PathLikeImage, URLImage


@pytest.mark.parametrize("mode", [ExtractionMethod.KM, ExtractionMethod.MC])
@pytest.mark.parametrize("resize", [True, False])
class TestMetadata:
    """Test metadata verification for different extraction configurations."""

    def test_metadata_file_path_as_str(self, test_image_path_as_str: str, mode: ExtractionMethod, resize: bool):
        """Test metadata for file path as string input."""
        palette = extract_colors(test_image_path_as_str, mode=mode, resize=resize)

        metadata = palette.metadata
        assert metadata
        assert metadata["source_type"] == "file_path"
        assert metadata["image_source"] == test_image_path_as_str

        # Verify extraction params
        params = metadata["extraction_params"]
        assert params["mode"] == mode
        assert params["resize"] == resize

        # Verify image info
        image_info = metadata["image_info"]
        assert image_info["original_size"] == (1202, 1276)
        assert image_info["format"] == "PNG"
        assert image_info["mode"] == "RGBA"
        assert image_info["has_alpha"] is True

        if resize:
            assert image_info["processed_size"] == (256, 256)
        else:
            assert image_info["processed_size"] == (1202, 1276)

    def test_metadata_file_path_as_pathlike(
        self, test_image_path_as_pathlike: PathLikeImage, mode: ExtractionMethod, resize: bool
    ):
        """Test metadata for file path as Path object input."""
        palette = extract_colors(test_image_path_as_pathlike, mode=mode, resize=resize)

        metadata = palette.metadata
        assert metadata
        assert metadata["source_type"] == "file_path"
        assert metadata["image_source"] == str(test_image_path_as_pathlike)

        # Verify extraction params
        params = metadata["extraction_params"]
        assert params["mode"] == mode
        assert params["resize"] == resize

        # Verify image info
        image_info = metadata["image_info"]
        assert image_info["original_size"] == (1202, 1276)
        assert image_info["format"] == "PNG"
        assert image_info["mode"] == "RGBA"
        assert image_info["has_alpha"] is True

        if resize:
            assert image_info["processed_size"] == (256, 256)
        else:
            assert image_info["processed_size"] == (1202, 1276)

    def test_metadata_url(self, test_image_as_url: URLImage, mode: ExtractionMethod, resize: bool):
        """Test metadata for URL input."""
        palette = extract_colors(test_image_as_url, mode=mode, resize=resize)

        metadata = palette.metadata
        assert metadata
        assert metadata["source_type"] == "url"
        assert metadata["image_source"] == test_image_as_url

        # Verify extraction params
        params = metadata["extraction_params"]
        assert params["mode"] == mode
        assert params["resize"] == resize

        # Verify image info
        image_info = metadata["image_info"]
        assert image_info["original_size"] == (1202, 1276)
        assert image_info["format"] == "PNG"
        assert image_info["mode"] == "RGBA"
        assert image_info["has_alpha"] is True

        if resize:
            assert image_info["processed_size"] == (256, 256)
        else:
            assert image_info["processed_size"] == (1202, 1276)

    def test_metadata_bytes(self, test_image_as_bytes: BytesImage, mode: ExtractionMethod, resize: bool):
        """Test metadata for bytes input."""
        palette = extract_colors(test_image_as_bytes, mode=mode, resize=resize)

        metadata = palette.metadata
        assert metadata
        assert metadata["source_type"] == "bytes"
        assert metadata["image_source"].startswith("<bytes: ")
        assert "bytes>" in metadata["image_source"]

        params = metadata["extraction_params"]
        assert params["mode"] == mode
        assert params["resize"] == resize

        image_info = metadata["image_info"]
        assert image_info["original_size"] == (1202, 1276)
        assert image_info["format"] == "PNG"
        assert image_info["mode"] == "RGBA"
        assert image_info["has_alpha"] is True

        if resize:
            assert image_info["processed_size"] == (256, 256)
        else:
            assert image_info["processed_size"] == (1202, 1276)


def test_metadata_processing_stats(test_image_path_as_str: str):
    """Test processing statistics in metadata."""
    palette = extract_colors(test_image_path_as_str)

    assert palette.metadata
    stats = palette.metadata["processing_stats"]

    # For resized image (256x256)
    assert stats["total_pixels"] == 256 * 256
    assert stats["valid_pixels"] <= stats["total_pixels"]
    assert stats["valid_pixels"] > 0
    assert isinstance(stats["extraction_time"], float)
    assert stats["extraction_time"] > 0
    assert "timestamp" in stats
    assert isinstance(stats["timestamp"], str)


def test_metadata_processing_stats_no_resize(test_image_path_as_str: str):
    """Test processing statistics for non-resized image."""
    palette = extract_colors(test_image_path_as_str, resize=False)

    assert palette.metadata
    stats = palette.metadata["processing_stats"]

    assert stats["total_pixels"] == 1202 * 1276
    assert stats["valid_pixels"] <= stats["total_pixels"]
    assert stats["valid_pixels"] > 0
    assert isinstance(stats["extraction_time"], float)
    assert stats["extraction_time"] > 0


def test_metadata_pil_image_source(test_image_path_as_str: str):
    """Test metadata for PIL Image input has descriptive source."""

    pil_image = Image.open(test_image_path_as_str)
    palette = extract_colors(pil_image)

    metadata = palette.metadata
    assert metadata
    assert metadata["source_type"] == "pil_image"
    assert metadata["image_source"] == "<pil_image: 1202x1276 RGBA>"
