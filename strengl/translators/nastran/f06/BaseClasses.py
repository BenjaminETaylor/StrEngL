"""
===============================================================================
    StrEngL.Nastran.Results.BaseClasses
    Copyright (C) 2015  Benjamin E. Taylor

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
===============================================================================
"""

#import numpy as np

class Result():
    # Common attributes:
    #   self.subcase = subcase
    #   self.ID = ID
    #   self.source = source
    def getType(self):
        return type(self)
    
class Linear(Result):
    # Interface requirements:
    #   self.forces = np.array([Px, Py, Pz])
    #   self.moments = np.array([Mx, My, Mz])      
    def rotate(self,dirCosines):
        raise NotImplementedError
        
class Element(Linear):
    # Interface requirements:
    #   self.stresses = np.array([[s11, s12, s13],
    #                             [s21, s22, s23],
    #                             [s31, s32, s33]])
    #   self.strains = np.array([[e11, e12, e13],
    #                            [e21, e22, e23],
    #                            [e31, e32, e33]])
    def rotateStress(self,dirCosines):
        # Tensor rotation
        raise NotImplementedError
    def rotateStrain(self,dirCosines):
        # Tensor rotation
        raise NotImplementedError
    
class Node(Linear):
    def __init__(self, ID, translations, rotations):
        # self.translations = np.array([dx, dy, dz])
        self.translations = translations
        # self.rotations = np.array([rx, ry, rz])
        self.rotations = rotations
    def __add__(self, other):
        translations =  self.translations + other.translations
        rotations = self.rotations + other.rotations
        return Node(None, translations, rotations)
    def __sub__(self, other):
        translations = self.translations - other.translations
        rotations = self.rotations - other.rotations
        return Node(None, translations, rotations)
    def __mul__(self, scalar):
        translations = self.translations * scalar
        rotations = self.rotations * scalar
        return Node(None, translations, rotations)
    def __imul__(self, scalar):
        self.translations = self.translations * scalar
        self.rotations = self.rotations * scalar
        return self
    def __truediv__(self, scalar):
        translations = self.translations / float(scalar)
        rotations = self.rotations / float(scalar)
        return Node(translations, rotations)
    def __itruediv__(self, scalar):
        self.translations = self.translations / float(scalar)
        self.rotations = self.rotations / float(scalar)
        return self
    def interpolate(self):
        raise NotImplementedError
    def extrapolate(self):
        raise NotImplementedError
    def fitData(self):
        raise NotImplementedError
        
class Element0D(Linear):
    def __init__(self, ID, forces, moments):
        self.ID = ID
        # self.forces = np.array([Px, Py, Pz])  
        self.forces = forces
        # self.moments = np.array([Mx, My, Mz])
        self.moments = moments
        # individual components
        self.setComponents()
    def __add__(self, other):
        forces =  self.forces + other.forces
        moments = self.moments + other.moments
        return Element0D(None, forces, moments)
    def __sub__(self, other):
        forces = self.forces - other.forces
        moments = self.moments - other.moments
        return Element0D(None, forces, moments)
    def __mul__(self, scalar):
        forces = self.forces * scalar
        moments = self.moments * scalar
        return Element0D(None, forces, moments)
    def __imul__(self, scalar):
        self.forces = self.forces * scalar
        self.moments = self.moments * scalar
        self.setComponents()
        return self
    def __truediv__(self, scalar):
        forces = self.forces / float(scalar)
        moments = self.moments / float(scalar)
        return Element0D(None, forces, moments)
    def __itruediv__(self, scalar):
        self.forces = self.forces / float(scalar)
        self.moments = self.moments / float(scalar)
        self.setComponents()
        return self
    def setComponents(self):
        self.Px = self.forces[0]
        self.Py = self.forces[1]
        self.Pz = self.forces[2]
        self.Mx = self.moments[0]
        self.My = self.moments[1]
        self.Mz = self.moments[2]
    def flipSigns(self):
        self.forces = self.forces * -1.
        self.moments = self.moments * -1.
        self.setComponents()
        
