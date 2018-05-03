/*========================================================================
* COSC 363  Computer Graphics (2017)
* Ray tracer 
* See Lab07.pdf for details. NO ANTI_ALIASING
*=========================================================================
*/

//Set build command to [g++ -Wall -o "%e" RayTracer.cpp Ray.cpp SceneObject.cpp Sphere.cpp Plane.cpp TextureBMP.cpp -lm -lGL -lGLU -lglut]
#include <iostream>
#include <cmath>
#include <vector>
#include <glm/glm.hpp>
#include "Sphere.h"
#include "SceneObject.h"
#include "Ray.h"
#include <GL/glut.h>
#include "Plane.h"
#include "TextureBMP.h"


#include <stdio.h>


using namespace std;

const float WIDTH = 20.0;  
const float HEIGHT = 20.0;
const float EDIST = 40.0;
const int NUMDIV = 500;
const int MAX_STEPS = 5;
const float XMIN = -WIDTH * 0.5;
const float XMAX =  WIDTH * 0.5;
const float YMIN = -HEIGHT * 0.5;
const float YMAX =  HEIGHT * 0.5;

vector<SceneObject*> sceneObjects;  //A global list containing pointers to objects in the scene
TextureBMP floor_texture, sphere_texture;

//---The most important function in a ray tracer! ---------------------------------- 
//   Computes the colour value obtained by tracing a ray and finding its 
//     closest point of intersection with objects in the scene.
//----------------------------------------------------------------------------------
glm::vec3 trace(Ray ray, int step)
{
	glm::vec3 backgroundCol(0);
	glm::vec3 light1(-18, 40, -3);
	glm::vec3 light2(15, -10, -30);
	//glm::vec3 light2(15, 80, 10);
	float ambientTerm = 0.2;
	float glass = 1/1.5;
	float magnifier = 1/1.01;
	glm::vec3 specCol(0);
	ray.closestPt(sceneObjects);		//Compute the closest point of intersetion of objects with the ray
	glm:: vec3 colorSum;
	if(ray.xindex == -1) return backgroundCol;      //If there is no intersection return background colour
	glm::vec3 col = sceneObjects[ray.xindex]->getColor(); //else return bject's colour
	
	
	//for light1
	glm:: vec3 normalVector = sceneObjects[ray.xindex]->normal(ray.xpt);
	glm:: vec3 lightVector1 = light1 - ray.xpt;
	lightVector1 = glm:: normalize(lightVector1);
	float lDotn1 = glm:: dot(lightVector1,normalVector); 
	glm:: vec3 reflVector1 = glm::reflect(-lightVector1, normalVector);
	float rDotv1 = glm:: dot(reflVector1,-ray.dir) ; 
	
	Ray shadow1(ray.xpt, lightVector1);
	shadow1.closestPt(sceneObjects);
	float lightDist1 = glm:: distance(light1, ray.xpt);

	
	//for light2
	glm:: vec3 lightVector2 = light2 - ray.xpt;
	lightVector2 = glm:: normalize(lightVector2);
	float lDotn2 = glm:: dot(lightVector2,normalVector); 
	glm:: vec3 reflVector2 = glm::reflect(-lightVector2, normalVector);
	float rDotv2 = glm:: dot(reflVector2,-ray.dir) ; 
	
	Ray shadow2(ray.xpt, lightVector2);
	shadow2.closestPt(sceneObjects);
	float lightDist2 = glm:: distance(light2, ray.xpt);

	//light1
	if(rDotv1 >= 0||rDotv2 >= 0) specCol = glm:: vec3(1); 
	
	if((shadow1.xindex == 1 && shadow1.xdist < lightDist1))
		colorSum = col * sceneObjects[1]->getColor();
	if((shadow1.xindex == 3 && shadow1.xdist < lightDist1))
		colorSum = col * sceneObjects[3]->getColor();

	if(lDotn1 <= 0 || (shadow1.xindex>-1 && shadow1.xdist < lightDist1))
		colorSum = glm:: vec3(ambientTerm * col);

	else 
		colorSum = glm:: vec3(ambientTerm*col + lDotn1*col + pow(rDotv1,10)*specCol);
	
	//light2
	
	if((shadow2.xindex == 1 && shadow2.xdist < lightDist2))
		colorSum += colorSum * sceneObjects[1]->getColor();
	if((shadow2.xindex == 3 && shadow2.xdist < lightDist2))
		colorSum += colorSum * sceneObjects[3]->getColor();
	
	if(lDotn2 <= 0 || (shadow2.xindex>-1 && shadow2.xdist < lightDist2))
		colorSum += glm:: vec3(ambientTerm * col);

	else 
		colorSum += glm:: vec3(ambientTerm*col + lDotn2*col + pow(rDotv2,10)*specCol);

		
	if(ray.xindex == 0 && step < MAX_STEPS)
	{
		glm:: vec3 reflectedDir = glm:: reflect(ray.dir, normalVector);
		Ray reflectedRay(ray.xpt, reflectedDir);
		glm:: vec3 reflectedCol = trace(reflectedRay, step+1); //recursion
		colorSum = colorSum + (0.8f*reflectedCol);
	}
	

	if(ray.xindex == 2)											//Patterned Sphere
	{
		
		if(sin(M_PI*ray.xpt.x/0.7)+ sin(M_PI*ray.xpt.y/0.7)>0)		//Checkered Pattern
			col = glm:: vec3(1, 0, 0);
		else
			col = glm:: vec3(0, 1, 0);
		
		/*--Horizontal Stripe Pattern---
		if(sin(M_PI*ray.xpt.y/0.7)>0)					
			col += glm:: vec3(1, 0, 0);
		else
			col += glm:: vec3(0, 1, 0);	
	
		
		--3d Checkerboard Pattern---
		if (((int)(ray.xpt.x/0.5) + (int)(ray.xpt.y/0.5) + (int)(ray.xpt.z/0.5)) % 2 == 0)
			col = glm:: vec3(1, 0, 0);
		else
			col = glm:: vec3(0, 1, 0);*/

		
		if(lDotn1 <= 0 || (shadow1.xindex>-1 && shadow1.xdist < lightDist1))
			colorSum = glm:: vec3(ambientTerm * col);
		else 
			colorSum = glm:: vec3(ambientTerm*col + lDotn1*col + pow(rDotv1,10)*specCol);
		
			
		if(lDotn2 <= 0 || (shadow2.xindex>-1 && shadow2.xdist < lightDist2))
			colorSum +=  colorSum * glm:: vec3(ambientTerm * col);
		else
			colorSum += glm:: vec3(ambientTerm*col + lDotn2*col + pow(rDotv2,10)*specCol);

			
	}
	
	if(ray.xindex == 5)									//Image Textured Sphere
	{
		
		float texcoords = 0.5 + (atan2(ray.xpt.z+110, ray.xpt.x+10)/(2*M_PI));
		float texcoordt = 0.5 - asin((ray.xpt.y-10)/5)/ (M_PI);
		col = sphere_texture.getColorAt(texcoords, texcoordt);
		
		
		if(lDotn1 <= 0 || (shadow1.xindex>-1 && shadow1.xdist < lightDist1))
			colorSum = glm:: vec3(ambientTerm * col);
		else 
			colorSum = glm:: vec3(ambientTerm*col + lDotn1*col + pow(rDotv1,10)*specCol);
		
			
		if(lDotn2 <= 0 || (shadow2.xindex>-1 && shadow2.xdist < lightDist2))
			colorSum +=  colorSum * glm:: vec3(ambientTerm * col);
		else
			colorSum += glm:: vec3(ambientTerm*col + lDotn2*col + pow(rDotv2,10)*specCol);

	}
	
	if(ray.xindex == 4)									//Texture for the plane
	{
		
		float texcoords = (ray.xpt.x + 20)/ 40;
		float texcoordt = (ray.xpt.z)/ -200;
		
		colorSum = floor_texture.getColorAt(texcoords, texcoordt);
		
		//light1
		if((shadow1.xindex == 1 && shadow1.xdist < lightDist1))
			colorSum = glm:: vec3(0.7f * colorSum) + glm:: vec3(0.3f * sceneObjects[1]->getColor());

		if((shadow1.xindex == 3 && shadow1.xdist < lightDist1))
			colorSum = glm:: vec3(0.7f * colorSum) + glm:: vec3(0.3f * sceneObjects[3]->getColor());
	 
		if ((lDotn1 <= 0 || (shadow1.xindex>-1 && shadow1.xdist < lightDist1)) && (shadow1.xindex != 1 && shadow1.xindex != 3))
				colorSum = glm:: vec3(ambientTerm * colorSum);
		

		//light2
		if((shadow2.xindex == 1 && shadow2.xdist < lightDist2))
			colorSum = glm:: vec3(0.7f * colorSum) + glm:: vec3(0.3f * sceneObjects[1]->getColor());

		if((shadow2.xindex == 3 && shadow2.xdist < lightDist2))
			colorSum = glm:: vec3(0.7f * colorSum) + glm:: vec3(0.3f * sceneObjects[3]->getColor());
	
		if ((lDotn2 <= 0 || (shadow2.xindex>-1 && shadow2.xdist < lightDist2)) && (shadow2.xindex != 1 && shadow2.xindex != 3))
			colorSum = glm:: vec3(ambientTerm * colorSum);

	}
	
	
	if(ray.xindex == 1 && step < MAX_STEPS)						//Glass Sphere
	{
		glm:: vec3 g = refract(ray.dir, normalVector, glass);
		Ray refractedRay1(ray.xpt, g);
		refractedRay1.closestPt(sceneObjects);
		glm:: vec3 m = sceneObjects[refractedRay1.xindex]->normal(refractedRay1.xpt);
		glm:: vec3 h = glm:: refract(g, -m, 1.0f/glass);
		Ray refractedRay2(refractedRay1.xpt, h);
		glm:: vec3 refractedCol = trace(refractedRay2, step+1); //recursion
		colorSum = colorSum + (0.8f*refractedCol);
		
			
	}
	
	if(ray.xindex == 3 && step < MAX_STEPS)						//Cyan magnified Sphere
	{
		glm:: vec3 g = refract(ray.dir, normalVector, magnifier);
		Ray refractedRay1(ray.xpt, g);
		refractedRay1.closestPt(sceneObjects);
		glm:: vec3 m = sceneObjects[refractedRay1.xindex]->normal(refractedRay1.xpt);
		glm:: vec3 h = glm:: refract(g, -m, 1.0f/magnifier);
		Ray refractedRay2(refractedRay1.xpt, h);
		glm:: vec3 refractedCol = trace(refractedRay2, step+1); //recursion
		colorSum = colorSum + (0.8f*refractedCol);
			
	}
	
	return colorSum;
}

