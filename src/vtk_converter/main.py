import argparse
import vtk
from stl import mesh

def vtk_to_stl(vtk_filename, stl_filename):
    """
    Converts a .vtk file to a .stl file.
    
    Args:
        vtk_filename (str): Path to the input .vtk file.
        stl_filename (str): Path to save the output .stl file.
    """
    # Create a reader based on the type of input file
    reader = vtk.vtkGenericDataObjectReader()
    reader.SetFileName(vtk_filename)
    reader.Update()
    
    # Get the data from the reader
    data = reader.GetOutput()

    # Check data type and handle accordingly
    if data.IsA('vtkPolyData'):
        poly_data = vtk.vtkPolyData()
        poly_data.DeepCopy(data)
    elif data.IsA('vtkUnstructuredGrid'):
        # Convert unstructured grid to polydata
        geometry_filter = vtk.vtkGeometryFilter()
        geometry_filter.SetInputData(data)
        geometry_filter.Update()
        poly_data = geometry_filter.GetOutput()
    else:
        raise ValueError("Unsupported VTK data type")

    # Convert VTK to STL
    stl_writer = vtk.vtkSTLWriter()
    stl_writer.SetFileName(stl_filename)
    stl_writer.SetInputData(poly_data)
    stl_writer.Write()
    print(f"Converted {vtk_filename} to {stl_filename}")

def stl_to_obj(stl_filename, obj_filename):
    """
    Converts a .stl file to a .obj file.
    
    Args:
        stl_filename (str): Path to the input .stl file.
        obj_filename (str): Path to save the output .obj file.
    """
    # Read STL file
    stl_mesh = mesh.Mesh.from_file(stl_filename)
    
    # Create OBJ file
    with open(obj_filename, 'w') as obj_file:
        # Write vertices
        for vertex in stl_mesh.vectors.reshape(-1, 3):
            obj_file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        
        # Write faces
        num_faces = len(stl_mesh.vectors)
        for i in range(num_faces):
            obj_file.write(f"f {3*i+1} {3*i+2} {3*i+3}\n")
    print(f"Converted {stl_filename} to {obj_filename}")

def convert_vtk_to_stl_and_obj(vtk_filename, stl_filename, obj_filename):
    """
    Converts a .vtk file to both .stl and .obj files.
    
    Args:
        vtk_filename (str): Path to the input .vtk file.
        stl_filename (str): Path to save the output .stl file.
        obj_filename (str): Path to save the output .obj file.
    """
    # Convert VTK to STL
    vtk_to_stl(vtk_filename, stl_filename)
    
    # Convert the generated STL to OBJ
    stl_to_obj(stl_filename, obj_filename)

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='Input file to convert')
    args = parser.parse_args()

    input_file = args.input_file

    output_stl_file = "scaffold.stl"
    output_obj_file = "scaffold.obj"

    print(f"Converting {input_file} to {output_stl_file} and {output_obj_file}")
    convert_vtk_to_stl_and_obj(input_file, output_stl_file, output_obj_file)