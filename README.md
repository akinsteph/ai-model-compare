# AI Model Comparison Tool 🤖

A modern web application that provides real-time comparisons of AI model pricing, features, and capabilities. Built with Flask and beautiful UI components.

## Features ✨

- Real-time price tracking from major AI providers
- Subscription model comparisons
- Usage limits and restrictions
- Beautiful dark theme UI
- Mobile-responsive design
- RESTful API endpoints
- Automated price updates

## Live Demo 🌐

Visit: [https://ai-model-compare.herokuapp.com](https://ai-model-compare.herokuapp.com)

## API Documentation 📚

### Endpoints

#### 1. Get Current Pricing
```http
GET /api/pricing
```

Returns current pricing information for all AI models.

**Response Example:**
```json
{
    "last_updated": "2024-11-10T14:00:00.000Z",
    "providers": {
        "openai": {
            "gpt4": {
                "input": "$0.03/1K tokens",
                "output": "$0.06/1K tokens"
            }
        }
    }
}
```

#### 2. Refresh Pricing
```http
GET /api/refresh-pricing
```

Triggers an immediate refresh of the pricing data.

### Rate Limits
- Pricing endpoint: 60 requests/minute
- Refresh endpoint: 1 request/minute

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/akinsteph/ai-model-compare.git
cd ai-model-compare
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Run the application:
```bash
python3 app.py
```

## Development 🛠

### Prerequisites
- Python 3.9+
- Flask
- BeautifulSoup4
- Requests

### Environment Setup
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip3 install -r requirements.txt
```

## Contributing 🤝

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits 🙏

Developed with ❤️ by [Stephen Akinola](https://github.com/akinsteph)

*"Comparing AI models shouldn't be rocket science... unless you're training an AI for rocket science!" - Stephen Akinola*
