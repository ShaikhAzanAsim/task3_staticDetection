import cv2

# Load the ideal empty-store background image
ideal = cv2.imread('reference.png')
ideal_gray = cv2.cvtColor(ideal, cv2.COLOR_BGR2GRAY)

# Open the busy-store video
cap = cv2.VideoCapture('output_1min.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)
threshold_frames = int(5 * fps)  # 10 seconds

tracked = []

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # --- Step 1: Difference with ideal ---
    diff = cv2.absdiff(frame_gray, ideal_gray)

    # Debug: raw difference
    cv2.imshow("1. Raw Difference", cv2.resize(diff, (diff.shape[1]//3, diff.shape[0]//3)))

    # --- Step 2: Threshold ---
    _, fgMask = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)

    # Debug: after threshold
    cv2.imshow("2. Thresholded Mask", cv2.resize(fgMask, (fgMask.shape[1]//3, fgMask.shape[0]//3)))

    # --- Step 3: Morphological cleaning ---
    fgMask = cv2.morphologyEx(
        fgMask,
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    )

    # Debug: after morphology
    cv2.imshow("3. Cleaned Mask", cv2.resize(fgMask, (fgMask.shape[1]//3, fgMask.shape[0]//3)))

    # --- Step 4: Contours ---
    contours, _ = cv2.findContours(fgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    new_tracked = []
    print(f"Frame: {int(cap.get(cv2.CAP_PROP_POS_FRAMES))}, Contours detected: {len(contours)}")
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 500:  # filter noise
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        print(f"   Contour -> x:{x}, y:{y}, w:{w}, h:{h}, area:{area}")

        matched = False
        for obj in tracked:
            x2, y2, w2, h2 = obj['bbox']
            if abs(x - x2) < 10 and abs(y - y2) < 10:
                obj['bbox'] = (x, y, w, h)
                obj['count'] += 1
                new_tracked.append(obj)
                matched = True
                break
        if not matched:
            new_tracked.append({'bbox': (x, y, w, h), 'count': 1})
    tracked = new_tracked

    # --- Step 5: Draw bounding boxes ---
    debug_frame = frame.copy()
    for obj in tracked:
        x, y, w, h = obj['bbox']
        if obj['count'] >= threshold_frames:
            cv2.rectangle(debug_frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(debug_frame, "Abandoned", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Debug: show frame with boxes
    h, w = debug_frame.shape[:2]
    cv2.imshow("4. Frame with Bounding Boxes", cv2.resize(debug_frame, (w//3, h//3)))

    # Quit with 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
