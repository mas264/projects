
#include <stdlib.h>
#include <math.h>
#include <GL/freeglut.h>
#include "loadTGA.h"


GLuint txId[5];

//Flybot
int rotateWing = 0;
int rotateFlybot = 0;
int fly = 0;

int wingAngleL = -90;
int wingAngleR = 90;
int angle = 25;

float flybotHeight = 0;
float flybotX = 0;

float timesRotated = 1;
int startRotating = 0;


//Robot
int legAngle = 10;
int flagR = 0;
int moveRobotX = 0;
int moveRobotZ = 0;
int rotateArm = 0;
int rotateRobot = 0;
int rotating = 0;
int legHeight = 0;
int bodyHeight = 20;
int armHeight = 0;
int headHeight = 0;
int hatHeight = 0;

//Hedges
float growSize1 = 10;
float growSize2 = 10;
float growSize3 = 10;
float growSize4 = 10;
float growSize5 = 10;
float growSize6 = 10;
float growSize7 = 10;
float growSize8 = 10;
float growSize9 = 10;

//Potted Plant

const int N = 13;
float vx[N] = {0, 5, 5, 4.5, 6, 5.5, 7, 6.5, 8, 7.5, 9, 8.5, 10};
float vy[N] = {0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11};
float vz[N] = {0};
int plantAng = 0;
int flagP = 0;
float rAmount = 1;
float gAmount = 0;
float bAmount = 0; 
int stopPlant = 0;
int colFlag = 0;

//Bridge
int bridgeHeight = -8;
int rotateTop = 0;


int stop = 0;
int step = 0;	
float theta = 0;     
float eye_x = -80,  eye_y = 40,  eye_z = 250; 
float look_x = -80, look_y = 40, look_z = 240;  



void loadTexture()	 
{
	glGenTextures(5, txId);   //Get 5 texture IDs 
	glBindTexture(GL_TEXTURE_2D, txId[0]); 
	loadTGA("Tile.tga");				//For the floor
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);	// Linear Filtering
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
	
	glBindTexture(GL_TEXTURE_2D, txId[1]); 
	loadTGA("Wall.tga");
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
	
	glBindTexture(GL_TEXTURE_2D, txId[2]); 
	loadTGA("GreenHedge.tga");
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
	
	glBindTexture(GL_TEXTURE_2D, txId[3]); 
	loadTGA("RedHedge.tga");
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
	
	glBindTexture(GL_TEXTURE_2D, txId[4]); 
	loadTGA("YellowHedge.tga");
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

}

void special(int key, int x, int y)
{
	
	step = 0;
    if(key == GLUT_KEY_LEFT) angle -= 5;
    else if(key == GLUT_KEY_RIGHT) angle += 5;
	else if(key == GLUT_KEY_DOWN) step = -1;
	else if(key == GLUT_KEY_UP) step = 1;

    
	glutPostRedisplay();
}

void specialKeyboard(unsigned char key, int x, int y)
{
	if(key == 32 && stop == 0) stop = 1;
	else if(key == 32 && stop == 1) stop = 0;
	
	glutPostRedisplay();
}

void floor()
{
	float white[4] = {1., 1., 1., 1.};
	float black[4] = {0};
	glColor4f(0.7, 0.7, 0.7, 1.0);
	glNormal3f(0.0, 1.0, 0.0);

	glBindTexture(GL_TEXTURE_2D, txId[0]);
	glMaterialfv(GL_FRONT, GL_SPECULAR, black);
	
	glBegin(GL_QUADS);
	for(int i = -200; i < 200; i+=20)
	{
		for(int j = -200;  j < 200; j+=20)
		{
			glTexCoord2f(0, 0);	glVertex3f(i, -0.1, j);
			glTexCoord2f(0, 1);	glVertex3f(i, -0.1, j+20);
			glTexCoord2f(1, 1);	glVertex3f(i+20, -0.1, j+20);
			glTexCoord2f(1, 0);	glVertex3f(i+20, -0.1, j);
		}
	}
	glEnd();
	glMaterialfv(GL_FRONT, GL_SPECULAR, white);

}

