import pytest
from click.testing import CliRunner
from owera.main import owera
from pathlib import Path
import tempfile

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def temp_spec_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml') as f:
        f.write("""
        project:
          name: TestApp
          tech_stack:
            backend: Python/Flask
            frontend: HTML/CSS
        features:
          - name: home_page
            description: Home page with welcome message
        """)
        f.flush()
        yield f.name

def test_generate_command(runner, temp_spec_file):
    """Test the generate command."""
    with tempfile.TemporaryDirectory() as temp_dir:
        result = runner.invoke(owera, [
            'generate',
            '--spec-file', temp_spec_file,
            '--output', temp_dir,
            '--check-deps'
        ])
        assert result.exit_code == 0
        assert "Project generated successfully" in result.output

def test_update_deps_command_dry_run(runner):
    """Test the update-deps command in dry run mode."""
    result = runner.invoke(owera, ['update-deps', '--dry-run'])
    assert result.exit_code == 0
    assert "The following updates would be made" in result.output

def test_update_deps_command_actual(runner):
    """Test the update-deps command with actual updates."""
    result = runner.invoke(owera, ['update-deps', '--no-dry-run'])
    assert result.exit_code == 0
    assert "Dependencies updated successfully" in result.output

def test_generate_command_without_check_deps(runner, temp_spec_file):
    """Test the generate command without dependency checking."""
    with tempfile.TemporaryDirectory() as temp_dir:
        result = runner.invoke(owera, [
            'generate',
            '--spec-file', temp_spec_file,
            '--output', temp_dir,
            '--no-check-deps'
        ])
        assert result.exit_code == 0
        assert "Project generated successfully" in result.output 