//---The main display module -----------------------------------------------------------
// In a ray tracing application, it just displays the ray traced image by drawing
// each cell as a quad.
//---------------------------------------------------------------------------------------
void display()
{
	float xp, yp;  //grid point
	float cellX = (XMAX-XMIN)/NUMDIV;  //cell width
	float cellY = (YMAX-YMIN)/NUMDIV;  //cell height

	glm::vec3 eye(0., 0., 0.);  //The eye position (source of primary rays) is the origin

	glClear(GL_COLOR_BUFFER_BIT);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

	glBegin(GL_QUADS);  //Each cell is a quad.

	for(int i = 0; i < NUMDIV; i++)  	//For each grid point xp, yp
	{
		
		for(int j = 0; j < NUMDIV; j++)
		{
			xp = XMIN + i*cellX;
			yp = YMIN + j*cellY;

		    glm::vec3 dir(xp+0.5*cellX, yp+0.5*cellY, -EDIST);	//direction of the primary ray

		    Ray ray = Ray(eye, dir);		//Create a ray originating from the camera in the direction 'dir'
			ray.normalize();				//Normalize the direction of the ray to a unit vector
		    glm::vec3 col = trace (ray, 1); //Trace the primary ray and get the colour value

			glColor3f(col.r, col.g, col.b);
			glVertex2f(xp, yp);				//Draw each cell with its color value
			glVertex2f(xp+cellX, yp);
			glVertex2f(xp+cellX, yp+cellY);
			glVertex2f(xp, yp+cellY);
        }
    }

    glEnd();
    glFlush();
}

