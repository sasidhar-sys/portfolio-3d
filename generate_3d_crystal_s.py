import numpy as np
import trimesh
import pygltflib
import json
import os

def create_smooth_s_curve(num_samples=300):
    """
    Generates a ultra-smooth, CAD-quality symmetrical 'S' centerline curve.
    Uses cubic Bezier composite curves for flawless continuity (C2-like smoothness).
    """
    # Key control points defining a luxury modern capital "S"
    # Upper terminal -> Top arc -> Waist -> Bottom arc -> Lower terminal
    points = np.array([
        [0.48,  0.85, 0.0],   # Top-right terminal tip
        [0.55,  0.96, 0.0],   # Top-right smooth turn
        [0.10,  1.10, 0.0],   # Top peak
        [-0.45, 0.98, 0.0],   # Top-left outer curve
        [-0.55, 0.60, 0.0],   # Upper left arc transition
        [-0.45, 0.25, 0.0],   # Inward waist entry upper
        [0.00,  0.00, 0.0],   # Center origin waist inflection
        [0.45, -0.25, 0.0],   # Inward waist entry lower
        [0.55, -0.60, 0.0],   # Lower right arc transition
        [0.45, -0.98, 0.0],   # Bottom-right outer curve
        [-0.10,-1.10, 0.0],   # Bottom peak
        [-0.55,-0.96, 0.0],   # Bottom-left smooth turn
        [-0.48,-0.85, 0.0]    # Bottom-left terminal tip
    ])
    
    # Interpolate using smooth cubic spline
    from scipy.interpolate import CubicSpline
    t_pts = np.linspace(0, 1, len(points))
    cs_x = CubicSpline(t_pts, points[:, 0], bc_type='clamped')
    cs_y = CubicSpline(t_pts, points[:, 1], bc_type='clamped')
    
    t = np.linspace(0, 1, num_samples)
    x = cs_x(t)
    y = cs_y(t)
    z = np.zeros_like(x)
    
    curve = np.column_stack([x, y, z])
    return curve

def create_beveled_profile(width=0.38, height=0.38, corner_radius=0.12, num_corners=16):
    """
    Generates a rounded superellipse / squircle cross section with thick bevels.
    """
    pts = []
    # Half dimensions minus radius
    hw = (width / 2.0) - corner_radius
    hh = (height / 2.0) - corner_radius
    
    # 4 corners
    centers = [
        (hw, hh),    # Top-right
        (-hw, hh),   # Top-left
        (-hw, -hh),  # Bottom-left
        (hw, -hh)    # Bottom-right
    ]
    angles = [
        np.linspace(0, np.pi/2, num_corners),
        np.linspace(np.pi/2, np.pi, num_corners),
        np.linspace(np.pi, 3*np.pi/2, num_corners),
        np.linspace(3*np.pi/2, 2*np.pi, num_corners)
    ]
    
    for (cx, cy), ang_range in zip(centers, angles):
        for a in ang_range[:-1]: # avoid duplicate point at arc joints
            px = cx + corner_radius * np.cos(a)
            py = cy + corner_radius * np.sin(a)
            pts.append([px, py])
            
    return np.array(pts)

