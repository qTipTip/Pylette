from Pylette import batch_extract_colors
from Pylette.src.types import BytesImage, PathLikeImage, URLImage


def test_batch_processing(
    test_image_path_as_pathlike: PathLikeImage,
    test_image_as_url: URLImage,
    test_image_as_bytes: BytesImage,
    test_image_path_as_str: PathLikeImage,
):
    results = batch_extract_colors(
        images=[test_image_path_as_str, test_image_path_as_pathlike, test_image_as_url, test_image_as_bytes]
    )
    assert len(results) == 4
    assert all([r.success for r in results])
