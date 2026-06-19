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

    // Parse command arguments
    bool verbose = false;
    if (args.length() > 0) {
        MString arg = args.asString(0);
        if (arg == "-verbose" || arg == "-v") {
            verbose = true;
        }
    }

#ifdef USE_PRMAN
    if (RiIsActive()) {
        MGlobal::displayInfo("RenderMan is already active.");
        return MS::kSuccess;
    }

    if (verbose) {
        MGlobal::displayInfo("Initializing RenderMan context...");
    }

    // Build shader search path
    const char* shader_base = "shader";
    const char* shader_path_suffix = "./shaders";
    const size_t total_len = strlen(shader_base) + strlen(PATH_SEPARATOR) + strlen(shader_path_suffix) + 1;
    char* shader_path = new char[total_len];
    sprintf(shader_path, "%s%s%s", shader_base, PATH_SEPARATOR, shader_path_suffix);

    RiBegin("mayaPRManTest");
    RiOption("render", "searchpath:shader", shader_path);
    RiDisplay("output.exr", "rgba", "string", RI_NULL);
    RiEnd();

    delete[] shader_path;

    MGlobal::displayInfo("RenderMan initialization completed.");
#else
    MGlobal::displayWarning("PRMan support is not enabled in this build.");
#endif

    return MS::kSuccess;
}