void walls(float x1, float x2, float z1, float z2)
{

	int wall_height = 20;
	
	//glTexEnvi(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_REPLACE);
	glBindTexture(GL_TEXTURE_2D, txId[1]);
	glBegin(GL_QUADS);
	
		//Front side
		glNormal3f(0, 0, 1);
		glTexCoord2f(15, 1);	glVertex3f(x1, 0, z1);
		glTexCoord2f(0, 1);	glVertex3f(	x2, 0, z1);
		glTexCoord2f(0, 0);	glVertex3f( x2, wall_height, z1);
		glTexCoord2f(15, 0);	glVertex3f(x1, wall_height, z1);
		
		//Back side
		glNormal3f(0, 0, -1);
		glTexCoord2f(15, 0);	glVertex3f(	x2, 0, z2);
		glTexCoord2f(15, 1);	glVertex3f(	x2, wall_height,z2);
		glTexCoord2f(0, 1);	glVertex3f(x1, wall_height, z2);
		glTexCoord2f(0, 0);	glVertex3f(x1, 0, z2);
	
		//Left side
		glNormal3f(-1, 0, 0);
		glTexCoord2f(1, 1);	glVertex3f(x1, 0, z2);
		glTexCoord2f(0, 1);	glVertex3f(x1, 0,z1);
		glTexCoord2f(0, 0);	glVertex3f(x1, wall_height, z1);
		glTexCoord2f(1, 0);	glVertex3f(x1, wall_height, z2);
		
		//Right side
		glNormal3f(1, 0, 0);
		glTexCoord2f(0, 1);	glVertex3f(x2, 0, z1);
		glTexCoord2f(1, 1);	glVertex3f(x2, 0,z2);
		glTexCoord2f(1, 0);	glVertex3f(x2, wall_height, z2);
		glTexCoord2f(0, 0);	glVertex3f(x2, wall_height, z1);
		
		//Top
		glNormal3f(0, 1, 0);
		glTexCoord2f(0, 0);	glVertex3f(x2, wall_height, z1);
		glTexCoord2f(0, 1);	glVertex3f(x2, wall_height,z2);
		glTexCoord2f(15, 1);	glVertex3f(x1, wall_height, z2);
		glTexCoord2f(15, 0);	glVertex3f(x1, wall_height, z1);
	glEnd();


}

void normal(float x1, float y1, float z1, 
            float x2, float y2, float z2,
		      float x3, float y3, float z3 )
{
	  float nx, ny, nz;
	  nx = y1*(z2-z3)+ y2*(z3-z1)+ y3*(z1-z2);
	  ny = z1*(x2-x3)+ z2*(x3-x1)+ z3*(x1-x2);
	  nz = x1*(y2-y3)+ x2*(y3-y1)+ x3*(y1-y2);

      glNormal3f(-nx, -ny, -nz);
}

