import pytest

from pylette.src.extractors import available_methods, get_extractor
from pylette.src.extractors.protocol import ColorExtractor
from pylette.src.types import ExtractionMethod


class TestRegistry:
    def test_registry_and_enum_in_sync(self):
        """Every enum member has an extractor and vice versa"""
        assert set(available_methods()) == set(ExtractionMethod)

    @pytest.mark.parametrize("method", list(ExtractionMethod))
    def test_get_extractor_by_enum(self, method: ExtractionMethod):
        extractor = get_extractor(method)
        assert isinstance(extractor, ColorExtractor)

    @pytest.mark.parametrize("method", list(ExtractionMethod))
    def test_get_extractor_by_string(self, method: ExtractionMethod):
        """Get extractor by string value should be identical to enum member"""
        assert get_extractor(method.value) is get_extractor(method)

    def test_unknown_method_raises_value_error(self):
        with pytest.raises(ValueError):
            get_extractor("NotARealMethod")
