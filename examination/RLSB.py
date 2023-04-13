# 人脸识别

"""


import cv2
import dlib
import numpy as np

# 加载facenet模型
model_path = "model/20180402-114759.pb"
net = cv2.dnn.readNetFromTensorflow(model_path)

# 加载人脸检测器和面部对齐器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("model/shape_predictor_68_face_landmarks.dat")

# 收集3个人的人脸特征向量和标签
data = {}
data["person1"] = np.zeros((10, 128))
data["person2"] = np.zeros((10, 128))
data["person3"] = np.zeros((10, 128))
labels = ["person1", "person2", "person3"]

# 对每个人的图片进行人脸检测和对齐，并提取特征向量
def extract_features(person, label):
    for i in range(10):
        img_path = f"{person}/{i+1}.jpg"
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        if len(faces) == 1:
            face = faces[0]
            landmarks = predictor(gray, face)
            aligned_face = dlib.get_face_chip(img, landmarks)
            blob = cv2.dnn.blobFromImage(aligned_face, 1.0/255, (160, 160))
            net.setInput(blob)
            features = net.forward().flatten()
            data[label][i] = features

# 提取特征向量
extract_features("person1", "person1")
extract_features("person2", "person2")
extract_features("person3", "person3")

# 输入一个新的人脸图片并识别
test_img = cv2.imread("test.jpg")
gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
faces = detector(gray)
if len(faces) == 1:
    face = faces[0]
    landmarks = predictor(gray, face)
    aligned_face = dlib.get_face_chip(test_img, landmarks)
    blob = cv2.dnn.blobFromImage(aligned_face, 1.0/255, (160, 160))
    net.setInput(blob)
    test_features = net.forward().flatten()
    # 计算相似度
    scores = []
    for label in labels:
        for i in range(10):
            features = data[label][i]
            score = np.dot(features, test_features) / np.linalg.norm(features) / np.linalg.norm(test_features)
            scores.append((score, label))
    scores.sort(reverse=True)
    print(f"Matched person: {scores[0][1]}")


"""

"""
# Import necessary libraries for face recognition


import face_recognition

# Load images of the three people
person1_image = face_recognition.load_image_file("person1.jpg")
person2_image = face_recognition.load_image_file("person2.jpg")
person3_image = face_recognition.load_image_file("person3.jpg")

# Get the face encodings of the three people
person1_encoding = face_recognition.face_encodings(person1_image)[0]
person2_encoding = face_recognition.face_encodings(person2_image)[0]
person3_encoding = face_recognition.face_encodings(person3_image)[0]

# Create a list of the face encodings and their corresponding names
known_face_encodings = [
    person1_encoding,
    person2_encoding,
    person3_encoding
]
known_face_names = [
    "Person 1",
    "Person 2",
    "Person 3"
]

# Load the image to be recognized
unknown_image = face_recognition.load_image_file("unknown.jpg")

# Get the face encoding of the unknown image
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

# Compare the unknown face encoding with the known face encodings
results = face_recognition.compare_faces(known_face_encodings, unknown_encoding)

# Get the name of the person with the closest match
for i in range(len(results)):
    if results[i]:
        print(known_face_names[i])
"""

"""
# Import necessary libraries
import face_recognition

# Load images of the three people
person_1_image = face_recognition.load_image_file("person_1.jpg")
person_2_image = face_recognition.load_image_file("person_2.jpg")
person_3_image = face_recognition.load_image_file("person_3.jpg")

# Encode the images
person_1_encoding = face_recognition.face_encodings(person_1_image)[0]
person_2_encoding = face_recognition.face_encodings(person_2_image)[0]
person_3_encoding = face_recognition.face_encodings(person_3_image)[0]

# Create a list of the encodings and their corresponding names
known_face_encodings = [
    person_1_encoding,
    person_2_encoding,
    person_3_encoding
]
known_face_names = [
    "Person 1",
    "Person 2",
    "Person 3"
]

# Load the image to be recognized
unknown_image = face_recognition.load_image_file("unknown.jpg")

# Encode the unknown image
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

# Compare the unknown encoding with the known encodings
results = face_recognition.compare_faces(known_face_encodings, unknown_encoding)

# Check which known face encoding matches the unknown encoding
for i in range(len(results)):
    if results[i]:
        print("The person in the unknown image is:", known_face_names[i])
"""