void pottedPlant(int swayDir)
{
	float wx[N], wy[N], wz[N]; 
	float angle = 10.0*M_PI/180.0;  //Rotate in 10 deg steps (converted 
	
	

	glPushMatrix();
	//  Include code for drawing the surface of revolution here.
	glBegin(GL_TRIANGLE_STRIP);
		for(int j = 0; j < 36; j++) 
		{
			if(colFlag) {
				glColor4f (1, 1, 1, 1);
				colFlag = 0;
			} else {
				glColor4f (0.87, 0.68, 0.18, 1);
				colFlag = 1;
			}
			for(int i = 0; i < N; i++) 
			{	
				wx[i] = (vx[i]*cos(angle)) + (vz[i]*sin(angle));
				wy[i] = vy[i];
				wz[i] = (-vx[i]*sin(angle)) + (vz[i]*cos(angle));
			
				if(i > 0) normal(wx[i-1], wy[i-1], wz[i-1], 
					vx[i-1], vy[i-1], vz[i-1],
					vx[i], vy[i], vz[i]);
				glVertex3f(vx[i], vy[i], vz[i]);
				
				if(i > 0) normal(wx[i-1], wy[i-1], wz[i-1], 
					vx[i], vy[i], vz[i],
					wx[i], wy[i], wz[i]);
				glVertex3f(wx[i], wy[i], wz[i]);
			}
		
			for(int i = 0; i < N; i++) {
				vx[i] = wx[i];
				vy[i] = wy[i];
				vz[i] = wz[i];
			}
		}	
	glEnd();
	glPopMatrix();
	
	glColor4f (0, 1, 0, 1.0); 
	glPushMatrix();
		glRotatef(plantAng*swayDir, 0, 0, 1);
		glTranslatef(0, 7.5, 0);
		glScalef(3, 15, 3);
		glutSolidCube(1);
	glPopMatrix();
	
	glColor4f (rAmount, gAmount, bAmount, 1.0); 
	glPushMatrix();
		glRotatef(plantAng*swayDir, 0, 0, 1);
		glTranslatef(0, 21, 0);
		glutSolidTorus(3, 4, 10, 30); 
		glColor4f (gAmount, bAmount, rAmount, 1.0);
		glutSolidSphere(3, 10, 10);
	glPopMatrix();
	
	
}

void plants()
{
	glPushMatrix();
		glTranslatef(80, 20, 190);
		pottedPlant(1);	
	glPopMatrix();
	glPushMatrix();
		glTranslatef(40, 20, 190);
		pottedPlant(-1);	
	glPopMatrix();
	glPushMatrix();
		glTranslatef(0, 20, 190);
		pottedPlant(1);	
	glPopMatrix();
	glPushMatrix();
		glTranslatef(-40, 20, 190);
		pottedPlant(-1);	
	glPopMatrix();
	glPushMatrix();
		glTranslatef(-80, 20, 190);
		pottedPlant(1);	
	glPopMatrix();
	
}

void makeHedge(float h, GLuint txId)
{


	glBindTexture(GL_TEXTURE_2D, txId);
	glBegin(GL_QUADS);
	 
	//Front
	glNormal3f(0, 0, 1);
	glTexCoord2f(0, 0);		glVertex3f(0, 0, 20);
	glTexCoord2f(1, 0);		glVertex3f(20, 0, 20);
	glTexCoord2f(1, h/20);		glVertex3f(20, h, 20);
	glTexCoord2f(0, h/20);		glVertex3f(0, h, 20);
	
	//Back
	glNormal3f(0, 0, -1);
	glTexCoord2f(1, 0);		glVertex3f(20, 0, 0);
	glTexCoord2f(1, h/20);		glVertex3f(20, h, 0);
	glTexCoord2f(0, h/20);		glVertex3f(0, h, 0);
	glTexCoord2f(0, 0);		glVertex3f(0, 0, 0);
	
	//Left
	glNormal3f(-1, 0, 0);
	glTexCoord2f(0, 0);		glVertex3f(0, 0, 0);
	glTexCoord2f(1, 0);		glVertex3f(0, 0, 20);
	glTexCoord2f(1, h/20);		glVertex3f(0, h, 20);
	glTexCoord2f(0, h/20);		glVertex3f(0, h, 0);
	
	
	//Right
	glNormal3f(1, 0, 0);
	glTexCoord2f(1, 0);		glVertex3f(20, 0, 20);
	glTexCoord2f(0, 0);		glVertex3f(20, 0, 0);
	glTexCoord2f(0, h/20);		glVertex3f(20, h, 0);
	glTexCoord2f(1, h/20);		glVertex3f(20, h, 20);
	
	//Top
	glNormal3f(0, 1, 0);
	glTexCoord2f(1, 1);		glVertex3f(20, h, 20);
	glTexCoord2f(1, 0);		glVertex3f(20, h, 0);
	glTexCoord2f(0, 0);		glVertex3f(0, h, 0);
	glTexCoord2f(0, 1);		glVertex3f(0, h, 20);
	
	
	
	glEnd();
	
}

