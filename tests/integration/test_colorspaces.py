import pathlib

import cv2
import pytest
from numpy.testing import assert_approx_equal

from Pylette.src.color_extraction import extract_colors


@pytest.fixture
def test_image_path_as_str():
    test_image = pathlib.Path(__file__).parent.parent / "data/test_image.png"

    yield str(test_image.absolute().resolve())


@pytest.fixture
def test_image_path_as_pathlike():
    test_image = pathlib.Path(__file__).parent.parent / "data/test_image.png"

    yield test_image


@pytest.fixture
def test_image_as_bytes():
    test_image = pathlib.Path(__file__).parent.parent / "data/test_image.png"

    with open(test_image, "rb") as f:
        yield f.read()


@pytest.fixture
def test_image_as_url(requests_mock):
    test_image = pathlib.Path(__file__).parent.parent / "data/test_image.png"
    test_image_url = "https://my-test-image.com/test_image.png"
    with open(test_image, "rb") as f:
        requests_mock.get(test_image_url, content=f.read(), headers={"Content-Type": "image/png"})

        yield test_image_url


@pytest.fixture
def test_image_from_opencv():
    test_image = pathlib.Path(__file__).parent.parent / "data/test_image.png"
    return cv2.imread(str(test_image.absolute().resolve()))


@pytest.fixture()
def test_kmean_extracted_palette(test_image_path_as_str):
    return extract_colors(image=test_image_path_as_str, palette_size=10, resize=True, mode="KM")


@pytest.mark.parametrize("palette_size", [1, 5, 10, 100])
@pytest.mark.parametrize(
    "extraction_mode",
    [
        "KM",
        pytest.param(
            "MC",
            marks=pytest.mark.skip("Currently a bug in the MC algorithm, causing frequencies not summing to one"),
        ),
    ],
)
def test_palette_invariants_with_image_path(test_image_path_as_str, palette_size, extraction_mode):
    palette = extract_colors(
        image=test_image_path_as_str,
        palette_size=palette_size,
        resize=True,
        mode=extraction_mode,
    )

    assert len(palette) == palette_size, f"Expected {palette_size} colors in palette, got {len(palette)}"
    assert (
        palette.number_of_colors == palette_size
    ), f"Expected {palette_size} colors in palette, got {palette.number_of_colors}"
    assert len(palette.colors) == palette_size, f"Expected {palette_size} colors in palette, got {len(palette.colors)}"
    assert (
        palette.colors[0].freq >= palette.colors[-1].freq
    ), "Expected colors to be sorted by frequency in descending order"
    assert palette.colors[0].freq > 0.0, "Expected the most frequent color to have a frequency greater than 0.0"
    assert (
        palette.colors[0].freq <= 1.0
    ), "Expected the most frequent color to have a frequency less than or equal to 1.0"

    assert_approx_equal(
        sum(c.freq for c in palette.colors),
        1.0,
        err_msg="Expected the sum of all frequencies to be 1.0",
    )


@pytest.mark.parametrize("palette_size", [1, 5, 10, 100])
@pytest.mark.parametrize(
    "extraction_mode",
    [
        "KM",
        pytest.param(
            "MC",
            marks=pytest.mark.skip("Currently a bug in the MC algorithm, causing frequencies not summing to one"),
        ),
    ],
)
def test_palette_invariants_with_image_pathlike(test_image_path_as_pathlike, palette_size, extraction_mode):
    palette = extract_colors(
        image=test_image_path_as_pathlike,
        palette_size=palette_size,
        resize=True,
        mode=extraction_mode,
    )

    assert len(palette) == palette_size, f"Expected {palette_size} colors in palette, got {len(palette)}"
    assert (
        palette.number_of_colors == palette_size
    ), f"Expected {palette_size} colors in palette, got {palette.number_of_colors}"
    assert len(palette.colors) == palette_size, f"Expected {palette_size} colors in palette, got {len(palette.colors)}"
    assert (
        palette.colors[0].freq >= palette.colors[-1].freq
    ), "Expected colors to be sorted by frequency in descending order"
    assert palette.colors[0].freq > 0.0, "Expected the most frequent color to have a frequency greater than 0.0"
    assert (
        palette.colors[0].freq <= 1.0
    ), "Expected the most frequent color to have a frequency less than or equal to 1.0"

    assert_approx_equal(
        sum(c.freq for c in palette.colors),
        1.0,
        err_msg="Expected the sum of all frequencies to be 1.0",
    )


@pytest.mark.parametrize("palette_size", [1, 5, 10, 100])
@pytest.mark.parametrize(
    "extraction_mode",
    [
        "KM",
        pytest.param(
            "MC",
            marks=pytest.mark.skip("Currently a bug in the MC algorithm, causing frequencies not summing to one"),
        ),
    ],
)
def test_palette_invariants_with_image_bytes(test_image_as_bytes, palette_size, extraction_mode):
    palette = extract_colors(
        image=test_image_as_bytes,
        palette_size=palette_size,
        resize=True,
        mode=extraction_mode,
    )

    assert len(palette) == palette_size, f"Expected {palette_size} colors in palette, got {len(palette)}"
    assert (
        palette.number_of_colors == palette_size
    ), f"Expected {palette_size} colors in palette, got {palette.number_of_colors}"
    assert len(palette.colors) == palette_size, f"Expected {palette_size} colors in palette, got {len(palette.colors)}"
    assert (
        palette.colors[0].freq >= palette.colors[-1].freq
    ), "Expected colors to be sorted by frequency in descending order"
    assert palette.colors[0].freq > 0.0, "Expected the most frequent color to have a frequency greater than 0.0"
    assert (
        palette.colors[0].freq <= 1.0
    ), "Expected the most frequent color to have a frequency less than or equal to 1.0"

    assert_approx_equal(
        sum(c.freq for c in palette.colors),
        1.0,
        err_msg="Expected the sum of all frequencies to be 1.0",
    )


