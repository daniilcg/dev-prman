#ifndef PRMAN_TEST_CMD_H
#define PRMAN_TEST_CMD_H

#include <maya/MPxCommand.h>
#include <maya/MStatus.h>
#include <maya/MArgList.h>

class PRManTestCmd : public MPxCommand
{
public:
    PRManTestCmd();
    virtual ~PRManTestCmd();

    static void* creator();
    virtual MStatus doIt(const MArgList& args);
};

#endif // PRMAN_TEST_CMD_H