void hedges(void)
{
	//Growing
	if(rotateFlybot == 130 && flybotX == 150) {
		growSize1 +=  1;
	}
	
	if(rotateFlybot == 120 && flybotX == 150) {
		growSize2 += 2;
	}
	if(rotateFlybot == 110 && flybotX == 150) {
		growSize3 += 3;
	}

	if(rotateFlybot == 100 && flybotX == 150) {
		growSize4 +=  4;
	}
	
	if(rotateFlybot == 90 && flybotX == 150) {
		growSize5 += 5;
	}
	if(rotateFlybot == 80 && flybotX == 150) {
		growSize6 += 4;
	}
	
	if(rotateFlybot == 70&& flybotX == 150) {
		growSize7 +=  3;
	}
	
	if(rotateFlybot == 60 && flybotX == 150) {
		growSize8 += 2;
	}
	if(rotateFlybot == 50 && flybotX == 150) {
		growSize9 += 1;
	}
	
	//Cutting
	if(moveRobotX == -120 && moveRobotZ == -165) {
		growSize1 /= 2;
	}
	if(moveRobotX == -90 && moveRobotZ == -165) {
		growSize2 /= 2;
	}
	if(moveRobotX == -60 && moveRobotZ == -165) {
		growSize3 /= 2;
	}
	if(moveRobotX == -30 && moveRobotZ == -165) {
		growSize4 /= 2;
	}
	if(moveRobotX == 0 && moveRobotZ == -165) {
		growSize5 /= 2;
	}
	if(moveRobotX == 30 && moveRobotZ == -165) {
		growSize6 /= 2;
	}
	if(moveRobotX == 60 && moveRobotZ == -165) {
		growSize7 /= 2;
	}
	if(moveRobotX == 90 && moveRobotZ == -165) {
		growSize8 /= 2;
	}
	if(moveRobotX == 120 && moveRobotZ == -165) {
		growSize9 /= 2;
	}
	
	
	//Generate Hedges
	glPushMatrix();
		glTranslatef(-120, 20, -200);
		makeHedge(growSize1, txId[3]);
	glPopMatrix();
	
	glPushMatrix();
		glTranslatef(-90, 20, -200);
		makeHedge(growSize2, txId[3]);
	glPopMatrix();
	
	glPushMatrix();
		glTranslatef(-60, 20, -200);
		makeHedge(growSize3, txId[3]);
	glPopMatrix();
	glPushMatrix();
	
	glPushMatrix();
		glTranslatef(-30, 20, -200);
		makeHedge(growSize4, txId[2]);
	glPopMatrix();
	
	glTranslatef(0, 20, -200);
		makeHedge(growSize5, txId[2]);
	glPopMatrix();
	
	glPushMatrix();
		glTranslatef(30, 20, -200);
		makeHedge(growSize6, txId[2]);
	glPopMatrix();
	
	glPushMatrix();
		glTranslatef(60, 20, -200);
		makeHedge(growSize7, txId[4]);
	glPopMatrix();
	
	glPushMatrix();
		glTranslatef(90, 20, -200);
		makeHedge(growSize8, txId[4]);
	glPopMatrix();

	glPushMatrix();
		glTranslatef(120, 20, -200);
		makeHedge(growSize9, txId[4]);
	glPopMatrix();
}

