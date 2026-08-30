import math
import logging
from typing import Dict, Tuple, Any

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points on the Earth's surface
    using the Haversine formula.
    
    Args:
        lat1, lon1: Coordinates of the first point in degrees.
        lat2, lon2: Coordinates of the second point in degrees.
        
    Returns:
        float: Distance in kilometers.
    """
    # Convert latitude and longitude from degrees to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Earth's radius in kilometers
    R = 6371.0

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return round(distance, 2)

def calculate_transport_cost(
    origin_coords: Tuple[float, float],
    dest_coords: Tuple[float, float],
    weight_metric_tons: float,
    rate_per_km_ton: float = 5.0,
    base_fare: float = 500.0
) -> Dict[str, Any]:
    """
    Estimate the transportation cost based on distance, cargo weight, and pricing parameters.
    
    Args:
        origin_coords (tuple): (latitude, longitude) of origin location.
        dest_coords (tuple): (latitude, longitude) of destination location.
        weight_metric_tons (float): Weight of the agricultural commodity in metric tons.
        rate_per_km_ton (float): Rate in local currency (INR) per kilometer per metric ton. Default is 5.0 INR.
        base_fare (float): Base flat fee to charge regardless of distance (minimum setup fare). Default is 500.0 INR.
        
    Returns:
        dict: A dictionary breakdown of the estimated distance, fares, and total cost.
    """
    lat1, lon1 = origin_coords
    lat2, lon2 = dest_coords
    
    # Calculate distance
    distance_km = haversine_distance(lat1, lon1, lat2, lon2)
    
    # Ensure minimum distance is not 0 to avoid zero charges if coordinates are exact same spot
    effective_distance = max(distance_km, 0.5)
    
    # Variable cost calculation
    variable_cost = effective_distance * weight_metric_tons * rate_per_km_ton
    
    # Total cost
    total_cost = base_fare + variable_cost
    
    result = {
        "status": "success",
        "origin": origin_coords,
        "destination": dest_coords,
        "distance_km": distance_km,
        "cargo_weight_tons": weight_metric_tons,
        "rate_per_km_ton": rate_per_km_ton,
        "base_fare": round(base_fare, 2),
        "variable_cost": round(variable_cost, 2),
        "total_estimated_cost": round(total_cost, 2)
    }
    
    logger.info(
        f"Calculated cost for {weight_metric_tons} tons over {distance_km} km: "
        f"Base={base_fare}, Var={round(variable_cost, 2)} -> Total={round(total_cost, 2)}"
    )
    return result
