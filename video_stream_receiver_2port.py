import cv2
import threading
import signal
import sys

# 프로그램 종료 플래그
terminate = False

# SIGINT 신호가 들어오면 종료 플래그 설정
def int_handler(signum, frame):
    global terminate
    terminate = True

signal.signal(signal.SIGINT, int_handler)

# UDP 스트림을 캡처하는 함수
def capture_stream(port):
    # GStreamer 파이프라인 설정
    gst_pipeline = f"udpsrc port={port} ! application/x-rtp, payload=26 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink"
    capture = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

    # 비디오 캡처가 실패하면 메시지 출력 후 종료
    if not capture.isOpened():
        print(f"VideoCapture open failed on port {port}")
        return

    print(f"Stream on port {port} started")

    while True:
        ret, frame = capture.read()
        if not ret:
            print(f"Read failed on port {port}")
            break

        # 프레임 표시
        cv2.imshow(f"Stream on Port {port}", frame)

        # 'q' 키 또는 종료 플래그로 종료
        if cv2.waitKey(1) & 0xFF == ord('q') or terminate:
            break

    capture.release()
    print(f"Stream on port {port} terminated")

def main():
    # 수신할 포트 리스트
    ports = [5000, 5001]
    threads = []

    # 각 포트에 대한 스레드 생성 및 시작
    for port in ports:
        thread = threading.Thread(target=capture_stream, args=(port,))
        thread.start()
        threads.append(thread)

    # 모든 스레드가 종료될 때까지 대기
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