void bridge(float r, float g, float b, float a)
{

	glColor4f(r, g, b, a);
	glEnable(GL_BLEND);
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
	glPushMatrix();
		if(flybotHeight < 70){
			glRotatef((flybotHeight+20)*2, 0, 1, 0);
		}
		glTranslatef(-30, (flybotHeight/2)-1, 0);
		glScalef(10, flybotHeight, 10);
		glutSolidCube(1);
	glPopMatrix();
	
	glPushMatrix();
		if(flybotHeight < 70){
			glRotatef((flybotHeight+20)*2, 0, 1, 0);
		}
		glTranslatef(30, (flybotHeight/2)-1, 0);
		glScalef(10, flybotHeight, 10);
		glutSolidCube(1);
	glPopMatrix();
	
	glPushMatrix();
		glTranslatef(0, flybotHeight + bridgeHeight, 0);
		glRotatef(rotateTop, 1, 0, 0);
		glScalef(70, 10, 10);
		glutSolidCube(1);
	glPopMatrix();
	
	if(bridgeHeight < 5 && flybotHeight == 70) {
		bridgeHeight++;
	}
	glDisable(GL_BLEND);
	

}


void flybot(void)
{
	glColor4f(1,0,0,1);			//Body
	glPushMatrix();
		glTranslatef(0, 10, 0);
		glutSolidSphere(10, 20, 20);
	glPopMatrix();
	
	glColor4f(0,0,1,1);			//Head
	glPushMatrix();

		glTranslatef(0, 23, 0);
		glutSolidSphere(5, 20, 20);
	glPopMatrix();
	
	glColor4f(1,1,0,1);	
	glPushMatrix();
		glRotatef(rotateWing, 0, 1, 0);
		glTranslatef(14, 15, 0); // Right Wing
		glRotatef(wingAngleR, 0, 0, 1);
		glScalef(18, 5, 5);
		glutSolidCube(1);
	glPopMatrix();
	
	glColor4f(1,1,0,1);	
	glPushMatrix();

		glRotatef(rotateWing, 0, 1, 0);
		glTranslatef(-14, 15, 0);	//Left Wing
		glRotatef(wingAngleL, 0, 0, 1);
		glScalef(18, 5, 5);
		glutSolidCube(1);
	glPopMatrix();
	
	
}


