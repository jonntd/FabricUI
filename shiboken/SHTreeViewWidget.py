from PySide import QtCore, QtGui
from FabricEngine import Core, FabricUI
from FabricEngine.FabricUI import *
from SHTreeView import SHTreeView

class SHTreeComboBox(QtGui.QComboBox):
  updateList = QtCore.Signal()

  def __init__(self): 
    super(SHTreeComboBox, self).__init__()

  def showPopup(self):
    self.updateList.emit()
    super(SHTreeComboBox, self).showPopup()
 

class SHTreeViewWidget(QtGui.QWidget):
  sceneHierarchyChanged = QtCore.Signal()
  sceneUpdated = QtCore.Signal(SceneHub.SHGLScene)
  
  def __init__(self, parent, klFile):
    self.parentApp = parent

    super(SHTreeViewWidget, self).__init__()
    self.shMainGLScene = SceneHub.SHGLScene(self.parentApp.client, klFile)
    self.shGLScene = SceneHub.SHGLScene(self.parentApp.client)

    self.treeModel = None
    self.bUpdatingSelectionFrom3D = False

    self.comboBox = SHTreeComboBox()
    self.shTreeView = SHTreeView(self.parentApp.client, self.shGLScene)
    
    layout = QtGui.QVBoxLayout()
    layout.addWidget(self.comboBox)
    layout.addWidget(self.shTreeView)
    self.setLayout(layout)
    self.comboBox.addItem("Main Scene")

    self.shTreeView.itemSelected.connect(self.onTreeItemSelected)
    self.shTreeView.itemDeselected.connect(self.onTreeItemDeselected)
    self.comboBox.updateList.connect(self.onUpdateSceneList)
    self.comboBox.currentIndexChanged.connect(self.onUpdateScene)
 
    self.onUpdateScene()
 
  def getScene(self):
    return self.shGLScene

  def __resetTree(self):
    self.shTreeView.reset()
    if self.treeModel is not None: self.treeModel = None
 
  def __constructTree(self):
    self.__resetTree()
    self.treeModel = SceneHub.SHTreeModel(self.shGLScene, self.shTreeView)
    self.sceneHierarchyChanged.connect(self.treeModel.onSceneHierarchyChanged)
    self.treeModel.sceneHierarchyChanged.connect(self.onSceneHierarchyChanged)
    sceneRootIndex = self.treeModel.addRootItemsFromScene(self.shGLScene)
    self.shTreeView.setModel(self.treeModel)
    self.shTreeView.setExpanded(sceneRootIndex, True)

  def onUpdateScene(self):
    sceneName = self.comboBox.currentText()
    if str(sceneName) == "Main Scene":
      self.shGLScene.setSHGLScene(self.shMainGLScene)
      self.__constructTree()
      self.sceneUpdated.emit(self.shGLScene)
    
    elif self.parentApp.dfgWidget.getDFGController().getBinding().getExec().hasVar(str(sceneName)):
      self.shGLScene.setSHGLScene(self.parentApp.dfgWidget.getDFGController().getBinding(), sceneName)
      self.__constructTree()
      self.sceneUpdated.emit(self.shGLScene)
    
    else:
      self.comboBox.clear()
      self.__resetTree()
    
  def onUpdateSceneList(self):
    self.comboBox.clear()
    
    binding = self.parentApp.dfgWidget.getDFGController().getBinding()
    sceneNameList = self.shGLScene.getSceneNamesFromBinding(binding)
      
    if len(sceneNameList) == 0 and not self.shGLScene.hasSG():
      self.__resetTree()

    if self.shMainGLScene.hasSG(): 
      self.comboBox.addItem("Main Scene")

    for sceneName in sceneNameList:
     self.comboBox.addItem(sceneName)
    
  def expandTree(self, level):
    if(level == -1): self.shTreeView.expandAll()
    elif(level>0): self.shTreeView.expandToDepth(level-1)

  def onSceneHierarchyChanged(self):
    #Check if it actually changed, to reduce number of notifications
    if self.shGLScene.hasSG() and self.shGLScene.sceneHierarchyChanged():
      self.sceneHierarchyChanged.emit()

  def onTreeItemSelected(self, item):
    if self.shGLScene.hasSG() and not self.bUpdatingSelectionFrom3D:
      self.shGLScene.treeItemSelected(item)
      self.sceneHierarchyChanged.emit()
     
  def onTreeItemDeselected(self, item):
    if self.shGLScene.hasSG() and not self.bUpdatingSelectionFrom3D:
      self.shGLScene.treeItemDeselected(item) 
      self.sceneHierarchyChanged.emit()

  def onUpdateFrom3DSelection(self):
    if self.shGLScene.hasSG():
      #Ensure there's not a loopback from TreeView selection change to 3D view
      self.bUpdatingSelectionFrom3D = True
      #Ensure it really changed we will be called for any accepted event only a few will be selection changes
      if self.shGLScene.selectionChangedFromManips():
        self.shTreeView.setSelectedObjects(self.shGLScene)
        self.sceneHierarchyChanged.emit()
      self.bUpdatingSelectionFrom3D = False
  