void drawCube(float top, float bottom, float left, float right, float near, float far, glm::vec3 col)
{
	
	Plane *p1 = new Plane (glm::vec3(left,bottom,far),
							glm::vec3(left,bottom,near),			//Bottom
							glm::vec3(right,bottom,near),
							glm::vec3(right,bottom,far), 
							col);
								
	Plane *p2 = new Plane (glm::vec3(left,top,far),
							glm::vec3(left,top,near),			//Top
							glm::vec3(right,top,near),
							glm::vec3(right,top,far), 
							col);
								
	Plane *p3 = new Plane (glm::vec3(left,bottom,far),			//Left
							glm::vec3(left,top,far),
							glm::vec3(left,top,near),
							glm::vec3(left,bottom,near),
							col);
								
	Plane *p4 = new Plane (glm::vec3(right,bottom,far),			//Right
							glm::vec3(right,top,far),
							glm::vec3(right,top,near),
							glm::vec3(right,bottom,near),
							col);

	Plane *p5 = new Plane (glm::vec3(left,bottom,far),			//Far
							glm::vec3(left,top,far),
							glm::vec3(right,top,far),
							glm::vec3(right,bottom,far),
							col);
								
	Plane *p6 = new Plane (glm::vec3(left,bottom,near),			//near
								glm::vec3(right,bottom,near),
								glm::vec3(right,top,near),
								glm::vec3(left,top,near),
								col);
								
	sceneObjects.push_back(p1);  //index 4 - 9
	sceneObjects.push_back(p2);
	sceneObjects.push_back(p3);
	sceneObjects.push_back(p4);
	sceneObjects.push_back(p5);
	sceneObjects.push_back(p6);
	
}