void robot(void)
{
	
	if(flybotHeight < 30){  //Generating legs
	
	legHeight = flybotHeight;
	glColor4f(0, 1, 0, 1);		
	glPushMatrix();

		glTranslatef(-5, 5, 0);
		glScalef(5, legHeight, 5);
		glutSolidCube(1);
	glPopMatrix();
	
	glColor4f(0, 1, 0, 1);
	glPushMatrix();

		glTranslatef(5, 5, 0);
		glScalef(5, legHeight, 5);
		glutSolidCube(1);
	glPopMatrix();
	
	}
	
	if(flybotHeight < 35 && flybotHeight > 30){ //Generating arms
		armHeight = flybotHeight - legHeight;
		
		glColor4f(0, 1, 0, 1);			//Left Arm
		glPushMatrix();
			glTranslatef(-10, 30, 0);
			glScalef(40, armHeight, 5);
			glutSolidCube(1);
		glPopMatrix();
	
		glColor4f(0, 1, 0, 1);			//Right Arm
		glPushMatrix();
			glTranslatef(10, 30, 0);
			glScalef(40, armHeight, 5);
			glutSolidCube(1);
		glPopMatrix();
	}
		
	if(flybotHeight < 50 && flybotHeight > 30){ //Generating body
		
		bodyHeight = flybotHeight - legHeight;
		
		glColor4f(1, 0, 0, 1);			//Body
		glPushMatrix();
			glTranslatef(0, 30, 0);
			glScalef(20, bodyHeight, 20);
			glutSolidCube(1);
		glPopMatrix();
		glColor4f(1, 0, 1, 1);
		glPushMatrix();
			glTranslatef(0, 30, 10);
			glutSolidSphere(5, bodyHeight, 20);
		glPopMatrix();
	}
	
	if(flybotHeight < 65 && flybotHeight > 50) { //Generating head
	
		headHeight = flybotHeight - (bodyHeight + legHeight);
		
		glColor4f(0, 0, 1, 1);
		glPushMatrix();
			glTranslatef(0, 45, 0);  //Head
			glScalef(15, headHeight, 15);
			glutSolidCube(1);
		glPopMatrix();
		
		
	}
	
	if(flybotHeight < 68 && flybotHeight > 65) {
		
		hatHeight = flybotHeight - (bodyHeight + legHeight + headHeight);
		
		glColor4f(1, 1, 0, 0);
		glPushMatrix();
			glTranslatef(0, 52, 0);  	//Hat
			glRotatef(90, -1, 0, 0);
			glutSolidCone(7.5, 7.5+hatHeight, 7.5, 7.5);
		glPopMatrix();
	}
		
		

	if(flybotHeight >= 65){
	glColor4f(1, 1, 0, 0);
	glPushMatrix();
		glTranslatef(0, 52, 0);  	//Hat
		glRotatef(90, -1, 0, 0);
		glutSolidCone(7.5, 7.5+hatHeight, 7.5, 7.5);
	glPopMatrix();
	}
	
	if(flybotHeight == 70){
	glPushMatrix();
		glTranslatef(0, 65, 0);
		glutSolidSphere(5, 20, 20);
	glPopMatrix();
	}

	if(flybotHeight >= 55){
		glColor4f(0, 0, 1, 1);
		glPushMatrix();
			glTranslatef(0, 45, 0);  //Head
			glScalef(15, headHeight, 15);
			glutSolidCube(1);
		glPopMatrix();
	}

	
	if(flybotHeight >= 40){
		glColor4f(1, 0, 0, 1);			//Body
		glPushMatrix();
			glTranslatef(0, 30, 0);
			glScalef(20, bodyHeight, 20);
			glutSolidCube(1);
		glPopMatrix();
		glColor4f(1, 0, 1, 1);
		glPushMatrix();
			glTranslatef(0, 30, 10);
			glutSolidSphere(5, 20, 20);
		glPopMatrix();
	}
	
		
	if(flybotHeight >= 30){
	glColor4f(0, 1, 0, 1);			//Left Leg
	glPushMatrix();
		if(rotating == 0 && flybotHeight == 70 && !stop) {
			glTranslatef(5, -8, 0);
			glRotatef(-legAngle, 1, 0, 0);
			glTranslatef(-5, 8, 0);
		}
		glTranslatef(-5, 15, 0);
		glScalef(5, legHeight, 5);
		glutSolidCube(1);
	glPopMatrix();
	
	glColor4f(0, 1, 0, 1);			//Right Leg
	glPushMatrix();
		if(rotating == 0 && flybotHeight == 70 && !stop) {
			glTranslatef(-5, 8, 0);
			glRotatef(legAngle, 1, 0, 0);
			glTranslatef(5, -8, 0);
		}
		glTranslatef(5, 15, 0);
		glScalef(5, legHeight, 5);
		glutSolidCube(1);
	glPopMatrix();

	
	glColor4f(0, 1, 0, 1);			//Left Arm
	glPushMatrix();
		glRotatef(rotateArm, 0, 1, 0);
		glTranslatef(-10, 30, 0);
		glScalef(40, armHeight, 5);
		glutSolidCube(1);
	glPopMatrix();
	
	glColor4f(0, 1, 0, 1);			//Right Arm
	glPushMatrix();
		glRotatef(rotateArm, 0, 1, 0);
		glTranslatef(10, 30, 0);
		glScalef(40, armHeight, 5);
		glutSolidCube(1);
	glPopMatrix();
}
}

