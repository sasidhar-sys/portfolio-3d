import cv2
import numpy as np
import math
import os

os.makedirs(r"c:\Projects\Attempt-1\alche-download\top\service", exist_ok=True)

width, height = 1280, 720
fps = 30
duration = 6 # seconds
total_frames = fps * duration

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

def create_uefn_video():
    path = r"c:\Projects\Attempt-1\alche-download\top\service\uefn.mp4"
    out = cv2.VideoWriter(path, fourcc, fps, (width, height))
    
    # 3D Knot / Geometric Optics
    num_particles = 150
    for frame_idx in range(total_frames):
        t = (frame_idx / total_frames) * 2 * math.pi
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Draw background grid
        grid_step = 60
        for x in range(0, width, grid_step):
            cv2.line(frame, (x, 0), (x, height), (15, 20, 30), 1)
        for y in range(0, height, grid_step):
            cv2.line(frame, (0, y), (width, y), (15, 20, 30), 1)
            
        # 3D Torus Knot Points
        pts = []
        for i in range(num_particles):
            u = (i / num_particles) * 2 * math.pi + t
            # Trefoil knot parametric formula
            x3d = (2 + math.cos(3*u)) * math.cos(2*u) * 120
            y3d = (2 + math.cos(3*u)) * math.sin(2*u) * 120
            z3d = math.sin(3*u) * 120
            
            # Rotate around Y & X
            angle_y = t * 0.8
            angle_x = t * 0.5
            
            # Y rot
            x1 = x3d * math.cos(angle_y) + z3d * math.sin(angle_y)
            z1 = -x3d * math.sin(angle_y) + z3d * math.cos(angle_y)
            y1 = y3d
            
            # X rot
            y2 = y1 * math.cos(angle_x) - z1 * math.sin(angle_x)
            z2 = y1 * math.sin(angle_x) + z1 * math.cos(angle_x)
            x2 = x1
            
            # Perspective projection
            fov = 500
            scale = fov / (fov + z2 + 300)
            proj_x = int(width / 2 + x2 * scale)
            proj_y = int(height / 2 + y2 * scale)
            
            radius = max(2, int(8 * scale))
            hue_val = int((i / num_particles * 180 + frame_idx * 2) % 180)
            pts.append((proj_x, proj_y, z2, radius, hue_val))

        # Sort by Z for proper depth buffering
        pts.sort(key=lambda p: p[2], reverse=True)
        
        # Connect adjacent points with glowing lines
        for i in range(len(pts)):
            p1 = pts[i]
            p2 = pts[(i + 1) % len(pts)]
            color_bgr = (255, 180, 50) # Cyan/blue glow
            alpha = max(0.2, min(1.0, (p1[2] + 200) / 400))
            cv2.line(frame, (p1[0], p1[1]), (p2[0], p2[1]), (int(255*alpha), int(200*alpha), int(100*alpha)), 2)
            
        for pt in pts:
            px, py, z, r, h = pt
            # BGR color based on depth
            b = int(255 * (0.5 + 0.5 * math.sin(h*0.05)))
            g = int(180 * (0.5 + 0.5 * math.cos(h*0.05)))
            r_c = int(255 * (0.5 + 0.5 * math.sin(h*0.1)))
            cv2.circle(frame, (px, py), r, (b, g, r_c), -1)
            cv2.circle(frame, (px, py), r + 4, (b//2, g//2, r_c//2), 1)

        out.write(frame)
    out.release()
    print("uefn.mp4 created")

def create_ue_video():
    path = r"c:\Projects\Attempt-1\alche-download\top\service\ue.mp4"
    out = cv2.VideoWriter(path, fourcc, fps, (width, height))
    
    # 3D Landscape Mesh Wave
    cols, rows = 30, 20
    for frame_idx in range(total_frames):
        t = (frame_idx / total_frames) * 2 * math.pi
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        grid_3d = []
        for r in range(rows):
            row_pts = []
            for c in range(cols):
                x = (c - cols/2) * 50
                z = (r - rows/2) * 50
                # Wave equation
                dist = math.sqrt(x*x + z*z) * 0.02
                y = math.sin(dist - t*2) * 40 + math.cos(c*0.4 + t) * 20
                
                # Perspective transform
                cam_y = -150
                cam_z = -400
                
                x_c = x
                y_c = y - cam_y
                z_c = z - cam_z
                
                fov = 450
                scale = fov / (fov + z_c)
                proj_x = int(width/2 + x_c * scale)
                proj_y = int(height/2 + y_c * scale)
                
                row_pts.append((proj_x, proj_y, z_c))
            grid_3d.append(row_pts)
            
        # Draw grid wireframe
        for r in range(rows):
            for c in range(cols):
                p1 = grid_3d[r][c]
                # Draw right link
                if c < cols - 1:
                    p2 = grid_3d[r][c+1]
                    intensity = max(0.2, min(1.0, 1.0 - (p1[2]-300)/500))
                    col = (int(255*intensity), int(140*intensity), int(40*intensity)) # Deep blue/magenta
                    cv2.line(frame, (p1[0], p1[1]), (p2[0], p2[1]), col, 1)
                # Draw down link
                if r < rows - 1:
                    p3 = grid_3d[r+1][c]
                    intensity = max(0.2, min(1.0, 1.0 - (p1[2]-300)/500))
                    col = (int(200*intensity), int(80*intensity), int(255*intensity))
                    cv2.line(frame, (p1[0], p1[1]), (p3[0], p3[1]), col, 1)
                    
                # Glowing nodes
                if (r + c + frame_idx//5) % 4 == 0:
                    cv2.circle(frame, (p1[0], p1[1]), 3, (255, 220, 100), -1)

        out.write(frame)
    out.release()
    print("ue.mp4 created")

def create_stellla_video():
    path = r"c:\Projects\Attempt-1\alche-download\top\service\stellla.mp4"
    out = cv2.VideoWriter(path, fourcc, fps, (width, height))
    
    # Orbiting sphere & particles
    np.random.seed(42)
    particle_data = []
    for _ in range(200):
        rad = np.random.uniform(150, 350)
        theta = np.random.uniform(0, 2*math.pi)
        phi = np.random.uniform(-math.pi/2, math.pi/2)
        speed = np.random.uniform(0.5, 1.5)
        p_size = np.random.uniform(2, 6)
        particle_data.append([rad, theta, phi, speed, p_size])

    for frame_idx in range(total_frames):
        t = (frame_idx / total_frames) * 2 * math.pi
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Central glowing sphere
        cx, cy = width // 2, height // 2
        for r in range(120, 0, -5):
            alpha = (120 - r) / 120.0
            color = (int(255 * alpha * 0.8), int(100 * alpha), int(220 * alpha))
            cv2.circle(frame, (cx, cy), r, color, -1)
            
        # Concentric glowing rings
        for ring_idx in range(3):
            rx = int(180 + 40 * ring_idx + 10 * math.sin(t*2 + ring_idx))
            ry = int(60 + 15 * ring_idx)
            cv2.ellipse(frame, (cx, cy), (rx, ry), int(t*30 + ring_idx*45), 0, 360, (200, 255, 150), 2)
            
        # Particles
        for p in particle_data:
            rad, theta, phi, speed, p_size = p
            curr_theta = theta + t * speed
            
            x = rad * math.cos(curr_theta) * math.cos(phi)
            y = rad * math.sin(phi)
            z = rad * math.sin(curr_theta) * math.cos(phi)
            
            # Perspective
            scale = 400 / (400 + z)
            px = int(cx + x * scale)
            py = int(cy + y * scale)
            
            sz = max(1, int(p_size * scale))
            brightness = max(0.3, min(1.0, scale))
            p_col = (int(255 * brightness), int(200 * brightness), int(255 * brightness))
            cv2.circle(frame, (px, py), sz, p_col, -1)
            
        out.write(frame)
    out.release()
    print("stellla.mp4 created")

create_uefn_video()
create_ue_video()
create_stellla_video()
