from __future__ import annotations

import cv2
import os
import numpy as np
import random
import time
from typing import Callable

from utils.define_module import define_module
from utils.pipe import Pipe, Notification

notifyPipe: Pipe
log: Callable


def init_module(pipe: Pipe):
    # 模块初始化
    global notifyPipe, log
    notifyPipe = pipe
    log = Notification.create_notifier(pipe, "FACIAL")


def demo():
    time.sleep(1)
    faceid = str(random.randint(0, 99))
    # 环境发生变化
    notifyPipe.send("ENVIRONMENT_ACTIVE")
    time.sleep(2)
    # 识别到人脸
    notifyPipe.send("FACE_ENTER", {"faceid": faceid})

    time.sleep(5)
    # 人脸离开
    notifyPipe.send("FACE_LEAVE")
    time.sleep(10)
    # 环境安静
    notifyPipe.send("ENVIRONMENT_SILENT")


# coding = utf-8


# 随机生成编号
def generate_random_number():
    return random.randint(100000, 999999)


# 遍历yml文件
def list_yml_files(directory):
    yml_files = []
    for file in os.listdir(directory):
        if file.endswith(".yml"):
            yml_files.append(file)
    return yml_files


# 函数：人脸录入
def collect_faces(cap, output_dir, id, face_cascade):
    # 初始化录入计数器
    count = 0

    # 进行人脸录入
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # 转换为灰度图像
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 检测人脸
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

        for (x, y, w, h) in faces:
            # 绘制人脸矩形框
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # 保存人脸图像
            cv2.imwrite(os.path.join(output_dir, f'{id}_{count}.jpg'), gray[y:y + h, x:x + w])
            count += 1

            # 显示人脸数目
            # cv2.putText(frame, f'Faces: {count}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 132, 88), 2)

        # 显示视频流
        # cv2.imshow('Capture Faces', frame)

        # 当录入数量达到指定数目时退出录入
        if count >= 40:
            break
        # 当用户按下空格键退出录入
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break
    cv2.destroyAllWindows()


# 函数：训练人脸识别模型
def train_face_recognizer(input_dir, output_file):
    # 创建LBPH人脸识别器
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    # 加载人脸图像和标签
    faces = []
    labels = []

    for i, filename in enumerate(os.listdir(input_dir)):
        img_path = os.path.join(input_dir, filename)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        faces.append(img)
        labels.append(i)

    # 训练人脸识别模型
    recognizer.train(faces, np.array(labels))

    # 保存模型
    recognizer.save(output_file)

    for filename in os.listdir(input_dir):
        img_path = os.path.join(input_dir, filename)
        os.remove(img_path)


# 判断脸是否存在
def detect_exist(cap, recognizers, face_cascade):
    global changeCount, nowName,missTime
    flag = False
    ret, frame = cap.read()
    if not ret:
        return flag

    # 转换为灰度图像
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 检测人脸
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    for (x, y, w, h) in faces:
        # 绘制人脸矩形框
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 识别人脸
        name = "Unknown"
        min_confidence = 1000
        flag = True
        for recognizer, id in recognizers:
            label, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            if confidence < min_confidence:
                min_confidence = confidence
                name = id

        if min_confidence > 49:
            flag = False
            name = "Unknown"
        log(nowName)
        if name == nowName and name != "Unknown":
            changeCount = 0
        if name != "Unknown" and name != nowName:
            changeCount += 1
            if changeCount >= 5:
                nowName = name
                notifyPipe.send("FACE_ENTER", {
                    "faceid": name
                })
                log(f"Face Enter: {nowName}")
        # cv2.putText(frame, name, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    # cv2.imshow('Face Recognition', frame)

    return flag

# 检测是否有人脸
def detect_face(cap, face_cascade):
    ret, frame = cap.read()
    if not ret:
        return False
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    return len(faces) > 0

# 检测环境变化
def detect_environment_change(cap, prev_frame):
    ret, frame = cap.read()
    if not ret:
        return False, None
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if prev_frame is None:
        return False, gray
    diff = cv2.absdiff(prev_frame, gray)
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    change = np.sum(thresh) / 255
    if change > 5000:
        return True, gray
    return False, gray


# 函数：实时检测与识别
def detect_and_recognize(cap, model_files):
    global missTime,nowName
    count = 0
    last_check_time = time.time()
    # 创建人脸检测器
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # 加载所有训练好的模型
    recognizers = []
    for model_file in model_files:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(model_file)
        recognizers.append((recognizer, model_file[:-4]))
    prev_frame = None
    # 进行实时检测与识别
    while True:
        current_time = time.time()
        if current_time - last_check_time >= 0.5:
            last_check_time = current_time
            environment_changed, prev_frame = detect_environment_change(cap, prev_frame)
            if not detect_face(cap, face_cascade):
                missTime += 1
            if environment_changed and missTime >= 20 :
                nowName = "Unknown"
                missTime = 0
                notifyPipe.send("ENVIRONMENT_ACTIVE")
                log("Environment Active")
            if detect_exist(cap, recognizers, face_cascade) :
                count = 0
                missTime = 0
            elif not detect_exist(cap, recognizers, face_cascade) and detect_face(cap,face_cascade):
                count += 1
            if count >= 10:
                log("New Face Enter")
                count = 0
                random_id = generate_random_number()  # 随机编号
                # 人脸录入
                output_dir = 'faces'

                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                collect_faces(cap, output_dir, random_id, face_cascade)

                # 训练人脸识别模型
                input_dir = 'faces'
                output_file = str(random_id) + '.yml'
                train_face_recognizer(input_dir, output_file)

                # 更新模型列表和识别器
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                recognizer.read(output_file)
                recognizers.append((recognizer, output_file[:-4]))
                model_files.append(output_file)

    # 释放摄像头和关闭窗口
    # cap.release()



cap: cv2.VideoCapture
yml_files: list[str]
nowName = "Unknown"
changeCount = 0
missTime = 0
@define_module("FACIAL")
def main(pipe: Pipe):
    init_module(pipe)
    log('START!')

    def h():
        global cap, yml_files
        current_directory = os.getcwd()  # 获取当前工作目录
        yml_files = list_yml_files(current_directory)  # 获取当前目录中的所有yml文件
        for yml_file in yml_files:
            log(yml_file)
        cap = cv2.VideoCapture(0)

    notifyPipe.run_on_main_thread(h)

    global cap, yml_files
    detect_and_recognize(cap, yml_files)
    notifyPipe.send("ENVIRONMENT_ACTIVE")
