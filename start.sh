#!/bin/bash

# Content Journey Finder - Startup Script
# This script helps you start the application in different modes

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print colored message
print_message() {
    color=$1
    message=$2
    echo -e "${color}${message}${NC}"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_message "$RED" "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_message "$RED" "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
}

# Check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_message "$RED" "Python 3 is not installed. Please install Python 3.10 or higher."
        exit 1
    fi
    
    version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    if (( $(echo "$version < 3.10" | bc -l) )); then
        print_message "$RED" "Python 3.10 or higher is required. Current version: $version"
        exit 1
    fi
}

# Start with Docker
start_docker() {
    print_message "$GREEN" "Starting application with Docker..."
    check_docker
    
    if [ "$1" == "build" ]; then
        docker-compose up --build
    else
        docker-compose up
    fi
}

# Start locally
start_local() {
    print_message "$GREEN" "Starting application locally..."
    check_python
    
    # Check if uv is installed
    if ! command -v uv &> /dev/null; then
        print_message "$YELLOW" "uv is not installed. Installing..."
        pip install uv
    fi
    
    # Install dependencies
    if [ ! -f "pyproject.toml" ]; then
        print_message "$RED" "pyproject.toml not found. Are you in the correct directory?"
        exit 1
    fi
    
    print_message "$GREEN" "Installing dependencies..."
    uv pip install -e .
    
    # Start the application
    print_message "$GREEN" "Starting uvicorn server..."
    python run.py
}

# Show help
show_help() {
    cat << EOF
Content Journey Finder - Startup Script

Usage: ./start.sh [mode]

Modes:
  docker        Start with Docker (default)
  docker-build  Start with Docker and rebuild image
  local         Start locally without Docker
  help          Show this help message

Examples:
  ./start.sh                 # Start with Docker
  ./start.sh docker-build    # Rebuild and start with Docker
  ./start.sh local           # Start locally

Environment:
  Create a .env file to configure the application (see .env.example)

Requirements:
  - Docker mode: Docker and Docker Compose
  - Local mode: Python 3.10+, uv (will be installed if missing)

EOF
}

# Main script
main() {
    mode=${1:-docker}
    
    case $mode in
        docker)
            start_docker
            ;;
        docker-build)
            start_docker build
            ;;
        local)
            start_local
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_message "$RED" "Unknown mode: $mode"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
