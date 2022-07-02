import shutil
import os
import FreeCADGui, FreeCAD
import glob
from PIL import Image

def animate(size=128, step=10, path='~/Videos/logo'):
    path = os.path.expanduser(path)
    shutil.rmtree(path)
    os.mkdir(path)
    obj = FreeCAD.getDocument('LogoAsm').getObjectsByLabel('PlaneCoincident')[0]
    FreeCAD.setActiveDocument(obj.Document.Name)
    view = FreeCADGui.getDocument(obj.Document.Name).ActiveView
    for i, a in enumerate(range(0, 360+step, step)):
        obj.Angle = a
        obj.Document.recompute()
        FreeCADGui.runCommand('asm3CmdQuickSolve',0)
        FreeCADGui.updateGui()
        FreeCADGui.updateGui()
        FreeCADGui.updateGui()
        filename = f'{path}/frame{i:03d}.png'
        #  print(f'saving {filename}')
        view.saveImage(filename, size, size, '#00000000')

    fp_in = f"{path}/*.png"
    fp_out = f"{path}/../logo.gif"

    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
    imgs = (Image.open(f) for f in sorted(glob.glob(fp_in)))
    img = next(imgs)  # extract first image from iterator
    img.save(fp=fp_out, format='GIF', append_images=imgs, disposal=2,
            save_all=True, duration=100, loop=0, transparency=0)
