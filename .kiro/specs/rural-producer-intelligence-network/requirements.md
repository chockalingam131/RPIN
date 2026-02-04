# Requirements Document

## Introduction

The Rural Producer Intelligence Network (RPIN) is an AI-powered web application designed to help rural producers (farmers, small-scale growers, artisans) optimize their selling decisions. The system provides intelligent recommendations on what to sell, where to sell, when to sell, and at what expected price to maximize profit and minimize wastage. RPIN addresses the critical information gap that rural producers face when making market decisions, reducing their dependence on guesswork or middlemen.

## Glossary

- **RPIN_System**: The Rural Producer Intelligence Network web application
- **Producer**: A rural farmer, small-scale grower, or artisan who produces goods for sale
- **Market**: A physical marketplace or mandi where producers can sell their goods
- **Spoilage_Risk**: The probability that a crop will deteriorate during transport and storage
- **Net_Profit**: Total revenue minus transport costs and spoilage losses
- **Price_Predictor**: AI model that forecasts market prices for the next 7 days
- **Demand_Classifier**: AI model that predicts demand levels (Low/Medium/High)
- **Spoilage_Predictor**: AI model that estimates spoilage risk based on weather and crop type
- **Optimization_Engine**: Component that calculates the best market choice for maximum profit
- **Explanation_Generator**: LLM component that provides natural language explanations

## Requirements

### Requirement 1: Producer Input Collection

**User Story:** As a rural producer, I want to input my production details, so that the system can provide personalized market recommendations.

#### Acceptance Criteria

1. WHEN a producer accesses the input form, THE RPIN_System SHALL display fields for village/location, crop type, quantity, and harvest date
2. WHEN a producer enters invalid location data, THE RPIN_System SHALL provide error feedback and suggest valid locations
3. WHEN a producer selects a crop type, THE RPIN_System SHALL validate it against the supported crop database
4. WHEN a producer enters quantity, THE RPIN_System SHALL accept numeric values with appropriate units (kg, tons, etc.)
5. WHEN a producer enters a harvest date, THE RPIN_System SHALL validate it is within a reasonable future timeframe (next 30 days)

### Requirement 2: Price Prediction

**User Story:** As a rural producer, I want to see predicted prices for multiple markets, so that I can identify the most profitable selling opportunities.

#### Acceptance Criteria

1. WHEN the system receives producer inputs, THE Price_Predictor SHALL generate price forecasts for the next 7 days for all relevant markets
2. WHEN generating price predictions, THE Price_Predictor SHALL use XGBoost regression model trained on historical mandi price data
3. WHEN historical data is insufficient, THE Price_Predictor SHALL return confidence intervals with the predictions
4. WHEN price predictions are generated, THE RPIN_System SHALL store them with timestamps for audit purposes
5. WHEN multiple markets are analyzed, THE Price_Predictor SHALL provide predictions for at least 3 nearby markets

### Requirement 3: Demand Level Classification

**User Story:** As a rural producer, I want to understand demand levels in different markets, so that I can avoid oversupplied markets.

#### Acceptance Criteria

1. WHEN price predictions are available, THE Demand_Classifier SHALL categorize demand as Low, Medium, or High for each market
2. WHEN classifying demand, THE Demand_Classifier SHALL use RandomForest model based on price trend analysis
3. WHEN demand classification is complete, THE RPIN_System SHALL display demand levels alongside price predictions
4. WHEN demand data is uncertain, THE Demand_Classifier SHALL indicate confidence levels in the classification

### Requirement 4: Spoilage Risk Assessment

**User Story:** As a rural producer, I want to understand spoilage risks for different timing and transport scenarios, so that I can minimize losses.

#### Acceptance Criteria

1. WHEN transport scenarios are evaluated, THE Spoilage_Predictor SHALL calculate spoilage risk based on crop type, weather conditions, and transport duration
2. WHEN weather data is retrieved, THE Spoilage_Predictor SHALL use current temperature and humidity forecasts
3. WHEN spoilage risk is calculated, THE RPIN_System SHALL express it as a percentage of total quantity
4. WHEN crop shelf-life data is accessed, THE Spoilage_Predictor SHALL reference the static crop shelf-life database
5. WHEN spoilage predictions exceed 20%, THE RPIN_System SHALL highlight this as a high-risk scenario

### Requirement 5: Transport Cost Calculation

