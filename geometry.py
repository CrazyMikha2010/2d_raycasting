from math import hypot, sqrt, sin, cos, acos, asin, radians, atan2, degrees

EPS = 1e-8
class Vector:
    def __init__(self, x:float=None, y:float=None, inp:bool=False) -> None:
        if inp:
            x, y = map(float, input().split())
        self.x, self.y = x, y

    def __xor__(self, other: 'Vector') -> int:
        other_x, other_y = other.x, other.y
        return self.x * other_y - self.y * other_x
    
    cross_product = __xor__
    
    def __mul__(self, other: 'Vector') -> int:
        return self.x * other.x + self.y * other.y
        
    dot_product = __mul__

    def __rmul__(self, n: 'Vector | int') -> int:
        return self * n
    
    def __abs__(self) -> int:
        return hypot(self.x, self.y)

    def __str__(self) -> str:
        return f'{self.x:.6f} {self.y:.6f}'


class Segment:
    def __init__(self, inp:bool) -> None:
        if inp:
            self.point1 = Vector(inp=True)
            self.point2 = Vector(inp=True)


class Ray:
    def __init__(self, x:int=0, y:int=0, deg:float=0) -> None:
        self.start_point = Vector(x, y)
        rad = radians(deg)
        dir_x = self.start_point.x + cos(rad)
        dir_y = self.start_point.y + sin(rad)
        self.dir_point = Vector(dir_x, dir_y)

def point_in_ray(point_x:int, point_y:int, ray_start_x: int, ray_start_y:int, ray_dir_x:int, ray_dir_y:int) -> bool:
                vector_from_point = Vector(point_x - ray_start_x, point_y - ray_start_y)
                vector = Vector(ray_dir_x - ray_start_x, ray_dir_y - ray_start_y)

                return abs(vector_from_point ^ vector) <= EPS and vector_from_point * vector >= -EPS

def point_in_segment(point_x:int, point_y:int, seg_point1_x:int, seg_point1_y:int, seg_point2_x:int, seg_point2_y:int) -> bool:
        vector1 = Vector(seg_point2_x - seg_point1_x, seg_point2_y - seg_point1_y)
        vector2 = Vector(seg_point1_x - seg_point2_x, seg_point1_y - seg_point2_y)
        vector_from_point1 = Vector(point_x - seg_point1_x, point_y - seg_point1_y)
        vector_from_point2 = Vector(point_x - seg_point2_x, point_y - seg_point2_y)

        if vector1 * vector_from_point1 < EPS or vector2 * vector_from_point2 < EPS:
            dist = min(abs(vector_from_point1), abs(vector_from_point2))
        else:
            cross = abs(vector1 ^ vector_from_point1)
            dist = cross / abs(vector1)
        if dist < EPS:
            return True
        return False

def crossRS(r: Ray, S:Segment) -> Vector | None:
    # получаем уравнения прямых, на которых лежит луч и отрезок (задача L)
    line1_A = r.dir_point.y - r.start_point.y
    line1_B = r.start_point.x - r.dir_point.x
    line1_C = r.dir_point.x * r.start_point.y - r.start_point.x * r.dir_point.y

    line2_A = S.point2.y - S.point1.y
    line2_B = S.point1.x - S.point2.x
    line2_C = S.point2.x * S.point1.y - S.point1.x * S.point2.y

    # находим точку пересечения этих прямых (задача Q)
    if abs(line1_A * line2_B - line2_A * line1_B) < EPS: # прямые параллельны
        if abs(line1_A * line2_C - line2_A * line1_C) < EPS and abs(line1_C * line2_B - line2_C * line1_B) < EPS: # совпадают
            # проверяем принадлежность точек отрезка к лучу (задача G)
            point1_in_ray = point_in_ray(S.point1.x, S.point1.y, r.start_point.x, r.start_point.y, r.dir_point.x, r.dir_point.y)
            point2_in_ray = point_in_ray(S.point2.x, S.point2.y, r.start_point.x, r.start_point.y, r.dir_point.x, r.dir_point.y)
            if not (point1_in_ray or point2_in_ray): # нет общих точек
                return None
            elif point1_in_ray and point2_in_ray: # отрезок полностью на луче => надо найти ближайшую к началу луча точку
                if hypot(r.start_point.x - S.point1.x, r.start_point.y - S.point1.y) < hypot(r.start_point.x - S.point2.x, r.start_point.y - S.point2.y):
                    return Vector(S.point1.x, S.point1.y)
                return Vector(S.point2.x, S.point2.y)
            return Vector(r.start_point.x, r.start_point.y) # только одна точка на луче
            
        # нет точек пересечения
        return None
    
    x = (line1_C * line2_B - line2_C * line1_B) / (line2_A * line1_B - line1_A * line2_B)
    if line1_B == 0:
        y = -(line2_A * x + line2_C) / line2_B
    else:
        y = -(line1_A * x + line1_C) / line1_B

    # проверяем если точка принадлежит к отрезку (задача K)
    if point_in_segment(x, y, S.point1.x, S.point1.y, S.point2.x, S.point2.y) and point_in_ray(x, y, r.start_point.x, r.start_point.y, r.dir_point.x, r.dir_point.y):
        return Vector(x, y)
    return None

n = int(input())
segments = []
for _ in range(n):
    segments.append(Segment(inp=True))

def get_angle(ray_x:int, ray_y:int, x:int, y:int) -> float:
    return degrees(atan2(y - ray_y, x - ray_x)) % 360

def get_crosses(ray_x:int, ray_y:int, light_angle:int=0, width:int=60):
    angles = set()
    left = (light_angle - width + 360) % 360
    right = (light_angle + width + 360) % 360
    angles.add(left)
    angles.add(right)
    for segment in segments:
        for point in [segment.point1, segment.point2]:
            angle = get_angle(ray_x, ray_y, point.x, point.y)
            for i in [-0.1, 0, 0.1]:
                a = (angle + i) % 360
                if left < right:
                    if not (left <= a <= right):
                        continue
                else:
                    if not (a >= left or a <= right):
                        continue
                angles.add(a)

    angles = sorted(list(angles))
    ang1, ang2 = [], []
    for ang in angles:
        if left < right:
            if left <= ang <= light_angle:
                ang1.append(ang)
            else:
                ang2.append(ang)
        else:
            diff = (ang - left) % 360
            if diff <= width:
                ang1.append(ang)
            else:
                ang2.append(ang)
    angles = ang1 + ang2

    ans = []
    for angle in angles:
        ray = Ray(ray_x, ray_y, angle)
        mindist = float('inf')
        curans = None
        for segment in segments:
            cross = crossRS(ray, segment)
            if cross:
                if mindist > hypot(ray_x - cross.x, ray_y - cross.y):
                    mindist = hypot(ray_x - cross.x, ray_y - cross.y)
                    curans = cross
        ans.append(curans)
    return ans



