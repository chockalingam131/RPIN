"""
Test script to verify RPIN data layer functionality
Run this after setup to ensure everything works correctly
"""
from app.data.loaders import data_loader
from app.data.agmarknet import agmarknet_client
from app.data.weather import weather_client

def main():
    print("=" * 60)
    print("RPIN Data Layer Test")
    print("=" * 60)
    
    # Test 1: Load crops
    print("\n1. Loading crops...")
    try:
        crops = data_loader.load_crops()
        print(f"   ✅ Loaded {len(crops)} crops")
        print(f"   Crops: {', '.join(crops.keys())}")
        
        # Show one crop detail
        tomato = crops.get('tomato')
        if tomato:
            print(f"   Example - Tomato: {tomato.shelf_life_days} days shelf life")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Load markets
    print("\n2. Loading markets...")
    try:
        markets = data_loader.load_markets()
        print(f"   ✅ Loaded {len(markets)} markets")
        print(f"   Markets: {', '.join(markets.keys())}")
        
        # Show one market detail
        madurai = markets.get('madurai')
        if madurai:
            print(f"   Example - {madurai.name}: {madurai.capacity_tons} tons capacity")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 3: Load distances
    print("\n3. Loading village distances...")
    try:
        distances = data_loader.load_distances()
        print(f"   ✅ Loaded {len(distances)} villages")
        print(f"   Villages: {', '.join(distances.keys())}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 4: Get nearby markets
    print("\n4. Finding markets near Theni (within 200km)...")
    try:
        nearby = data_loader.get_nearby_markets("theni", max_distance_km=200)
        print(f"   ✅ Found {len(nearby)} nearby markets:")
        for market_id, distance in nearby[:3]:  # Show top 3
            market = data_loader.get_market(market_id)
            print(f"      - {market.name}: {distance} km")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 5: Fetch price data
    print("\n5. Fetching price data for tomato in Madurai...")
    try:
        prices = agmarknet_client.fetch_historical_prices("tomato", "madurai", days=7)
        print(f"   ✅ Fetched {len(prices)} price records")
        if prices:
            latest = prices[-1]
            print(f"   Latest price: ₹{latest.modal_price}/kg on {latest.date}")
            print(f"   Price range: ₹{latest.min_price} - ₹{latest.max_price}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 6: Fetch weather data
    print("\n6. Fetching weather forecast for Madurai...")
    try:
        weather = weather_client.fetch_forecast("Madurai", days=7)
        print(f"   ✅ Fetched {len(weather)} weather forecasts")
        if weather:
            today = weather[0]
            print(f"   Today: {today.temperature_celsius}°C, {today.humidity_percent}% humidity")
            if len(weather) > 1:
                tomorrow = weather[1]
                print(f"   Tomorrow: {tomorrow.temperature_celsius}°C, {tomorrow.humidity_percent}% humidity")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 7: Test data queries
    print("\n7. Testing data queries...")
    try:
        # Get specific crop
        crop = data_loader.get_crop("tomato")
        assert crop is not None, "Failed to get tomato crop"
        
        # Get specific market
        market = data_loader.get_market("madurai")
        assert market is not None, "Failed to get Madurai market"
        
        # Get distance
        distance = data_loader.get_distance("theni", "madurai")
        assert distance is not None, "Failed to get distance"
        assert distance == 80, f"Expected 80 km, got {distance}"
        
        print(f"   ✅ All queries working correctly")
        print(f"   Distance Theni → Madurai: {distance} km")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 All tests passed! Data layer is working correctly.")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Start the server: python main.py")
    print("2. Visit API docs: http://localhost:8000/docs")
    print("3. Continue with Task 5: Implement ML models")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Some tests failed. Please check the errors above.")
            exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
