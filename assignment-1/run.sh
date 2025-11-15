#!/usr/bin/env bash
set -e

# PROJECT ROOT = directory containing THIS run.sh
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Add assignment-1 directory to module search path
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"

# Create venv if needed
if [ ! -d "$PROJECT_DIR/.venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$PROJECT_DIR/.venv"
fi

source "$PROJECT_DIR/.venv/bin/activate"

# Install dependencies
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    pip3 install --upgrade pip --quiet
    pip install -r "$PROJECT_DIR/requirements.txt" --quiet
fi

case "$1" in
  "demo" )
      echo "Running Assignment 1 demo..."
      python3 -m src.main
      ;;

  "test" )
      echo "Running Assignment 1 tests..."
      pytest -q "$PROJECT_DIR/tests" -v
      ;;

  "clean" )
      echo "Cleaning..."
      rm -rf "$PROJECT_DIR/.venv" "$PROJECT_DIR/.pytest_cache"
      find "$PROJECT_DIR" -name "__pycache__" -exec rm -rf {} +
      ;;

  * )
      echo "Unknown command: $1"
      echo "Usage:"
      echo "  ./run.sh run     # Run demo"
      echo "  ./run.sh test    # Run tests"
      echo "  ./run.sh clean"
      ;;
esac