void display(void)
{
   float lgt_pos[] = {100, 250, 0.0, 1.0};  //light0 position (directly above the origin)
   float head_lgt_pos[] = {flybotX-10, flybotHeight, -10.0, 1.0};
   float head_lgt_dir[] = {-1, -1, 0};
	float shadowMat[16] = {250, 0, 0, 0,
						  -100, 0, -0, -1,
						    0, 0, 250, 0, 
						    0, 0, 0, 250}; 
   

   float dir_x = -sin(theta), dir_y = 0,  dir_z = -cos(theta);
   float d = 2;

   eye_x = eye_x + (step * dir_x);
   eye_y = eye_y + (step * dir_y);
   eye_z = eye_z + (step * dir_z);
	 
	
   look_x = eye_x + (d * dir_x);
   look_y = eye_y + (d * dir_y);
   look_z = eye_z + (d * dir_z);

   glClear (GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);
   glMatrixMode(GL_MODELVIEW);
   glLoadIdentity();

   gluLookAt (eye_x, eye_y, eye_z, look_x, look_y, look_z, 0.0, 1.0, 0.0);
	glLightfv(GL_LIGHT0, GL_POSITION, lgt_pos);   //light position
   
   glRotatef(angle, 0, 1, 0);  //rotate scene based on arrows pushed
   
   glPushMatrix();                                
		glRotatef(rotateFlybot, 0, 1, 0);
		glTranslatef(flybotX+2, 0, 0);
		glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, 20.0f);
		glLightf(GL_LIGHT1, GL_SPOT_EXPONENT, 2.0f);
		glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, head_lgt_dir); 
		glLightfv(GL_LIGHT1, GL_POSITION, head_lgt_pos);
	glPopMatrix();
	
	
	glEnable(GL_TEXTURE_2D);
	floor();
	walls(-200, 200, -180, -200);
	walls(-200, 200, 180, 200);
	hedges();
    glDisable(GL_TEXTURE_2D);
   
	glEnable(GL_LIGHTING);
   glPushMatrix();
	if(fly == 1) {
		if(flybotX == 150) {
			glRotatef(rotateFlybot, 0, 1, 0);
		}
		
	}
	glTranslatef(flybotX, flybotHeight, 0);
	flybot();
   glPopMatrix();
  
	glPushMatrix();
		glTranslatef(moveRobotX, 0, moveRobotZ);
		glRotatef(-rotateRobot, 0, 1, 0);
		glRotatef(90, 0, 1, 0);
		robot();
	glPopMatrix();
   
	glPushMatrix();
		plants();
	glPopMatrix();
	
	glPushMatrix();
		glRotatef(90, 0, 1, 0);
		bridge(0.33, 0.38, 0.90, 1);
	glPopMatrix();
	
	
	glDisable(GL_LIGHTING);
	if(flybotHeight > 0){
		glPushMatrix();
			glMultMatrixf(shadowMat);
			glRotatef(90, 0, 1, 0);
			bridge(0.2, 0.2, 0.2, 1);
		glPopMatrix();
	}
	
	glEnable(GL_LIGHTING);
	

   
   glutSwapBuffers();   //Useful for animation
}



void initialize(void) 
{
    float grey[4] = {0.2, 0.2, 0.2, 1.0};
    float white[4]  = {1.0, 1.0, 1.0, 1.0};
	float blue[4]  = {0.0, 0.0, 1.0, 1.0};

	loadTexture();  
	
	glEnable(GL_LIGHTING);
	glEnable(GL_LIGHT0);
    glLightfv(GL_LIGHT0, GL_AMBIENT, grey);
    glLightfv(GL_LIGHT0, GL_DIFFUSE, white);
    glLightfv(GL_LIGHT0, GL_SPECULAR, white);
    
    
    glEnable(GL_LIGHT1);
    glLightfv(GL_LIGHT1, GL_AMBIENT, grey);
    glLightfv(GL_LIGHT1, GL_DIFFUSE, blue);
    glLightfv(GL_LIGHT1, GL_SPECULAR, white);
    
    
    
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE);
    glEnable(GL_COLOR_MATERIAL);
    
    glMaterialfv(GL_FRONT, GL_SPECULAR, white);
    glMaterialf(GL_FRONT, GL_SHININESS, 50);
    
	glEnable(GL_TEXTURE_2D);
	glEnable(GL_DEPTH_TEST);
	glEnable(GL_NORMALIZE);
	glClearColor (0.0, 0.0, 0.0, 0.0);  //Background colour

    glMatrixMode (GL_PROJECTION);
    glLoadIdentity ();
    gluPerspective(60., 1.0, 10.0, 1000.0);   //Perspective projection
}

