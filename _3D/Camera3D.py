from OpenGL.GLU import *
from OpenGL.GLUT import *

Orbital_Cam = False

def switch_cam(w, h):
	"""
	Change le mode de la caméra et demande un réaffichage,
	Camera Globale <-> Camera Embarqué
	"""
	global Orbital_Cam
	Orbital_Cam = not Orbital_Cam
	glutReshapeWindow(w, h)

def cam_lookAt(camPosition, targetPosition, upVector):
	"""
	Défini la caméra selon le mode actuel
	"""
	if Orbital_Cam == False:
		cam_terrain_view(camPosition, targetPosition, upVector)
	else:
		cam_worm_view(targetPosition, upVector)

def cam_terrain_view(camPosition, targetPosition, upVector):
	"""
	Camera globale, regarde le terrain complet
	"""
	gluLookAt(camPosition[0], camPosition[1], camPosition[2],
			targetPosition[0], targetPosition[1], targetPosition[2],
			upVector[0], upVector[1], upVector[2])

def cam_worm_view(upVector):
	"""
	Camera embarqué, qui cible le point d'origine de la scène
	"""
	cam_X = 0
	cam_Y = 7
	cam_Z = 3

	target_X = 0
	target_Y = 0
	target_Z = 0

	gluLookAt(cam_X, cam_Y, cam_Z,
			target_X, target_Y, target_Z,
			upVector[0], upVector[1], upVector[2])

def getCameraMode():
	return Orbital_Cam
