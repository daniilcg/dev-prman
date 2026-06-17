#include "PRManTestCmd.h"
#include <maya/MGlobal.h>
#include <maya/MFnPlugin.h>

#ifdef _WIN32
#define PATH_SEPARATOR ";"
#else
#define PATH_SEPARATOR ":"
#endif

// RenderMan headers are optional and only required if the plugin is built with PRMAN support.
#ifdef USE_PRMAN
#include <ri.h>
#endif

PRManTestCmd::PRManTestCmd() {}
PRManTestCmd::~PRManTestCmd() {}

void* PRManTestCmd::creator()
{
    return new PRManTestCmd();
}

MStatus PRManTestCmd::doIt(const MArgList& args)
{
    MGlobal::displayInfo("PRManTest command running.");

#ifdef USE_PRMAN
    if (RiIsActive()) {
        MGlobal::displayInfo("RenderMan is already active.");
    } else {
        RiBegin("mayaPRManTest");
        RiOption("render", "searchpath:shader", "shader" PATH_SEPARATOR "./shaders");
        RiDisplay("output.exr", "rgba", "string", RI_NULL);
        RiEnd();
        MGlobal::displayInfo("RenderMan initialization completed.");
    }
#else
    MGlobal::displayWarning("PRMan support is not enabled in this build.");
#endif

    return MS::kSuccess;
}
