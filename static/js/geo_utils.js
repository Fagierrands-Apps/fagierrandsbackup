/**
 * Utility functions for geospatial calculations
 * This replaces the need for GDAL on the backend
 */

// Calculate distance between two points using the Haversine formula
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Earth radius in kilometers
    
    // Convert latitude and longitude from degrees to radians
    const lat1Rad = toRadians(lat1);
    const lon1Rad = toRadians(lon1);
    const lat2Rad = toRadians(lat2);
    const lon2Rad = toRadians(lon2);
    
    // Haversine formula
    const dlon = lon2Rad - lon1Rad;
    const dlat = lat2Rad - lat1Rad;
    const a = Math.sin(dlat/2)**2 + Math.cos(lat1Rad) * Math.cos(lat2Rad) * Math.sin(dlon/2)**2;
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    const distance = R * c; // Distance in kilometers
    
    return distance;
}

// Convert degrees to radians
function toRadians(degrees) {
    return degrees * (Math.PI / 180);
}

// Calculate bearing between two points
function calculateBearing(lat1, lon1, lat2, lon2) {
    const lat1Rad = toRadians(lat1);
    const lon1Rad = toRadians(lon1);
    const lat2Rad = toRadians(lat2);
    const lon2Rad = toRadians(lon2);
    
    const y = Math.sin(lon2Rad - lon1Rad) * Math.cos(lat2Rad);
    const x = Math.cos(lat1Rad) * Math.sin(lat2Rad) -
              Math.sin(lat1Rad) * Math.cos(lat2Rad) * Math.cos(lon2Rad - lon1Rad);
    
    let bearing = Math.atan2(y, x);
    bearing = toDegrees(bearing);
    bearing = (bearing + 360) % 360; // Normalize to 0-360
    
    return bearing;
}

// Convert radians to degrees
function toDegrees(radians) {
    return radians * (180 / Math.PI);
}

// Calculate midpoint between two coordinates
function calculateMidpoint(lat1, lon1, lat2, lon2) {
    const lat1Rad = toRadians(lat1);
    const lon1Rad = toRadians(lon1);
    const lat2Rad = toRadians(lat2);
    const lon2Rad = toRadians(lon2);
    
    const Bx = Math.cos(lat2Rad) * Math.cos(lon2Rad - lon1Rad);
    const By = Math.cos(lat2Rad) * Math.sin(lon2Rad - lon1Rad);
    
    const latMid = Math.atan2(
        Math.sin(lat1Rad) + Math.sin(lat2Rad),
        Math.sqrt((Math.cos(lat1Rad) + Bx) * (Math.cos(lat1Rad) + Bx) + By * By)
    );
    
    const lonMid = lon1Rad + Math.atan2(By, Math.cos(lat1Rad) + Bx);
    
    return {
        latitude: toDegrees(latMid),
        longitude: toDegrees(lonMid)
    };
}

// Check if a point is within a certain radius of another point
function isPointWithinRadius(lat1, lon1, lat2, lon2, radiusKm) {
    const distance = calculateDistance(lat1, lon1, lat2, lon2);
    return distance <= radiusKm;
}

// Export the functions if using ES modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        calculateDistance,
        calculateBearing,
        calculateMidpoint,
        isPointWithinRadius,
        toRadians,
        toDegrees
    };
}