
import cv2
import numpy as np
from ultralytics import YOLO

# טעינת המודל המקורי והחכם שלך - נטען פעם אחת כשהשרת עולה
model = YOLO("yolov8s-world.pt")

# הגדרת ה-Classes המקורית שלך
model.set_classes([
    "milk", "egg", "cheese", "butter", 
    "tomato", "cucumber", "chicken", 
    "ketchup", "onion", "garlic", "yogurt"
])

def process_image_for_ingredients(image_bytes: bytes) -> list:
    """
    פונקציה זו מקבלת תמונה כבייטים, מעבירה אותה דרך מודל ה-YOLO המקורי
    ומחזירה רשימה של מצרכים שזוהו.
    """
    try:
        # המרה לפורמט ש-OpenCV מבין
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            print("שגיאה: לא ניתן היה לפענח את התמונה שנתקבלה מהממשק")
            return []
            
        # הרצת המודל החכם שלך על התמונה
        results = model(image)
        
        detected_items = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                label = model.names[class_id] 
                
                if label not in detected_items:
                    detected_items.append(label)
                    
        print(f"המצרכים שזוהו בהצלחה באלגוריתם: {detected_items}")
        return detected_items

    except Exception as e:
        print(f"תקלה בזמן ריצת מודל ה-YOLO המקורי: {e}")
        return []