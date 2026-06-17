import os

try:
    import maya
    import maya.cmds as MayaCmds
    import maya.OpenMaya as OpenMaya
    import maya.standalone
except ImportError:
    MayaCmds = None
    OpenMaya = None
    maya = None

try:
    import prman
    from prman import rmanGettr as prman_rmanGettr
except ImportError:
    prman = None
    prman_rmanGettr = None


def ensure_maya_available():
    if MayaCmds is None:
        raise RuntimeError("Maya Python API is not available in this environment.")


def createCamera():
    ensure_maya_available()
    name = MayaCmds.camera()
    MayaCmds.setAttr(name[1] + '.horizontalFilmAperture', 0.962)
    MayaCmds.setAttr(name[1] + '.verticalFilmAperture', 0.731)
    MayaCmds.setAttr(name[1] + '.focalLength', 50)
    MayaCmds.setAttr(name[1] + '.focusDistance', 3)
    MayaCmds.setAttr(name[1] + '.shutterAngle', 100)
    return name


def createMesh():
    ensure_maya_available()
    return MayaCmds.polyCube()


def createLight():
    ensure_maya_available()
    return MayaCmds.directionalLight()


def createLocator():
    ensure_maya_available()
    return MayaCmds.spaceLocator()


def createNurbsCurve():
    ensure_maya_available()
    return MayaCmds.curve(d=1, p=[(-1, 0, 0), (0, 0, 1), (1, 0, 0)])


def createNurbsSurface():
    ensure_maya_available()
    return MayaCmds.nurbsPlane(d=3, p=(0, 0, 0), ax=(0, 1, 0), w=1, lr=1, n='nurbsPlane1')


def createSubdiv():
    ensure_maya_available()
    name = MayaCmds.polyCube()
    MayaCmds.setAttr(name[0] + '.subdivisionsWidth', 2)
    MayaCmds.setAttr(name[0] + '.subdivisionsHeight', 2)
    return name


def createParticle():
    ensure_maya_available()
    return MayaCmds.particle()


def createHair():
    ensure_maya_available()
    name = MayaCmds.polyCube()
    MayaCmds.select(name[0])
    MayaCmds.CreateHair()
    return name


def createFluid():
    ensure_maya_available()
    return MayaCmds.fluidEmitter()


def createRigidBody():
    ensure_maya_available()
    name = MayaCmds.polyCube()
    MayaCmds.rigidBody(name[0], active=True)
    return name


def createSoftBody():
    ensure_maya_available()
    name = MayaCmds.polyCube()
    MayaCmds.soft(name[0])
    return name


def createConstraint():
    ensure_maya_available()
    name = MayaCmds.polyCube()
    MayaCmds.pointConstraint(name[0], name[0])
    return name


def createDeformer():
    ensure_maya_available()
    name = MayaCmds.polyCube()
    MayaCmds.nonLinear(name[0], type='bend')
    return name


def createExpression():
    ensure_maya_available()
    name = MayaCmds.polyCube()
    MayaCmds.expression(s=name[0] + '.translateX = time * 1')
    return name


def createShader():
    ensure_maya_available()
    return MayaCmds.shadingNode('lambert', asShader=True)


def createTexture():
    ensure_maya_available()
    return MayaCmds.shadingNode('file', asTexture=True)


def createMaterial():
    ensure_maya_available()
    material = MayaCmds.shadingNode('lambert', asShader=True)
    shading_group = MayaCmds.sets(renderable=True, noSurfaceShader=True, empty=True)
    MayaCmds.connectAttr(material + '.outColor', shading_group + '.surfaceShader')
    return material


def createRenderLayer():
    ensure_maya_available()
    return MayaCmds.createRenderLayer()


def createRenderPass():
    ensure_maya_available()
    return MayaCmds.createRenderPass()


def createRenderSettings():
    ensure_maya_available()
    return MayaCmds.shadingNode('renderSettings', asUtility=True)


def createRenderGlobals():
    ensure_maya_available()
    return MayaCmds.shadingNode('renderGlobals', asUtility=True)


def createRenderView():
    ensure_maya_available()
    return MayaCmds.shadingNode('renderView', asUtility=True)


def createRenderLayerManager():
    ensure_maya_available()
    return MayaCmds.shadingNode('renderLayerManager', asUtility=True)


def createRenderPassManager():
    ensure_maya_available()
    return MayaCmds.shadingNode('renderPassManager', asUtility=True)


