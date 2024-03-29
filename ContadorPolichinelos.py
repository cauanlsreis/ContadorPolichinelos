import cv2
import mediapipe as mp
import math

video = cv2.VideoCapture('polichinelos.mp4')
pose = mp.solutions.pose
Pose = pose.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.5) #variavel de detecção dos pontos
draw = mp.solutions.drawing_utils #variavel responsavel por desenhar no video

contador = 0
check = True

while True:
  success,img = video.read() #Checar a imagem
  videoRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #cONVERTER PARA rgb
  results = Pose.process(videoRGB) #vai receber o resultado da detecção, os pontos d ocorpo
  points = results.pose_landmarks #vai extrair os pontos e coordenadas do corpo de dentro de resultado
  draw.draw_landmarks(img, points, pose.POSE_CONNECTIONS) #tivndo a função de desenhar os pontos

  h,w,_ = img.shape #extraindo as dimensões da imagem de video img
  #identificndo um polichinelo
  if points:
    #extraindo coordenadas (*h *w usado para converter para pixel)
    peDireitoY = int(points.landmark[pose.PoseLandmark.RIGHT_FOOT_INDEX].y*h)
    peDireitoX = int(points.landmark[pose.PoseLandmark.RIGHT_FOOT_INDEX].x*w)

    peEsquerdoY = int(points.landmark[pose.PoseLandmark.LEFT_FOOT_INDEX].y*h)
    peEsquerdoX = int(points.landmark[pose.PoseLandmark.LEFT_FOOT_INDEX].x*w)

    maoDireitaY = int(points.landmark[pose.PoseLandmark.RIGHT_INDEX].y*h)
    maoDireitaX = int(points.landmark[pose.PoseLandmark.RIGHT_INDEX].x*w)

    maoEsquerdaY = int(points.landmark[pose.PoseLandmark.LEFT_INDEX].y*h)
    maoEsquerdaX = int(points.landmark[pose.PoseLandmark.LEFT_INDEX].x*w)

    #calculando a distancia entre as duas mãos
    distMaos = math.hypot(maoDireitaX-maoEsquerdaX, maoDireitaY-maoEsquerdaY)

    # calculando a distancia entre os dois pés
    distPes = math.hypot(peDireitoX-peEsquerdoX, peDireitoY-peEsquerdoY)

    print(f'mãos: {distMaos}, pés: {distPes}')

    #maos <=150 pes >= 150
    if check == True and distMaos <=150 and distPes >=150: #corrigindo porblema de verificação por frames
      contador +=1
      check = False
    if distMaos >= 150 and distPes <= 150:
      check = True

    #inserindo contagem dentro do video
    texto = f'QTD {contador}'
    cv2.rectangle(img,(40,240),(280,120),(255,0,0),-1)
    cv2.putText(img, texto, (40,200), cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)


  cv2.imshow('Resultado', img) #Exibir a variável img
  cv2.waitKey(40) #delay de 40
