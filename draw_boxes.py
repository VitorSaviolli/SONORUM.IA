import cv2 

def draw(data, frame, allowed_classes):
    if allowed_classes is None or "frets" in allowed_classes:
        for (cx, cy, conf) in data['frets']:
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
    if allowed_classes is None or "frets_box" in allowed_classes:
        for (pt1, pt2, conf) in data['frets_box']:
            x1, y1 = pt1
            x2, y2 = pt2
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 200, 0), 2)

    if allowed_classes is None or "nut" in allowed_classes:
        for (cx, cy, conf) in data['nut']:
            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

    if allowed_classes is None or "neck" in allowed_classes:
        for (pt1, pt2, conf) in data['neck_box']:
            x1, y1 = pt1
            x2, y2 = pt2
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 2)

    return frame
