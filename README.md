# Receipt Processing API

A FastAPI-based service for processing receipts and calculating loyalty points. This service provides endpoints to process receipts and retrieve points for specific retailers.

## Features

- Process receipts and calculate loyalty points
- Retrieve points for specific retailers
- Docker support for easy deployment
- Comprehensive API documentation
- Test suite for validation

## Prerequisites

- Python 3.12+
- Docker (for containerized deployment)

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

---

## ⚡️ Using [uv](https://github.com/astral-sh/uv) for Fast Dependency Management

> **Note:** I personally use [uv](https://github.com/astral-sh/uv) as my preferred Python package manager because it's super fast and reliable. You are encouraged to use it for the best experience!

For faster and more reliable installs, you can use [uv](https://github.com/astral-sh/uv) instead of pip:

### Install uv
```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

### Install dependencies with uv
```bash
uv pip install -r requirements.txt
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
curl -X POST "http://localhost:8000/receipts" \
     -H "Content-Type: application/json" \
     -d '{
       "retailer": "M&M Corner Market",
       "purchaseDate": "2022-03-20",
       "purchaseTime": "14:33",
       "items": [
         { "shortDescription": "Gatorade", "price": "2.25" },
         { "shortDescription": "Gatorade", "price": "2.25" },
         { "shortDescription": "Gatorade", "price": "2.25" },
         { "shortDescription": "Gatorade", "price": "2.25" }
       ],
       "total": "9.00"
     }'
```

Sample response breakdown:
```text
Total Points: 109
Breakdown:
    50 points - total is a round dollar amount
    25 points - total is a multiple of 0.25
    14 points - retailer name (M&M Corner Market) has 14 alphanumeric characters
                note: '&' is not alphanumeric
    10 points - 2:33pm is between 2:00pm and 4:00pm
    10 points - 4 items (2 pairs @ 5 points each)
  + ---------
  = 109 points
```

### Get Points for Receipt ID
```bash
curl "http://localhost:8000/receipts/5f9cc72b-cdad-4880-bef2-b2a0d5dab5b3/points"
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