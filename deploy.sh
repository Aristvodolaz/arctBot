#!/bin/bash
# Deployment script for ArctBot

set -e  # Exit on error

echo "🚀 Starting deployment..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ Error: .env file not found!${NC}"
    echo "Please create .env file from .env.example"
    exit 1
fi

# Check if google_credentials.json exists
if [ ! -f config/google_credentials.json ]; then
    echo -e "${RED}❌ Error: config/google_credentials.json not found!${NC}"
    echo "Please add your Google API credentials file"
    exit 1
fi

echo -e "${GREEN}✅ Configuration files found${NC}"

# Check deployment method
echo ""
echo "Select deployment method:"
echo "1) Docker Compose (recommended)"
echo "2) Direct Python (systemd service)"
echo "3) Just build Docker image"
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo -e "${YELLOW}🐳 Deploying with Docker Compose...${NC}"
        
        # Stop existing container if running
        if [ "$(docker ps -q -f name=arctbot)" ]; then
            echo "Stopping existing container..."
            docker-compose down
        fi
        
        # Build and start
        docker-compose up -d --build
        
        echo -e "${GREEN}✅ Bot deployed successfully!${NC}"
        echo ""
        echo "Useful commands:"
        echo "  - View logs: docker-compose logs -f"
        echo "  - Stop bot: docker-compose down"
        echo "  - Restart bot: docker-compose restart"
        echo "  - Check status: docker-compose ps"
        ;;
        
    2)
        echo -e "${YELLOW}🐍 Setting up Python environment...${NC}"
        
        # Create virtual environment if not exists
        if [ ! -d "venv" ]; then
            echo "Creating virtual environment..."
            python3 -m venv venv
        fi
        
        # Activate virtual environment
        source venv/bin/activate
        
        # Install/update dependencies
        echo "Installing dependencies..."
        pip install --upgrade pip
        pip install -r requirements.txt
        
        # Setup systemd service
        echo ""
        echo "To run as systemd service:"
        echo "1. Edit systemd.service file with your paths"
        echo "2. Run: sudo cp systemd.service /etc/systemd/system/arctbot.service"
        echo "3. Run: sudo systemctl daemon-reload"
        echo "4. Run: sudo systemctl enable arctbot"
        echo "5. Run: sudo systemctl start arctbot"
        echo ""
        echo "Or run directly:"
        echo "  python main.py"
        ;;
        
    3)
        echo -e "${YELLOW}🏗️  Building Docker image...${NC}"
        docker build -t arctbot:latest .
        echo -e "${GREEN}✅ Docker image built successfully!${NC}"
        echo ""
        echo "To run the container manually:"
        echo "  docker run -d --name arctbot --env-file .env -v \$(pwd)/logs:/app/logs -v \$(pwd)/config/google_credentials.json:/app/config/google_credentials.json:ro arctbot:latest"
        ;;
        
    *)
        echo -e "${RED}❌ Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✨ Deployment complete!${NC}"