@pytest.mark.parametrize("palette_size", [1, 5, 10, 100])
@pytest.mark.parametrize(
    "extraction_mode",
    [
        "KM",
        pytest.param(
            "MC",
            marks=pytest.mark.skip("Currently a bug in the MC algorithm, causing frequencies not summing to one"),
        ),
    ],
)
def test_palette_invariants_with_opencv(test_image_from_opencv, palette_size, extraction_mode):
    palette = extract_colors(
        image=test_image_from_opencv,
        palette_size=palette_size,
        resize=True,
        mode=extraction_mode,
    )

    assert len(palette) == palette_size, f"Expected {palette_size} colors in palette, got {len(palette)}"
    assert (
        palette.number_of_colors == palette_size
    ), f"Expected {palette_size} colors in palette, got {palette.number_of_colors}"
    assert len(palette.colors) == palette_size, f"Expected {palette_size} colors in palette, got {len(palette.colors)}"
    assert (
        palette.colors[0].freq >= palette.colors[-1].freq
    ), "Expected colors to be sorted by frequency in descending order"
    assert palette.colors[0].freq > 0.0, "Expected the most frequent color to have a frequency greater than 0.0"
    assert (
        palette.colors[0].freq <= 1.0
    ), "Expected the most frequent color to have a frequency less than or equal to 1.0"

    assert_approx_equal(
        sum(c.freq for c in palette.colors),
        1.0,
        err_msg="Expected the sum of all frequencies to be 1.0",
    )


@pytest.mark.parametrize("palette_size", [1, 5, 10, 100])
@pytest.mark.parametrize(
    "extraction_mode",
    [
        "KM",
        pytest.param(
            "MC",
            marks=pytest.mark.skip("Currently a bug in the MC algorithm, causing frequencies not summing to one"),
        ),
    ],
)
def test_palette_invariants_with_image_url(test_image_as_url, palette_size, extraction_mode):
    palette = extract_colors(
        image=test_image_as_url,
        palette_size=palette_size,
        resize=True,
        mode=extraction_mode,
    )

    assert len(palette) == palette_size, f"Expected {palette_size} colors in palette, got {len(palette)}"
    assert (
        palette.number_of_colors == palette_size
    ), f"Expected {palette_size} colors in palette, got {palette.number_of_colors}"
    assert len(palette.colors) == palette_size, f"Expected {palette_size} colors in palette, got {len(palette.colors)}"
    assert (
        palette.colors[0].freq >= palette.colors[-1].freq
    ), "Expected colors to be sorted by frequency in descending order"
    assert palette.colors[0].freq > 0.0, "Expected the most frequent color to have a frequency greater than 0.0"
    assert (
        palette.colors[0].freq <= 1.0
    ), "Expected the most frequent color to have a frequency less than or equal to 1.0"

    assert_approx_equal(
        sum(c.freq for c in palette.colors),
        1.0,
        err_msg="Expected the sum of all frequencies to be 1.0",
    )


def test_colorspace_invariants_hls(test_kmean_extracted_palette):
    for color in test_kmean_extracted_palette:
        H, L, S = color.get_colors(colorspace="hls")
        assert 0 <= H <= 360, f"Expected 0 <= h <= 360, got {H}"
        assert 0 <= L <= 1, f"Expected 0 <= l <= 1, got {L}"
        assert 0 <= S <= 1, f"Expected 0 <= s <= 1, got {S}"


def test_colorspace_invariants_hsv(test_kmean_extracted_palette):
    for color in test_kmean_extracted_palette:
        H, L, V = color.get_colors(colorspace="hls")
        assert 0 <= H <= 360, f"Expected 0 <= h <= 360, got {H}"
        assert 0 <= L <= 1, f"Expected 0 <= l <= 1, got {L}"
        assert 0 <= V <= 1, f"Expected 0 <= s <= 1, got {V}"


def test_colorspace_invariants_rgb(test_kmean_extracted_palette):
    for color in test_kmean_extracted_palette:
        r, g, b = color.rgb
        assert 0 <= r <= 255, f"Expected 0 <= r <= 255, got {r}"
        assert 0 <= g <= 255, f"Expected 0 <= g <= 255, got {g}"
        assert 0 <= b <= 255, f"Expected 0 <= b <= 255, got {b}"


@pytest.mark.parametrize("resize, sort_mode", [(True, "luminance"), (False, "frequency")])
def test_color_extraction_deterministic_kmeans(test_image_path_as_str, resize, sort_mode):
    palette1 = extract_colors(
        image=test_image_path_as_str,
        palette_size=5,
        resize=resize,
        mode="KM",
        sort_mode=sort_mode,
    )
    palette2 = extract_colors(
        image=test_image_path_as_str,
        palette_size=5,
        resize=resize,
        mode="KM",
        sort_mode=sort_mode,
    )
    for c1, c2 in zip(palette1.colors, palette2.colors):
        r, g, b, freq = c1.rgb[0], c1.rgb[1], c1.rgb[2], c1.freq
        r2, g2, b2, freq2 = c2.rgb[0], c2.rgb[1], c2.rgb[2], c2.freq

        assert r == r2, f"Expected r1 == r2, got {r} != {r2}"
        assert g == g2, f"Expected g1 == g2, got {g} != {g2}"
        assert b == b2, f"Expected b1 == b2, got {b} != {b2}"
        assert freq == freq2, f"Expected freq1 == freq2, got {freq} != {freq2}"
