
""" Prototype: Convert Photo or Text to a Simple 3D Model """

# Import required libraries
import cv2
import numpy as np
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection     # Support appearance of 3D shapes

# Function to generate a simple 3D shape from text input
def generate_from_text(user_description):
    print(f"Creating a 3D shape based on the description from user: '{user_description}'")
    shape = user_description.lower()

    # Matching common shape keywords
    if "cube" in shape or "box" in shape:
        model = trimesh.primitives.Box()
    elif "cylinder" in shape:
        model = trimesh.primitives.Cylinder()
    elif "cone" in shape:
        model = trimesh.creation.cone(radius=1.0, height=2.0)
    elif "torus" in shape or "donut" in shape:
        model = trimesh.creation.torus(major_radius=3.0, minor_radius=1.0)
    elif "capsule" in shape:
        model = trimesh.creation.capsule(radius=0.5, height=2.0)
    elif "icosphere" in shape or "ico" in shape:
        model = trimesh.creation.icosphere()
    else:
        model = trimesh.primitives.Sphere()     # Default shape

    model.export("output_text.obj")
    print("3D model from text saved as 'output_text.obj'")
    display_model("output_text.obj")

# Function to generate a simple 3D shape from image input
def generate_from_image(img_path):
    # Load image
    print("Creating a 3D model of the image from user. ")
    try:
        img = cv2.imread(img_path)
        if img is None:
            raise FileNotFoundError("Image could not be read. Check the path and format.")
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    # Resize for complexity reduction
    img = cv2.resize(img, (384, 384))

    # Convert to grayscale to extract brightness for depth
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Edge Detection (Canny) to extract height map
    edges = cv2.Canny(blurred, 100, 200)
    edges_norm = edges / 255.0

    # Contour Detection
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_map = np.zeros_like(gray, dtype=np.uint8)
    cv2.drawContours(contour_map, contours, -1, 255, thickness=cv2.FILLED)
    contour_norm = contour_map / 255.0

    # Combine Edge and Contour maps
    combined = np.maximum(edges_norm, contour_norm)
    heightmap = combined * 0.1 # scale to control the spread of point cloud

    # Convert to 3D vertices
    h, w = heightmap.shape
    vertices = []
    for y in range(h):
        for x in range(w):
            z = heightmap[y, x]
            if z > 0:
                vertices.append([x, y, z])
    vertices = np.array(vertices)

    # Convert to point cloud and export
    point_cloud = trimesh.points.PointCloud(vertices)
    point_cloud.export("output_image.obj")
    print("3D model from image saved as 'output_image.obj'")
    display_model("output_image.obj")

# Display .obj file using matplotlib
def display_model(file_name):
    try:
        model = trimesh.load(file_name)

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')

        if isinstance(model, trimesh.Trimesh):
            vertices = model.vertices
            faces = model.faces

            mesh = Poly3DCollection(vertices[faces], facecolor='orange', edgecolors='k', alpha=0.5)
            ax.add_collection3d(mesh)

            # Use raw vertices for scaling
            ax.auto_scale_xyz(vertices[:, 0], vertices[:, 1], vertices[:, 2])

        elif isinstance(model, trimesh.points.PointCloud):
            vertices = model.vertices
            ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], s=0.5, c=vertices[:, 2], cmap='viridis')

        else:
            print("Unsupported model type for visualization.")
            return

        ax.set_title("3D Model")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Could not display model: {e}")

print("Welcome to the 3D Model Generator!")
choice = input("Would you like to input a 'text' or an 'image'?\n").strip().lower()

if choice == "text":
    description = input("Enter a brief description (e.g., 'a cone'): \n")
    generate_from_text(description)
elif choice == "image":
    image = input("Enter the image file path (e.g., 'picture.jpg'): \n")
    generate_from_image(image)
else:
    print("Invalid choice. Please type 'text' or 'image'.")

