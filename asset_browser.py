import os
import re
import maya.cmds as cmds

# ===== Paths =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_FOLDER = os.path.join(BASE_DIR, "assets")
DEFAULT_THUMBNAIL = os.path.join(BASE_DIR, "default.png")

# Create asset folder if it doesn't exist
os.makedirs(ASSET_FOLDER, exist_ok=True)


def choose_classification(callback):
    """
    Opens a window that lets the user choose a classification
    (a top-level folder inside ASSET_FOLDER).

    When the user clicks "OK", the window closes and the callback
    is called with the chosen classification.
    """

    win = "ChooseClassificationWin"

    if cmds.window(win, exists=True):
        cmds.deleteUI(win)

    window = cmds.window(win, title="Choose Classification", widthHeight=(300, 100))

    cmds.columnLayout(adjustableColumn=True, rowSpacing=10)

    cmds.text(label="Select Classification:")

    option_menu = cmds.optionMenu("classOption")

    classifications = [
        d for d in os.listdir(ASSET_FOLDER)
        if os.path.isdir(os.path.join(ASSET_FOLDER, d))
    ]

    for cls in classifications:
        cmds.menuItem(label=cls)

    def onOK(*args):
        chosen = cmds.optionMenu("classOption", query=True, value=True)
        cmds.deleteUI(win)
        callback(chosen)

    cmds.button(label="OK", command=onOK)

    cmds.showWindow(window)


def get_maya_files(classification):
    """
    Searches the immediate subdirectories (asset folders) inside the chosen classification folder
    for Maya files (.ma or .mb) and matching thumbnail images.

    For each asset folder, if multiple Maya files exist
    (e.g. Asset_v001.ma, Asset_v002.ma, etc.),
    only the one with the highest version number is returned.
    """

    class_dir = os.path.join(ASSET_FOLDER, classification)

    files = []

    asset_dirs = [
        d for d in os.listdir(class_dir)
        if os.path.isdir(os.path.join(class_dir, d))
    ]

    version_regex = re.compile(r'^(.*)_v(\d+)$')

    for asset in asset_dirs:

        asset_dir = os.path.join(class_dir, asset)

        maya_files = [
            f for f in os.listdir(asset_dir)
            if f.endswith('.ma') or f.endswith('.mb')
        ]

        if not maya_files:
            continue

        latest_file = None
        highest_version = -1

        for f in maya_files:

            base, ext = os.path.splitext(f)

            match = version_regex.match(base)

            if match:
                version = int(match.group(2))
            else:
                version = 0

            if version > highest_version:
                highest_version = version
                latest_file = f

        if latest_file:

            asset_path = os.path.join(asset_dir, latest_file)

            base_name = os.path.splitext(latest_file)[0]

            thumb = None

            for ext in ['.png', '.jpg']:

                candidate = os.path.join(asset_dir, base_name + ext)

                if os.path.isfile(candidate):
                    thumb = candidate
                    break

            if not thumb:
                thumb = DEFAULT_THUMBNAIL

            files.append({
                'asset': asset_path,
                'thumbnail': thumb,
                'name': base_name
            })

    return files


def import_maya_file(asset_file, use_reference=False):
    """
    Imports the specified Maya file into the current scene.
    If use_reference is True, the file is referenced.
    """

    try:

        ns = os.path.basename(asset_file).replace('.', '_')

        if use_reference:
            cmds.file(asset_file, reference=True, namespace=ns)
        else:
            cmds.file(asset_file, i=True, namespace=ns)

        cmds.inViewMessage(
            amg='Imported: <hl>{}</hl>'.format(os.path.basename(asset_file)),
            pos='topCenter',
            fade=True
        )

    except Exception as e:

        cmds.error("Error importing asset: " + str(e))


def build_asset_browser(classification):
    """
    Builds the asset browser UI for the given classification.
    Displays all Maya files with thumbnails.
    """

    files = get_maya_files(classification)

    win = "AssetBrowserWin"

    if cmds.window(win, exists=True):
        cmds.deleteUI(win)

    window = cmds.window(
        win,
        title="Asset Browser - " + classification,
        widthHeight=(600, 400)
    )

    cmds.columnLayout(adjustableColumn=True)

    cmds.text(label="Import Mode:")

    import_mode = cmds.optionMenu("importMode")

    cmds.menuItem(label="Normal Import")
    cmds.menuItem(label="Reference Import")

    cmds.scrollLayout(childResizable=True)

    cmds.gridLayout(numberOfColumns=4, cellWidthHeight=(140, 140))

    for fileInfo in files:

        cmds.iconTextButton(
            style='iconAndTextVertical',
            image=fileInfo['thumbnail'],
            label=fileInfo['name'],
            width=140,
            height=140,
            command=lambda asset=fileInfo['asset']:
                import_maya_file(
                    asset,
                    use_reference=(cmds.optionMenu("importMode", q=True, select=True) == 2)
                )
        )

    cmds.setParent('..')
    cmds.setParent('..')

    cmds.showWindow(window)


def main():
    """
    Main entry point.
    """

    choose_classification(build_asset_browser)


main()