class Element1D(Element):
    def __init__(self, ID, forces, momentsA, momentsB):
        self.ID = ID
        # self.forces = np.array([Px, Vy, Vz])        
        self.forces = forces
        # self.momentsA = np.array([T, Mya, Mza])
        self.momentsA = momentsA
        # self.momentsB = np.array([T, Myb, Mzb])
        self.momentsB = momentsB
        # individual components
        self.setComponents()
    def __add__(self, other):
        forces =  self.forces + other.forces
        momentsA = self.momentsA + other.momentsA
        momentsB = self.momentsB + other.momentsB
        return Element1D(None, forces, momentsA, momentsB)
    def __sub__(self, other):
        forces = self.forces - other.forces
        momentsA = self.momentsA - other.momentsA
        momentsB = self.momentsB - other.momentsB
        return Element1D(None, forces, momentsA, momentsB)
    def __mul__(self, scalar):
        forces = self.forces * scalar
        momentsA = self.momentsA * scalar
        momentsB = self.momentsB * scalar
        return Element1D(None, forces, momentsA, momentsB)
    def __imul__(self, scalar):
        self.forces = self.forces * scalar
        self.momentsA = self.momentsA * scalar
        self.momentsB = self.momentsB * scalar
        self.setComponents()
        return self
    def __truediv__(self, scalar):
        forces = self.forces / float(scalar)
        momentsA = self.momentsA / float(scalar)
        momentsB = self.momentsB / float(scalar)
        return Element1D(None, forces, momentsA, momentsB)
    def __itruediv__(self, scalar):
        self.forces = self.forces / float(scalar)
        self.momentsA = self.momentsA / float(scalar)
        self.momentsB = self.momentsB / float(scalar)
        self.setComponents()
        return self
    def setComponents(self):
        self.Px = self.forces[0]
        self.Vy = self.forces[1]
        self.Vz = self.forces[2]
        self.T = self.momentsA[0]
        self.Mya = self.momentsA[1]
        self.Mza = self.momentsA[2]
        self.Myb = self.momentsB[1]
        self.Mzb = self.momentsB[2]        
    def maxMoment(self):
        # compare 3D moment vector on each side
        # return highest side
        raise NotImplementedError
    
class Element2D(Element):
    def __init__(self, ID, forces, moments, shears):
        self.ID = ID        
        # self.forces = np.array([Nx, Ny, Nxy])
        self.forces = forces
        # self.moments = np.array([Mx, My, Mxy])
        self.moments = moments
        # self.shears = np.array([Qx, Qy])
        self.shears = shears
        # individual components
        self.setComponents()
    def __add__(self, other):
        forces =  self.forces + other.forces
        moments = self.moments + other.moments
        shears = self.shears + other.shears
        return Element2D(None, forces, moments, shears)
    def __sub__(self, other):
        forces = self.forces - other.forces
        moments = self.moments - other.moments
        shears = self.shears - other.shears
        return Element2D(None, forces, moments, shears)
    def __mul__(self, scalar):
        forces = self.forces * scalar
        moments = self.moments * scalar
        shears = self.shears * scalar
        return Element2D(None, forces, moments, shears)
    def __imul__(self, scalar):
        self.forces = self.forces * scalar
        self.moments = self.moments * scalar
        self.shears = self.shears * scalar
        self.setComponents()
        return self
    def __truediv__(self, scalar):
        forces = self.forces / float(scalar)
        moments = self.moments / float(scalar)
        shears = self.shears / float(scalar)
        return Element2D(None, forces, moments, shears)
    def __itruediv__(self, scalar):
        self.forces = self.forces / float(scalar)
        self.moments = self.moments / float(scalar)
        self.shears = self.shears / float(scalar)
        self.setComponents()
        return self
    def setComponents(self):
        self.Nx = self.forces[0]
        self.Ny = self.forces[1]
        self.Nxy = self.forces[2]
        self.Mx = self.moments[0]
        self.My = self.moments[1]
        self.Mxy = self.moments[2]
        self.Qx = self.shears[0]
        self.Qy = self.shears[1]       
    def rotate(self, angle):
        # In-plane rotation
        raise NotImplementedError
    def shrinkThickness(self, t_old, t_new):
        raise NotImplementedError
    def growThickness(self, t_old, t_new):
        raise NotImplementedError
    def minThickness(self, t_old, MS):
        raise NotImplementedError
    def getUpperStress(self):
        raise NotImplementedError
    def getLowerStress(self):
        raise NotImplementedError
    
