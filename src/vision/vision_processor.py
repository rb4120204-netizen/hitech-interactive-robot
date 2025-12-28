"""
Vision Processor Module
Handles computer vision tasks using OpenCV
"""

import cv2
import logging
import numpy as np
from typing import Optional, List, Tuple
import time

logger = logging.getLogger(__name__)


class VisionProcessor:
    """Computer vision processor"""
    
    def __init__(self, config):
        """Initialize vision processor"""
        self.config = config
        
        # Initialize camera
        camera_index = config.get('vision', {}).get('camera_index', 0)
        self.camera = cv2.VideoCapture(camera_index)
        
        if not self.camera.isOpened():
            logger.error("Failed to open camera")
            self.camera = None
        else:
            # Set camera properties
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            logger.info("Camera initialized")
        
        # Load face detection cascade
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        # Object tracking
        self.tracking_object = None
        self.tracker = None
    
    def capture_image(self, filename: Optional[str] = None) -> Optional[np.ndarray]:
        """
        Capture image from camera
        
        Args:
            filename: Optional filename to save image
            
        Returns:
            Captured image or None
        """
        if not self.camera:
            logger.error("Camera not available")
            return None
        
        ret, frame = self.camera.read()
        
        if ret:
            if filename:
                cv2.imwrite(filename, frame)
                logger.info(f"Image saved to {filename}")
            return frame
        else:
            logger.error("Failed to capture image")
            return None
    
    def detect_faces(self) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in current frame
        
        Returns:
            List of face bounding boxes (x, y, w, h)
        """
        if not self.camera:
            return []
        
        ret, frame = self.camera.read()
        
        if not ret:
            return []
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        logger.info(f"Detected {len(faces)} face(s)")
        return faces.tolist()
    
    def track_face(self, duration: float = 5.0):
        """
        Track detected face for specified duration
        
        Args:
            duration: Tracking duration in seconds
        """
        if not self.camera:
            return
        
        logger.info("Starting face tracking")
        start_time = time.time()
        
        while time.time() - start_time < duration:
            faces = self.detect_faces()
            
            if len(faces) > 0:
                # Get largest face
                largest_face = max(faces, key=lambda f: f[2] * f[3])
                x, y, w, h = largest_face
                
                # Calculate face center
                face_center_x = x + w // 2
                frame_center_x = 320  # Assuming 640px width
                
                # Simple tracking logic
                if face_center_x < frame_center_x - 50:
                    logger.debug("Face on left, turning left")
                    # Signal to turn head left
                elif face_center_x > frame_center_x + 50:
                    logger.debug("Face on right, turning right")
                    # Signal to turn head right
                else:
                    logger.debug("Face centered")
            
            time.sleep(0.1)
        
        logger.info("Face tracking complete")
    
    def detect_motion(self, threshold: int = 25) -> bool:
        """
        Detect motion in camera feed
        
        Args:
            threshold: Motion detection threshold
            
        Returns:
            True if motion detected
        """
        if not self.camera:
            return False
        
        # Capture two frames
        ret1, frame1 = self.camera.read()
        time.sleep(0.1)
        ret2, frame2 = self.camera.read()
        
        if not (ret1 and ret2):
            return False
        
        # Convert to grayscale
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        # Calculate difference
        diff = cv2.absdiff(gray1, gray2)
        _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
        
        # Count non-zero pixels
        motion_pixels = cv2.countNonZero(thresh)
        motion_detected = motion_pixels > 1000
        
        if motion_detected:
            logger.info("Motion detected")
        
        return motion_detected
    
    def track_object(self, object_name: str = "person"):
        """
        Track specific object
        
        Args:
            object_name: Name of object to track
        """
        logger.info(f"Tracking object: {object_name}")
        
        # This is a placeholder for object tracking
        # In a full implementation, you would use:
        # - YOLO for object detection
        # - OpenCV trackers (CSRT, KCF, etc.)
        # - MediaPipe for specific objects
        
        if not self.camera:
            return
        
        # Simple color-based tracking example
        ret, frame = self.camera.read()
        if ret:
            logger.info(f"Object tracking for {object_name} started")
    
    def get_frame(self) -> Optional[np.ndarray]:
        """Get current camera frame"""
        if not self.camera:
            return None
        
        ret, frame = self.camera.read()
        return frame if ret else None
    
    def detect_colors(self, color_name: str) -> List[Tuple[int, int, int, int]]:
        """
        Detect specific color in frame
        
        Args:
            color_name: Color to detect (red, blue, green, yellow)
            
        Returns:
            List of bounding boxes for detected color regions
        """
        if not self.camera:
            return []
        
        ret, frame = self.camera.read()
        if not ret:
            return []
        
        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Color ranges (HSV)
        color_ranges = {
            'red': ([0, 100, 100], [10, 255, 255]),
            'blue': ([100, 100, 100], [130, 255, 255]),
            'green': ([40, 100, 100], [80, 255, 255]),
            'yellow': ([20, 100, 100], [30, 255, 255]),
        }
        
        if color_name.lower() not in color_ranges:
            logger.warning(f"Unknown color: {color_name}")
            return []
        
        lower, upper = color_ranges[color_name.lower()]
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Get bounding boxes
        boxes = [cv2.boundingRect(c) for c in contours if cv2.contourArea(c) > 500]
        
        logger.info(f"Detected {len(boxes)} {color_name} region(s)")
        return boxes
    
    def cleanup(self):
        """Release camera resources"""
        if self.camera:
            self.camera.release()
            logger.info("Camera released")