void timer(int value)
{
	rotateWing += 10;
	step = 0; //if up or down arrow not pushed stay at current location
	
	if(wingAngleL < 0) {
		wingAngleL++;
	}
	
	if(wingAngleR > 0) {
		wingAngleR--;
	}
	
	if(rotateFlybot == 0 && startRotating == 1){
			timesRotated++;
	}
	if(flybotHeight < 70) {
		flybotHeight++;
	}
	if(flybotHeight == 70 && flybotX < 150) {
		flybotX++;
	}
	
	if(flybotX == 150) {
		rotateFlybot++;
		rotateFlybot = rotateFlybot % 360;
		startRotating = 1;
	}
	
	if(rotateWing > 700) {
		fly = 1;
	}
	
	
	//Robot
	if( legAngle >= -10 && flagR == 0) {
		legAngle--;
		
	} else if (legAngle <= 10){
		legAngle++;
		flagR = 1;
	} else {
		flagR = 0;
	}
	
	if(flybotHeight == 70) {
		if (moveRobotX < 165 && moveRobotX >= 0 && moveRobotZ == 0 && !stop) {
			moveRobotX++;
		}
		rotateArm += 5;
	
		if(moveRobotX == 165 && !stop) {
			if(rotateRobot < 90) {
				rotateRobot++;
				rotateRobot = rotateRobot % 360;
				rotating = 1;
				
			}
			if(rotateRobot == 90 && moveRobotZ < 165) {
				moveRobotZ++;
				rotating = 0;
			}
		}
		
		if(moveRobotZ == 165 && !stop) {
			if(rotateRobot < 180) {
				rotateRobot++;
				rotateRobot = rotateRobot % 360;
				rotating = 1;
			}
			if(rotateRobot == 180 && moveRobotX > -165) {
				moveRobotX--;
				rotating = 0;
			}
		}
		
		if(moveRobotX == -165 && !stop) {
			if(rotateRobot < 270) {
				rotateRobot++;
				rotateRobot = rotateRobot % 360;
				rotating = 1;
				
			}
			if(rotateRobot == 270 && moveRobotZ > -165) {
				moveRobotZ--;
				rotating = 0;
			}
		}
		
		if(moveRobotZ == -165 && !stop) {
			if(rotateRobot < 360 && rotateRobot != 0) {
				rotateRobot++;
				rotateRobot = rotateRobot % 360;
				rotating = 1;
			}
			if(rotateRobot == 0 && moveRobotX < 165) {
				moveRobotX++;
				rotating = 0;
			}
		}
		
	}

	//Plants
	if( plantAng >= -10 && !flagP && !stopPlant) {
		plantAng--;
		
	} else if (plantAng <= 10 && !stopPlant){
		plantAng++;
		flagP = 1;
	} else {
		flagP = 0;
	}
	

	
	if(moveRobotX < 90 && moveRobotX > -90 && moveRobotZ == 165) {
		if(rAmount < 1.0) {
			rAmount += .005;
		} else if (gAmount < 1.0) {
			gAmount +=.005;
		} else if (bAmount < 1.0) {
			bAmount += .005;
		} else {
			rAmount = 0;
			gAmount = 0;
			bAmount = 0;
		}
		stopPlant = 1;
		
	} else {
		stopPlant = 0;
	}
	//Bridge
	rotateTop++;
	rotateTop = rotateTop % 360;
	
	
	glutPostRedisplay();
	glutTimerFunc(50, timer, 0);
	

}


int main(int argc, char** argv)
{
   glutInit(&argc, argv);
   glutInitDisplayMode (GLUT_DOUBLE|GLUT_DEPTH);
   glutInitWindowSize (600, 600); 
   glutInitWindowPosition (50, 50);
   glutCreateWindow ("Robot");
   initialize ();

   glutDisplayFunc(display); 
   glutSpecialFunc(special);
   glutKeyboardFunc(specialKeyboard);
   glutTimerFunc(50, timer, 0);
   glutMainLoop();
   return 0;
}