void drawTetrahedron(float bottom, float top, float left, float right, float near, float far, glm::vec3 col)
{
	
	float mid_x = (left + right)/ 2;
	float mid_z = (near + far)/ 2;
	
	
	Plane *p1 = new Plane (glm::vec3(left,bottom,far),
							glm::vec3(left,bottom,near),			//Bottom
							glm::vec3(right,bottom,near),
							glm::vec3(right,bottom,far), 
							col);
	
	Plane *p2 = new Plane (glm::vec3(left,bottom,near),
							glm::vec3(mid_x,top,mid_z),
							glm::vec3(mid_x,top,mid_z), 
							glm::vec3(left,bottom,far),			//Left
							col);
	
	Plane *p3 = new Plane (glm::vec3(right,bottom,near),
							glm::vec3(mid_x,top,mid_z),
							glm::vec3(mid_x,top,mid_z), 
							glm::vec3(right,bottom,far),			//Right
							col);
							
	Plane *p4 = new Plane (glm::vec3(right,bottom,far),
							glm::vec3(left,bottom,far),
							glm::vec3(mid_x,top,mid_z),
							glm::vec3(mid_x,top,mid_z),		//Far
							col);
							
	Plane *p5 = new Plane (glm::vec3(right,bottom,near),
							glm::vec3(mid_x,top,mid_z),
							glm::vec3(mid_x,top,mid_z),		//Near
							glm::vec3(left,bottom,near),
							col);
							
							
	sceneObjects.push_back(p1);			//index 10-14
	sceneObjects.push_back(p2);
	sceneObjects.push_back(p3);
	sceneObjects.push_back(p4);
	sceneObjects.push_back(p5);
	
}


