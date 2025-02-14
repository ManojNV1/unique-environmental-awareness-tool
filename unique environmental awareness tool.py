import cv2
import requests
from plyer import notification
import time

# Configuration
API_KEY = 'your_openweathermap_api_key'  # Free at https://home.openweathermap.org/users/sign_up
CITY = 'London'
ECO_THRESHOLD = 400  # CO2 ppm considered "good air quality"

def get_air_quality():
    try:
        url = f'http://api.openweathermap.org/data/2.5/air_pollution?q={CITY}&appid={API_KEY}'
        response = requests.get(url).json()
        return response['list'][0]['components']['co']
    except:
        return None

def energy_saving_lighting(frame, co2_level):
    # Convert frame to grayscale based on CO2 levels
    if co2_level > ECO_THRESHOLD:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.putText(frame, f"High CO2: {co2_level}ppm!", (10,30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
    return frame

def eco_feedback():
    cap = cv2.VideoCapture(0)
    last_check = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Check air quality every 5 minutes
        if time.time() - last_check > 300:
            co2_level = get_air_quality()
            last_check = time.time()
            
            if co2_level and co2_level > ECO_THRESHOLD:
                notification.notify(
                    title='🌍 Eco Alert!',
                    message=f'High CO2 levels ({co2_level}ppm) detected!\nConsider fresh air!',
                    timeout=10
                )
        
        # Visual feedback
        frame = energy_saving_lighting(frame, co2_level or ECO_THRESHOLD)
        cv2.imshow('Eco Feedback Camera', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    eco_feedback()