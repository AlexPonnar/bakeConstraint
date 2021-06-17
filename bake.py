
from maya import cmds
import operator
from pprint import pprint

conType = ['parentConstraint', 'pointConstraint', 'orientConstraint']

def QueryConstraints():
    listCont = []
    for each_con in conType:
        listCont.append(cmds.ls(type=each_con))

    conDict = {}
    for each in reduce(operator.add, listCont):
        type = cmds.nodeType(each)
        data = {}
        child = cmds.listRelatives(each, parent=True)
        if type == 'parentConstraint':
            driverParent = cmds.parentConstraint(each, query=True, targetList=True)

        elif type == 'pointConstraint':
            driverParent = cmds.pointConstraint(each, query=True, targetList=True)

        elif type == 'orientConstraint':
            dirverParent = cmds.oreientConstraint(each, query=True, targetList=True)

        data.update({'driver': driverParent})
        data.update({'child': child})
        conDict.update({each: data})
    return conDict


def smartBake(start_frame, end_frame, controllers):
    bake_status = cmds.bakeResults(controllers,
                                   t=(start_frame, end_frame),
                                   simulation=True,
                                   sampleBy=1,
                                   oversamplingRate=1,
                                   disableImplicitControl=True,
                                   preserveOutsideKeys=True,
                                   sparseAnimCurveBake=True,
                                   removeBakedAttributeFromLayer=False,
                                   removeBakedAnimFromLayer=True,
                                   bakeOnOverrideLayer=False,
                                   minimizeRotation=True,
                                   controlPoints=True,
                                   shape=True)

    delConstraint = []
    for each in conType:
        constraint = cmds.listConnections(controllers, type=each)
        if constraint:
            delConstraint.append(set(constraint))
    if delConstraint:
        for each in delConstraint:
            cmds.delete(each)













