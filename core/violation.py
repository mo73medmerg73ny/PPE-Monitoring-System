import time
import os 
import cv2
import datetime


def iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    inter = max(0, x2-x1) * max(0, y2-y1)

    ar1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    ar2 = (box2[2] - box2[0]) * (box2[3] - box2[1])

    uni = ar1 + ar2 - inter
    return inter / uni


def separate_detections(detections):
    person = []
    hardhat = []
    vest = []

    for (x1, y1, x2, y2, cls_name, conf, track_id) in detections:
        if cls_name == 'Person':
            box = [x1, y1, x2, y2]
            person.append((box, cls_name, conf, track_id))
        elif cls_name == 'Hardhat':
            box = [x1, y1, x2, y2]
            hardhat.append((box, cls_name, conf, track_id))

        else:
            box = [x1, y1, x2, y2]
            vest.append((box, cls_name, conf, track_id))

    return person, hardhat, vest


def check_ppe(person, hardhats, vests):
    results = []

    for (box_p, _, _, track_id) in person:
        has_hardhat = False
        has_vest = False

        for (box_h, _, _, _) in hardhats:
            if iou(box_p, box_h) >= 0.1:
                has_hardhat = True
                break

        for (box_v, _, _, _) in vests:
            if iou(box_p, box_v) >= 0.1:
                has_vest = True
                break

        results.append({
               'id' : track_id,
               'has_hardhat' : has_hardhat,
               'has_vest' : has_vest
                })
        
    return results


def log_violation(results, timers, frame, threshold=5):
    violations = []

    for person in results:
        pid = person['id']
        has_violation = not person['has_hardhat'] or not person['has_vest']

        if has_violation:
            if pid not in timers:
                timers[pid] = {'start': time.time(), 'logged': False}
            
            elif not timers[pid]['logged']:
                elapsed = time.time() - timers[pid]['start']

                if elapsed >= threshold:
                    os.makedirs('violations', exist_ok=True)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    image_path = f'violations/person_{pid}_{timestamp}.jpg'
                    cv2.imwrite(image_path, frame)

                    if not person['has_hardhat']:
                        violations.append({
                            'person_id': pid,
                            'violation_type': 'No Hardhat',
                            'timestamp' : datetime.now(),
                            'image_path' : image_path
                        })

                    if not person['has_vest']:
                        violations.append({
                            'person_id': pid,
                            'violation_type': 'No Vest',
                            'timestamp' : datetime.now(),
                            'image_path' : image_path
                        })
                        
                    timers[pid]['logged'] = True
        else:
            if pid in timers:
                del timers[pid]

    return violations 
