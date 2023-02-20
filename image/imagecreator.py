import PIL


def create_image(MEDIA_ROOT, root, path, height):
    with PIL.Image.open((MEDIA_ROOT + '/' + path)) as im:
        w, h = im.size
        new_size = (int(w * (int(height) / h)), int(height))
        im.thumbnail(new_size)
        im.save(root + '/' + path.split('/')[-1])
    return