def createRenderSettingsManager():
    ensure_maya_available()
    return MayaCmds.shadingNode('renderSettingsManager', asUtility=True)


def createRenderGlobalsManager():
    ensure_maya_available()
    return MayaCmds.shadingNode('renderGlobalsManager', asUtility=True)


def createRenderViewManager():
    ensure_maya_available()
    return MayaCmds.shadingNode('renderViewManager', asUtility=True)


def configure_render_globals():
    ensure_maya_available()
    MayaCmds.setAttr('defaultRenderGlobals.imageFormat', 8)
    MayaCmds.setAttr('defaultRenderGlobals.animation', 1)
    MayaCmds.setAttr('defaultRenderGlobals.startFrame', 1)
    MayaCmds.setAttr('defaultRenderGlobals.endFrame', 10)
    MayaCmds.setAttr('defaultRenderGlobals.byFrameStep', 1)
    MayaCmds.setAttr('defaultRenderGlobals.outFormatControl', 0)
    MayaCmds.setAttr('defaultRenderGlobals.putFrameBeforeExt', 1)
    MayaCmds.setAttr('defaultRenderGlobals.extensionPadding', 4)
    MayaCmds.setAttr('defaultRenderGlobals.periodInExt', 1)


def list_all_nodes():
    ensure_maya_available()
    return MayaCmds.ls(dag=True, long=True)


def is_prman_available():
    return prman is not None


def get_rman_gettr():
    if prman_rmanGettr is None:
        raise RuntimeError('prman.rmanGettr() is not available.')
    return prman_rmanGettr()


def initialize_prman(name='python', options=None):
    if not is_prman_available():
        raise RuntimeError('RenderMan Python API is not available.')
    if hasattr(prman, 'RiBegin'):
        prman.RiBegin(name)
    elif hasattr(prman, 'Begin'):
        prman.Begin(name)
    else:
        raise RuntimeError('RenderMan API does not expose RiBegin or Begin.')

    if options:
        for key, value in options.items():
            set_prman_option(key, value)


def set_prman_option(name, value):
    if not is_prman_available():
        raise RuntimeError('RenderMan Python API is not available.')
    if hasattr(prman, 'RiOption'):
        prman.RiOption('render', name, value)
    elif hasattr(prman, 'Option'):
        prman.Option('render', name, value)
    else:
        raise RuntimeError('RenderMan API does not expose RiOption or Option.')


def create_prman_display(filename='output.exr', display='rgba', type='string'):
    if not is_prman_available():
        raise RuntimeError('RenderMan Python API is not available.')
    if hasattr(prman, 'RiDisplay'):
        prman.RiDisplay(filename, display, type)
    elif hasattr(prman, 'Display'):
        prman.Display(filename, display, type)
    else:
        raise RuntimeError('RenderMan API does not expose RiDisplay or Display.')


def end_prman():
    if not is_prman_available():
        return
    if hasattr(prman, 'RiEnd'):
        prman.RiEnd()
    elif hasattr(prman, 'End'):
        prman.End()


def backgroundRender():
    ensure_maya_available()
    return MayaCmds.ls(dag=True, long=True)


def bakeSimulation():
    ensure_maya_available()
    return MayaCmds.ls(dag=True, long=True)


def is_running_in_maya():
    return MayaCmds is not None


def initialize_maya_standalone():
    if maya is None:
        raise RuntimeError('Maya standalone module is not available.')
    maya.standalone.initialize(name='python')


def print_environment_status():
    print('Maya API available:', is_running_in_maya())
    print('RenderMan API available:', is_prman_available())
    if is_running_in_maya():
        print('Maya version: %s' % MayaCmds.about(version=True))
    if is_prman_available():
        if hasattr(prman, '__version__'):
            print('RenderMan version:', prman.__version__)


def main():
    print('Running Maya tests...')
    print_environment_status()
    if is_running_in_maya():
        configure_render_globals()
        nodes = list_all_nodes()
        print('Found %d DAG nodes.' % len(nodes))
    if is_prman_available():
        try:
            get_rman_gettr()
            print('RenderMan getter is available.')
        except RuntimeError as exc:
            print('RenderMan helper error:', exc)
    if not is_running_in_maya() and not is_prman_available():
        print('Neither Maya nor RenderMan APIs are available. Run this module in a supported environment.')


if __name__ == '__main__':
    main()

