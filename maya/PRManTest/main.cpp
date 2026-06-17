#include <maya/MFnPlugin.h>
#include <maya/MGlobal.h>
#include "PRManTestCmd.h"

MStatus initializePlugin(MObject obj)
{
    MFnPlugin plugin(obj, "AlembicPRMan", "1.0", "Any");
    MStatus status = plugin.registerCommand("prmanTest", PRManTestCmd::creator);
    if (!status) {
        status.perror("registerCommand");
        return status;
    }

    MGlobal::displayInfo("prmanTest plugin loaded.");
    return status;
}

MStatus uninitializePlugin(MObject obj)
{
    MFnPlugin plugin(obj);
    MStatus status = plugin.deregisterCommand("prmanTest");
    if (!status) {
        status.perror("deregisterCommand");
    }
    return status;
}
