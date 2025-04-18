# Receipt Processing API

A FastAPI-based service for processing receipts and calculating loyalty points. This service provides endpoints to process receipts and retrieve points for specific retailers.

## Features

- Process receipts and calculate loyalty points
- Retrieve points for specific retailers
- Docker support for easy deployment
- Comprehensive API documentation
- Test suite for validation

## Prerequisites

- Python 3.8+
- Docker (optional, for containerized deployment)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/thevyasamit/receipt_processing.git
cd receipt_processing
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Local Development

Start the server in development mode:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Docker Deployment

**Note:** This Docker image is not published to any Docker registry. You must build it locally, and Docker must be installed on your system.

Build and run the Docker container locally:
```bash
# Build the Docker image and tag it as 'receipt-processor:latest'
docker build -t receipt-processor:latest .

# List all Docker images to verify the image was built successfully
docker images
# You should see an entry for receipt-processor:latest

# Run the container, mapping port 8000 on your host to port 80 in the container
# The --rm flag ensures the container is removed after it stops
docker run --rm -p 8000:80 receipt-processor:latest
```

- The API will be available at `http://localhost:8000` after the container starts.
- If you make code changes, rebuild the image to apply updates.
- The `--rm` flag ensures the container is cleaned up after you stop it.

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Process Receipt
```bash
curl -X POST "http://localhost:8000/receipts/process" \
     -H "Content-Type: application/json" \
     -d '{
       "retailer": "Target",
       "purchaseDate": "2024-04-17",
       "purchaseTime": "14:30",
       "items": [
         {
           "shortDescription": "Mountain Dew 12PK",
           "price": 6.49
         },
         {
           "shortDescription": "Emils Cheese Pizza",
           "price": 12.25
         }
       ],
       "total": 18.74
     }'
```

### Get Points for Retailer
```bash
curl "http://localhost:8000/receipts/Target/points"
```

## Testing

Run the test suite:
```bash
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For support, please open an issue in the GitHub repository. 