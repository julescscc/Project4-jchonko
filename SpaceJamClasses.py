from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task
from CollideObjectBase import *
from typing import Callable

class Planet(SphereCollideObject):

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Planet, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 1.1)
        #self.modelNode = loader.loadModel(modelPath)
        #self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Drone(SphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Drone, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 4)
        #self.modelNode = loader.loadModel(modelPath)
        #self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

    droneCount = 0

class Universe(InverseSphereCollideObject):

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Universe, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 0.9)
        #self.modelNode = loader.loadModel(modelPath)
        #self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class SpaceStation(CapsuleCollidableObject):

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(SpaceStation, self).__init__(loader, modelPath, parentNode, nodeName, 1, -1, 5, 1, -1, -5, 10)
        #self.modelNode = loader.loadModel(modelPath)
        #self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Player(SphereCollideObject):

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float, manager: Task, accept: Callable[[str, Callable], None]):
        super(Player, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 60)
        #self.modelNode = loader.loadModel(modelPath)
        #self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.taskManager = manager
        self.render = parentNode

        self.accept = accept

        self.SetKeyBindings()
    
    def Thrust(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyThrust, 'forward-thrust')
        else:
            self.taskManager.remove('forward-thrust')
    
    def ApplyThrust(self, task):
        rate = 5
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.forward())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont

    def LeftTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyLeftTurn, 'left-turn')
        else:
            self.taskManager.remove('left-turn')

    def ApplyLeftTurn(self, task):
        rate = 0.5
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont

    def RightTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyRightTurn, 'right-turn')
        else:
            self.taskManager.remove('right-turn')

    def ApplyRightTurn(self, task):
        rate = -0.5
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont
    
    def UpTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyUpTurn, 'up-turn')
        else:
            self.taskManager.remove('up-turn')

    def ApplyUpTurn(self, task):
        rate = 0.5
        self.modelNode.setP(self.modelNode.getP() + rate)
        return Task.cont
    
    def DownTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyDownTurn, 'down-turn')
        else:
            self.taskManager.remove('down-turn')

    def ApplyDownTurn(self, task):
        rate = -0.5
        self.modelNode.setP(self.modelNode.getP() + rate)
        return Task.cont
    
    def LeftRoll(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyLeftRoll, 'left-roll')
        else:
            self.taskManager.remove('left-roll')

    def ApplyLeftRoll(self, task):
        rate = -0.5
        self.modelNode.setR(self.modelNode.getR() + rate)
        return Task.cont
    
    def RightRoll(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyRightRoll, 'right-roll')
        else:
            self.taskManager.remove('right-roll')

    def ApplyRightRoll(self, task):
        rate = 0.5
        self.modelNode.setR(self.modelNode.getR() + rate)
        return Task.cont
    
    def SetKeyBindings(self):
        self.accept('space', self.Thrust, [1])
        self.accept('space-up', self.Thrust, [0])
        self.accept('a', self.LeftTurn, [1])
        self.accept('a-up', self.LeftTurn, [0])
        self.accept('d', self.RightTurn, [1])
        self.accept('d-up', self.RightTurn, [0])
        self.accept('w', self.UpTurn, [1])
        self.accept('w-up', self.UpTurn, [0])
        self.accept('s', self.DownTurn, [1])
        self.accept('s-up', self.DownTurn, [0])
        self.accept('q', self.LeftRoll, [1])
        self.accept('q-up', self.LeftRoll, [0])
        self.accept('e', self.RightRoll, [1])
        self.accept('e-up', self.RightRoll, [0])