//---This function initializes the scene ------------------------------------------- 
//   Specifically, it creates scene objects (spheres, planes, cones, cylinders etc)
//     and add them to the list of scene objects.
//   It also initializes the OpenGL orthographc projection matrix for drawing the
//     the ray traced image.
//----------------------------------------------------------------------------------
void initialize()
{
    glMatrixMode(GL_PROJECTION);
    gluOrtho2D(XMIN, XMAX, YMIN, YMAX);
    glClearColor(0, 0, 0, 1);
	floor_texture = TextureBMP("Floor.bmp");
	sphere_texture = TextureBMP("Sphere.bmp");

	//-- Create a pointer to a sphere object
	Sphere *sphere1 = new Sphere(glm::vec3(-5.0, -5.0, -120.0), 15.0, glm::vec3(0, 0, 1));
	Sphere *sphere2 = new Sphere(glm::vec3(8, -15, -80), 3, glm::vec3(0, 0, 0));
	Sphere *sphere3 = new Sphere(glm::vec3(5, 0, -100), 4, glm::vec3(0, 0, 0)); 
	Sphere *sphere4 = new Sphere(glm::vec3(-4, -13, -80), 5, glm::vec3(0, 0.5, 0.5)); 
	Sphere *sphere5 = new Sphere(glm::vec3(-10, 10, -110), 5, glm::vec3(0, 0, 0)); 
	Sphere *sphere6 = new Sphere(glm::vec3(15, 18, -130), 5, glm::vec3(1, 0, 0));  
	
	Plane *plane1 = new Plane (glm::vec3(-20.,-20,0),
								glm::vec3(20.,-20,0),
								glm::vec3(20.,-20,-200),
								glm::vec3(-20.,-20,-200),
								glm::vec3(0.5,0,0.5));
	
	Plane *plane2 = new Plane (glm::vec3(20,-20,0),
								glm::vec3(20.,50,0),
								glm::vec3(20.,50,-200),
								glm::vec3(20.,-20,-200),
								glm::vec3(0.5,0.,0.5));						
	
	Plane *plane3 = new Plane (glm::vec3(-20,-20,0),
								glm::vec3(-20.,-20,-200),
								glm::vec3(-20.,50,-200),
								glm::vec3(-20.,50,0),
								glm::vec3(0.5,0.,0.5));		
								
	Plane *plane4 = new Plane (glm::vec3(-20,-20,-200),
								glm::vec3(20.,-20,-200),
								glm::vec3(20.,50,-200),
								glm::vec3(-20.,50,-200),
								glm::vec3(0.5,0.,0.5));	
								
	Plane *plane5 = new Plane (glm::vec3(-20,-20,0),
								glm::vec3(20.,-20,0),
								glm::vec3(20.,50,0),
								glm::vec3(-20.,50,0),
								glm::vec3(0.5,0.,0.5));					
	

	//Cylinder *c = new Cylinder(3, 3, 5, glm::vec3(0, 1, 0));
	//--Add the above to the list of scene objects.
	
	
	
	
	sceneObjects.push_back(sphere1); 
	sceneObjects.push_back(sphere2); 
	sceneObjects.push_back(sphere3);
	sceneObjects.push_back(sphere4);
	sceneObjects.push_back(plane1);
	sceneObjects.push_back(sphere5);
	sceneObjects.push_back(sphere6);
	sceneObjects.push_back(plane2);
	sceneObjects.push_back(plane3);
	sceneObjects.push_back(plane4);
	sceneObjects.push_back(plane5);
 	drawCube(-5, -10, -10, -5, -85, -90, glm:: vec3(.7,.7,0));
 	drawTetrahedron(-5, 0, 10, 15, -75, -80, glm::vec3(0.5,0,0.5));

	//sceneObjects.push_back(sphere4);
	//sceneObjects.push_back(c);
}



int main(int argc, char *argv[]) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB );
    glutInitWindowSize(600, 600);
    glutInitWindowPosition(20, 20);
    glutCreateWindow("Raytracer");

    glutDisplayFunc(display);
    initialize();

    glutMainLoop();
    return 0;
}
