#!/bin/bash

# MegaStore BigData Lab Starter Script
# Usage: ./start-lab.sh [lab-name]
# Options: mongodb | duckdb | neo4j | spark | stop | restart-all

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Function to display help
show_help() {
    cat << EOF
${BLUE}MegaStore BigData Lab Starter${NC}

Usage: ./start-lab.sh [COMMAND]

Commands:
  mongodb       Start MongoDB lab (MongoDB + Mongo Express)
  duckdb        Start DuckDB lab (Jupyter with DuckDB)
  neo4j         Start Neo4j lab (Graph Database)
  spark         Start Spark lab (PySpark + Jupyter)

  stop          Stop all running labs
  restart-all   Restart all labs (stop + start all)
  status        Show status of all labs
  help          Show this help message

Examples:
  ./start-lab.sh mongodb
  ./start-lab.sh duckdb
  ./start-lab.sh stop

Access Information:
  MongoDB:       localhost:27017 (database), localhost:8081 (Mongo Express UI)
  DuckDB:        localhost:8888 (Jupyter)
  Neo4j:         localhost:7474 (Browser), localhost:7687 (Bolt)
  Spark:         localhost:8888 (Jupyter), localhost:4040 (Spark UI)

EOF
}

# Function to start a lab
start_lab() {
    local lab=$1
    local lab_dir="$SCRIPT_DIR/$lab"

    if [ ! -d "$lab_dir" ]; then
        print_error "Lab directory not found: $lab_dir"
        return 1
    fi

    print_info "Starting $lab lab..."

    cd "$lab_dir"

    # Check if docker-compose.yml exists
    if [ ! -f "docker-compose.yml" ]; then
        print_error "docker-compose.yml not found in $lab_dir"
        return 1
    fi

    # Build images if necessary
    if [ "$lab" == "duckdb" ] || [ "$lab" == "spark" ]; then
        print_info "Building Docker image for $lab..."
        docker-compose build --quiet
    fi

    # Start containers
    docker-compose up -d

    if [ $? -eq 0 ]; then
        print_success "$lab lab started!"

        # Show access information
        case $lab in
            mongodb)
                echo ""
                echo "MongoDB is starting. Access at:"
                echo "  Database:     mongodb://localhost:27017"
                echo "  Mongo Express: http://localhost:8081"
                echo "  Username:      admin"
                echo "  Password:      pass"
                echo ""
                echo "Check container status with: docker-compose logs"
                ;;
            duckdb)
                echo ""
                echo "DuckDB Jupyter is starting. Access at:"
                echo "  Jupyter:       http://localhost:8888"
                echo ""
                echo "Check the logs for the access token:"
                echo "  docker-compose logs duckdb | grep token"
                ;;
            neo4j)
                echo ""
                echo "Neo4j is starting. Access at:"
                echo "  Browser:       http://localhost:7474"
                echo "  Bolt:          bolt://localhost:7687"
                echo "  Auth:          None (no authentication)"
                echo ""
                echo "Import data by running Cypher scripts in the browser:"
                echo "  Check: docker/neo4j/import/import-megastore.cypher"
                ;;
            spark)
                echo ""
                echo "Spark/PySpark is starting. Access at:"
                echo "  Jupyter:       http://localhost:8888"
                echo "  Spark UI:      http://localhost:4040"
                echo ""
                echo "Check the logs for the access token:"
                echo "  docker-compose logs spark | grep token"
                ;;
        esac

        return 0
    else
        print_error "Failed to start $lab lab"
        return 1
    fi
}

# Function to stop all labs
stop_all_labs() {
    print_info "Stopping all labs..."

    for lab in mongodb duckdb neo4j spark; do
        local lab_dir="$SCRIPT_DIR/$lab"
        if [ -d "$lab_dir" ] && [ -f "$lab_dir/docker-compose.yml" ]; then
            print_info "Stopping $lab..."
            cd "$lab_dir"
            docker-compose down --quiet 2>/dev/null || true
            print_success "$lab stopped"
        fi
    done

    print_success "All labs stopped"
}

# Function to show status
show_status() {
    print_info "Lab Status:"
    echo ""

    for lab in mongodb duckdb neo4j spark; do
        local lab_dir="$SCRIPT_DIR/$lab"
        if [ -d "$lab_dir" ] && [ -f "$lab_dir/docker-compose.yml" ]; then
            cd "$lab_dir"

            # Get container status
            local status=$(docker-compose ps -q 2>/dev/null | wc -l)

            if [ $status -gt 0 ]; then
                echo -e "${GREEN}✓ $lab${NC} (running)"
                docker-compose ps --services 2>/dev/null | sed 's/^/    - /'
            else
                echo -e "${RED}✗ $lab${NC} (stopped)"
            fi
            echo ""
        fi
    done
}

# Function to restart all labs
restart_all_labs() {
    print_warning "Restarting all labs..."
    stop_all_labs
    echo ""
    sleep 2

    for lab in mongodb duckdb neo4j spark; do
        start_lab "$lab" || true
        echo ""
        sleep 2
    done

    show_status
}

# Main script logic
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

case "$1" in
    mongodb|duckdb|neo4j|spark)
        start_lab "$1"
        ;;
    stop)
        stop_all_labs
        ;;
    restart-all)
        restart_all_labs
        ;;
    status)
        show_status
        ;;
    help|-h|--help)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac

exit $?
