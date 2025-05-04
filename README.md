TEXT OR IMAGE TO 3D MODEL GENERATOR


This Python project allows users to input either a 'text' or an 'image', and converts it into a simple 3D object. The 3D object is saved as an `.obj` file and visualized using Matplotlib in a 3D scatter plot.


Features -
* _Text Input_: Supports basic shapes like cube, cone, cylinder, pyramid, torus, etc.
* _Image Input_: Converts image brightness into a 3D point cloud.
* _Output_: Saves `.obj` file for use in Blender, MeshLab, or any 3D viewer.
* _Visualization_: Displays the model using an interactive 3D scatter plot via Matplotlib.


Requirements -

_Install dependencies with_:
pip install -r requirements.txt

_Dependencies_: 
* opencv-python
* numpy
* matplotlib
* trimesh


How to Use - 

_Run the script_:
python text_image_to_3d_model.py

_Choose between_:
* "text" → Type a shape description (e.g., "a small torus")
* "image" → Provide path to an image (e.g., "myobject.jpg")

_The script will_:
* Generate a simple 3D shape or point cloud
* Save the model (.obj)
* Visualizes the model using Matplotlib in a 3D scatter plot

_Output Files_:
* Text	'output_text.obj'
* Image	'output_image.obj'

These files can be opened using Blender, MeshLab, or Windows 3D Viewer.


_Supported Shapes for Text_: 
Cube / Box, Cylinder, Cone, Torus / Donut, Capsule, Icosphere, Pyramid, Anything else defaults to Sphere


THOUGHT PROCESS

The goal was to build a lightweight, beginner-friendly tool that simulates AI-powered 3D model generation from text or image.
 Used 'opencv', 'trimesh', 'numpy', and 'matplotlib' for simplicity.

Libraries Used - 
* _opencv-python_:	Loads and processes image files (resize, grayscale conversion)
* _numpy_:	Handles matrix/grid operations for point cloud generation
* _matplotlib_:	Visualizes the 3D models as scatter plots 
* _trimesh_:	Generates 3D shape primitives (cube, cone, etc.) and handles .obj export

Two Modes of Operation - 

_Text-based Input_:
* Matches keywords like "cube", "cone", etc.
* Uses trimesh to generate basic 3D primitives
* Saves and displays the shape using matplotlib

_Image-based Input_:
* Reads an image using opencv
* Converts it to grayscale → brightness represents depth
* Uses numpy to build a 3D point cloud
* Uses trimesh.points.PointCloud() to save as .obj
* Displays the 3D point cloud using matplotlib

Output Format -
* Chose .obj for its simplicity and wide compatibility
* Easy to inspect, share, and open in any 3D software