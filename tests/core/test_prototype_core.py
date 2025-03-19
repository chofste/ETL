import pytest
from pathlib import Path
import importlib.util
from core.core import generate_script

TEST_DIR = Path(__file__).parent


@pytest.fixture
def generated_script_file():
    """Fixture to generate the script and return its path."""
    script_path = TEST_DIR / "generated_script.py"
    generate_script("config_test.json")
    return script_path  # Return the script path for use in tests


def import_generated_script(script_path):
    """Dynamically import the generated script as a module."""
    module_name = "generated_script"
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module  # Return the dynamically loaded module


class TestPrototypeCore:
    def test_generated_script_exists(self, generated_script_file):
        assert (
            generated_script_file.exists()
        ), f"File {generated_script_file} does not exist"

    def test_output_files_exists(self, generated_script_file):
        module = import_generated_script(generated_script_file)

        assert hasattr(
            module, "main"
        ), "The generated script does not have a 'main' function"

        try:
            module.main()
        except Exception as e:
            pytest.fail(f"Running main() in the generated script failed: {e}")

        file_path_aggregation = TEST_DIR / "output_aggregation_test.csv"
        file_path_transformation = TEST_DIR / "output_transformation_test.csv"
        file_path_merged = TEST_DIR / "output_merged_test.csv"

        assert (
            file_path_aggregation.exists()
        ), f"File {file_path_aggregation} does not exist in the test directory"
        assert (
            file_path_transformation.exists()
        ), f"File {file_path_transformation} does not exist in the test directory"
        assert (
            file_path_merged.exists()
        ), f"File {file_path_merged} does not exist in the test directory"


if __name__ == "__main__":
    pytest.main()