def build_hollow_s_mesh():
    """
    Builds a single manifold mesh for a 3D capital "S" with hollow interior & thick optical bevels.
    """
    curve = create_smooth_s_curve(num_samples=240)
    N = len(curve)
    
    # Calculate tangents, normals, binormals along curve
    tangents = np.zeros_like(curve)
    tangents[:-1] = curve[1:] - curve[:-1]
    tangents[-1] = tangents[-2]
    tangents /= np.linalg.norm(tangents, axis=1, keepdims=True)
    
    # Parallel transport frames to prevent twisting
    normals = np.zeros_like(curve)
    binormals = np.zeros_like(curve)
    
    up = np.array([0.0, 0.0, 1.0])
    for i in range(N):
        t_vec = tangents[i]
        b_vec = np.cross(t_vec, up)
        b_norm = np.linalg.norm(b_vec)
        if b_norm < 1e-5:
            b_vec = np.array([1.0, 0.0, 0.0])
        else:
            b_vec /= b_norm
        n_vec = np.cross(b_vec, t_vec)
        n_vec /= np.linalg.norm(n_vec)
        
        binormals[i] = b_vec
        normals[i] = n_vec
        
    # Outer profile & Inner hollow profile
    outer_prof = create_beveled_profile(width=0.42, height=0.42, corner_radius=0.14, num_corners=10)
    inner_prof = create_beveled_profile(width=0.24, height=0.24, corner_radius=0.07, num_corners=10)
    
    M_out = len(outer_prof)
    M_in = len(inner_prof)
    
    vertices = []
    faces = []
    
    # Generate outer tube vertices
    outer_vert_start = len(vertices)
    for i in range(N):
        pos = curve[i]
        n_vec = normals[i]
        b_vec = binormals[i]
        for px, py in outer_prof:
            v = pos + px * b_vec + py * n_vec
            vertices.append(v)
            
    # Generate inner tube vertices (reversed orientation for hollow interior)
    inner_vert_start = len(vertices)
    for i in range(N):
        pos = curve[i]
        n_vec = normals[i]
        b_vec = binormals[i]
        for px, py in inner_prof:
            v = pos + px * b_vec + py * n_vec
            vertices.append(v)
            
    # Triangulate outer tube faces
    for i in range(N - 1):
        r1 = outer_vert_start + i * M_out
        r2 = outer_vert_start + (i + 1) * M_out
        for j in range(M_out):
            j_next = (j + 1) % M_out
            v1 = r1 + j
            v2 = r1 + j_next
            v3 = r2 + j
            v4 = r2 + j_next
            faces.append([v1, v3, v2])
            faces.append([v2, v3, v4])
            
    # Triangulate inner tube faces (facing inward into hollow pocket)
    for i in range(N - 1):
        r1 = inner_vert_start + i * M_in
        r2 = inner_vert_start + (i + 1) * M_in
        for j in range(M_in):
            j_next = (j + 1) % M_in
            v1 = r1 + j
            v2 = r1 + j_next
            v3 = r2 + j
            v4 = r2 + j_next
            # Reverse face winding for inward normal
            faces.append([v1, v2, v3])
            faces.append([v2, v4, v3])
            
    # Seal start cap (t = 0) connecting outer and inner profiles
    start_outer_r = outer_vert_start
    start_inner_r = inner_vert_start
    for j in range(M_out):
        j_next = (j + 1) % M_out
        o1 = start_outer_r + j
        o2 = start_outer_r + j_next
        i1 = start_inner_r + j
        i2 = start_inner_r + j_next
        faces.append([o1, i1, o2])
        faces.append([o2, i1, i2])
        
    # Seal end cap (t = N - 1) connecting outer and inner profiles
    end_outer_r = outer_vert_start + (N - 1) * M_out
    end_inner_r = inner_vert_start + (N - 1) * M_in
    for j in range(M_out):
        j_next = (j + 1) % M_out
        o1 = end_outer_r + j
        o2 = end_outer_r + j_next
        i1 = end_inner_r + j
        i2 = end_inner_r + j_next
        faces.append([o1, o2, i1])
        faces.append([o2, i2, i1])
        
    mesh = trimesh.Trimesh(vertices=np.array(vertices), faces=np.array(faces))
    
    # Center origin (0, 0, 0)
    mesh.vertices -= mesh.center_mass
    
    # Scale to standard height = 2.0 units
    extents = mesh.extents
    scale_factor = 2.0 / extents[1]
    mesh.vertices *= scale_factor
    
    # Smooth surface normals
    mesh.fix_normals()
    
    return mesh

def apply_crystal_pbr_and_export(mesh, output_path):
    """
    Exports the single mesh as a GLB with PBR transmission glass materials & extensions.
    """
    # Export mesh as standard GLB using trimesh first
    glb_data = mesh.export(file_type='glb')
    
    # Parse with pygltflib to inject PBR Transmission, IOR, and Volume extension metadata
    gltf = pygltflib.GLTF2.load_from_bytes(glb_data)
    
    # Ensure extensions & extensionsUsed/Required exist
    gltf.extensionsUsed = [
        "KHR_materials_transmission",
        "KHR_materials_ior",
        "KHR_materials_volume",
        "KHR_materials_specular"
    ]
    
    # Configure PBR material
    if gltf.materials:
        mat = gltf.materials[0]
        mat.name = "OpticalCrystalGlass"
        
        # PBR Base properties
        mat.pbrMetallicRoughness.baseColorFactor = [0.94, 0.97, 1.0, 1.0] # Crystal optical tint
        mat.pbrMetallicRoughness.metallicFactor = 0.0
        mat.pbrMetallicRoughness.roughnessFactor = 0.04 # Glossy polished polish
        mat.doubleSided = True
        mat.alphaMode = "BLEND"
        
        # Injects Transmission & Glass Optical extensions
        mat.extensions = {
            "KHR_materials_transmission": {
                "transmissionFactor": 0.98
            },
            "KHR_materials_ior": {
                "ior": 1.52
            },
            "KHR_materials_volume": {
                "thicknessFactor": 0.5,
                "attenuationColor": [0.92, 0.96, 1.0],
                "attenuationDistance": 2.5
            },
            "KHR_materials_specular": {
                "specularFactor": 1.0,
                "specularColorFactor": [1.0, 1.0, 1.0]
            }
        }
        
    # Save back to GLB file
    gltf.save(output_path)
    print(f"GLB exported successfully to: {output_path}")
    print(f"Triangles: {len(mesh.faces):,}")
    print(f"Vertices: {len(mesh.vertices):,}")

if __name__ == "__main__":
    s_mesh = build_hollow_s_mesh()
    
    # Paths to export
    out_dir = r"c:\Projects\Attempt-1\alche-download\models"
    os.makedirs(out_dir, exist_ok=True)
    
    path1 = os.path.join(out_dir, "crystal_s.glb")
    path2 = r"c:\Projects\Attempt-1\crystal_s.glb"
    
    apply_crystal_pbr_and_export(s_mesh, path1)
    apply_crystal_pbr_and_export(s_mesh, path2)
