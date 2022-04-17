from asyncio import get_event_loop
from uuid import uuid4

from PIL import Image

from pyodide.http import pyfetch
from js import Blob, URL, Reflect
from pyact import use_memo, use_effect, use_state, as_js

IDENTITY = lambda img: img


async def save_image_to_vfs(asset_path):
    _, ext = asset_path.rsplit(".", 1)
    file_path = uuid4().hex
    response = await pyfetch(asset_path)
    if response.status == 200:
        with open(file_path, "wb") as f:
            f.write(await response.bytes())
        return file_path, ext
    return None, None


def transform_image(vfs_path, format, transformer=IDENTITY):
    with Image.open(vfs_path) as img:
        img = transformer(img)
        changed_path = uuid4().hex
        img.save(changed_path, format=format)
        return changed_path


def create_blob(data, mime_type):
    blob = Reflect.construct(Blob, as_js([[data], dict(type=mime_type)]))
    return blob


def use_vfs_asset(asset_path):
    vfs_path, set_vfs_path = use_state(as_js((None, None)))

    @use_effect(asset_path)
    def load_iasset():
        async def load():
            path = await save_image_to_vfs(asset_path)
            if path is not None:
                set_vfs_path(as_js(path))

        get_event_loop().run_until_complete(load())

    return vfs_path


def use_image_transformation(vfs_path, format, transformer=IDENTITY):
    @use_memo(vfs_path, format, transformer)
    def transformed_vfs_asset_path():
        if vfs_path is None:
            return None
        return transform_image(vfs_path, format, transformer)

    return transformed_vfs_asset_path


def use_blob(vfs_path, mime_type):
    @use_memo(vfs_path, mime_type)
    def blob():
        if vfs_path is None:
            return None
        with open(vfs_path, "rb") as f:
            return create_blob(f.read(), mime_type)

    return blob


def use_object_url(object):
    @use_memo(object)
    def object_url():
        if object is None:
            return None
        return URL.createObjectURL(object)

    @use_effect(object_url)
    def clear_object_url():
        if object_url is not None:
            return lambda: URL.revokeObjectURL(object_url)

    return object_url


def use_image_transformer(asset_path, transformer=IDENTITY):
    vfs_path, extension = use_vfs_asset(asset_path)
    transformed_path = use_image_transformation(vfs_path, extension, transformer)
    blob = use_blob(transformed_path, f"image/{extension}")
    image_path = use_object_url(blob)

    return image_path


def use_style(counter):
    color = "error" if counter < 0 else "warning" if counter == 0 else "success"

    @use_memo(color)
    def style():
        return dict(color=f"{color}.main")

    @use_effect(counter)
    def print_counter():
        print(f"Counter: {counter}")

    return style
