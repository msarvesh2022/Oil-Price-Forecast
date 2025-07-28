A web-based application for forecasting oil prices using SARIMA (Seasonal AutoRegressive Integrated Moving Average) time series model with interactive visualization.

# Oil Price Time Series Forecasting


## Features

- **Interactive Web Interface**: Simple form-based input for forecast steps
- **SARIMA Model**: Advanced time series forecasting using pre-trained model
- **Visual Charts**: Interactive line graphs showing forecast trends
- **Month-based Display**: Forecast results shown by month (e.g., "July 2025")
- **Real-time Results**: Instant forecast generation and display
- **Responsive Design**: Works on desktop and mobile devices

## Screenshots

The application provides:
- Clean input form for number of forecast steps
- Interactive line chart visualization
- Detailed forecast values by month
- Summary statistics (min, max, mean values)

## Installation

### Prerequisites

- Python 3.7 or higher
- Flask web framework
- Required Python packages (see requirements.txt)

### Setup

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure model file exists**:
   - Make sure `sarima_model.pkl2` is in the project directory
   - This file contains the pre-trained SARIMA model

## Usage

### Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to:
   ```
   http://localhost:5000
   ```

### Using the Application

1. **Enter Forecast Steps**: 
   - Input the number of forecast steps (1-100)
   - Default value is 12 steps

2. **Get Forecast**: 
   - Click "Get Forecast" button
   - Results appear instantly on the same page

3. **View Results**:
   - **Chart**: Interactive line graph showing price trends
   - **Values**: Detailed forecast values by month
   - **Statistics**: Min, max, and mean values

## API Endpoints

- **GET /** - Main application interface
- **GET /?steps=N** - Get forecast for N steps

## File Structure

```
Oil Price Time Series/
├── app.py              # Main Flask application
├── sarima_model.pkl2   # Pre-trained SARIMA model
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── test_api.py        # API testing script (optional)
```

## Technical Details

### Model Information
- **Model Type**: SARIMA (Seasonal AutoRegressive Integrated Moving Average)
- **Purpose**: Oil price time series forecasting
- **Input**: Number of forecast steps
- **Output**: Predicted oil prices by month

### Technologies Used
- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Charts**: Chart.js library
- **Data Processing**: Pandas
- **Model Loading**: Pickle

### Key Features
- **Input Validation**: Ensures valid step numbers (1-100)
- **Error Handling**: Graceful error messages for invalid inputs
- **Responsive Design**: Works on various screen sizes
- **Real-time Processing**: Instant forecast generation

## Customization

### Modifying Forecast Range
- Edit the validation in `app.py` to change the maximum allowed steps
- Currently limited to 100 steps for performance

### Styling
- Modify CSS in the HTML template within `app.py`
- Chart colors and styling can be adjusted in the JavaScript section

### Model
- Replace `sarima_model.pkl2` with your own trained SARIMA model
- Ensure the model has a `.forecast(steps=N)` method

## Troubleshooting

### Common Issues

1. **"Model file not found"**
   - Ensure `sarima_model.pkl2` exists in the project directory

2. **"Port already in use"**
   - Change the port in `app.py` or stop other services using port 5000

3. **"Forecast error"**
   - Check if the model file is corrupted or incompatible
   - Verify the model has the required forecast method

### Performance Tips
- For large numbers of forecast steps (>50), processing may take longer
- The application is optimized for typical forecast ranges (1-50 steps)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, please open an issue in the repository.

---

**Note**: This application is for educational and demonstration purposes. Actual oil price forecasting should consider multiple factors and use comprehensive market analysis. 