**User Story:** As a rural producer, I want to know transport costs to different markets, so that I can factor them into my profit calculations.

#### Acceptance Criteria

1. WHEN market distances are calculated, THE RPIN_System SHALL use the synthetic village-to-market distance database
2. WHEN transport costs are computed, THE RPIN_System SHALL apply standard per-kilometer rates based on vehicle type and cargo weight
3. WHEN multiple transport options exist, THE RPIN_System SHALL calculate costs for the most economical option
4. WHEN distance data is unavailable, THE RPIN_System SHALL estimate based on geographic coordinates

### Requirement 6: Profit Optimization

**User Story:** As a rural producer, I want the system to calculate net profit for each market option, so that I can make informed selling decisions.

#### Acceptance Criteria

1. WHEN all prediction data is available, THE Optimization_Engine SHALL calculate net profit for each market considering price, transport cost, and spoilage risk
2. WHEN calculating net profit, THE Optimization_Engine SHALL use the formula: (Predicted_Price × Remaining_Quantity) - Transport_Cost
3. WHEN multiple time scenarios are evaluated, THE Optimization_Engine SHALL recommend the optimal selling day within the 7-day forecast
4. WHEN profit calculations are complete, THE RPIN_System SHALL rank markets by expected net profit
5. WHEN the best market is identified, THE RPIN_System SHALL highlight it prominently in the results

### Requirement 7: Market Comparison Display

**User Story:** As a rural producer, I want to see a clear comparison of all market options, so that I can easily understand my choices.

#### Acceptance Criteria

1. WHEN results are displayed, THE RPIN_System SHALL present a comparison table with columns for market name, predicted price, demand level, spoilage risk, transport cost, and net profit
2. WHEN the comparison table is rendered, THE RPIN_System SHALL highlight the recommended market with visual emphasis
3. WHEN displaying monetary values, THE RPIN_System SHALL format them in Indian Rupees with appropriate thousand separators
4. WHEN showing percentages, THE RPIN_System SHALL display spoilage risk and confidence levels with clear formatting
5. WHEN the table contains multiple rows, THE RPIN_System SHALL sort them by net profit in descending order

### Requirement 8: Natural Language Explanations

**User Story:** As a rural producer, I want to receive explanations in simple language, so that I can understand why certain recommendations are made.

#### Acceptance Criteria

1. WHEN recommendations are generated, THE Explanation_Generator SHALL create natural language explanations using LLM API
2. WHEN generating explanations, THE Explanation_Generator SHALL include key factors like price differences, spoilage risks, and transport costs
3. WHEN explanations are provided, THE RPIN_System SHALL present them in the local language or simple English
4. WHEN profit differences are significant, THE Explanation_Generator SHALL quantify the financial impact in the explanation
5. WHEN multiple factors influence the recommendation, THE Explanation_Generator SHALL prioritize the most impactful factors in the explanation

### Requirement 9: Data Integration and APIs

**User Story:** As a system administrator, I want reliable data integration, so that the system provides accurate and up-to-date information.

#### Acceptance Criteria

1. WHEN the system starts, THE RPIN_System SHALL load historical mandi price data from AGMARKNET or equivalent public sources
2. WHEN weather data is needed, THE RPIN_System SHALL fetch current and forecast data from open weather APIs
3. WHEN crop shelf-life information is required, THE RPIN_System SHALL access the static crop shelf-life database
4. WHEN distance calculations are needed, THE RPIN_System SHALL query the synthetic village-to-market distance database
5. WHEN external APIs are unavailable, THE RPIN_System SHALL use cached data and notify users of potential data staleness

### Requirement 10: System Performance and Reliability

**User Story:** As a rural producer with limited internet connectivity, I want the system to respond quickly and work reliably, so that I can get timely market information.

#### Acceptance Criteria

1. WHEN a user submits input data, THE RPIN_System SHALL provide complete recommendations within 10 seconds under normal conditions
2. WHEN ML models are loaded, THE RPIN_System SHALL cache them in memory to avoid repeated loading delays
3. WHEN the system experiences high load, THE RPIN_System SHALL maintain response times under 30 seconds for 95% of requests
4. WHEN external data sources are slow, THE RPIN_System SHALL implement timeout mechanisms and fallback to cached data
5. WHEN errors occur, THE RPIN_System SHALL provide user-friendly error messages and suggest alternative actions