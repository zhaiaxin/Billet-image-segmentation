# This file is used to split the path into 3 parts
# path, name and suffix


def split_slash(path_name_suffix):
    """
    This method only work with '/'

    :param path_name_suffix: absolute path to the image file, just like"c:/a/b/c.png"
    :return: the path and the name_suffix, "c:/a/b" and "c.png"
    """
    x = []
    for i in range(len(path_name_suffix)):
        if path_name_suffix[i] == '/':
            x.append(i)

    path = path_name_suffix[0:max(x)]
    name_suffix = path_name_suffix[max(x) + 1:len(path_name_suffix)]

    return path, name_suffix


def split_dot(name_suffix):
    """
    This methond only work with '.'

    :param name_suffix: the name and suffix of an image, just like 'c.png'
    :return: the name of the image, 'c'
    """
    index = name_suffix.index(".")
    name = name_suffix[0:index]

    return name


if __name__ == '__main__':
    path, name_suffix = split_slash("c:/a/b/c.png")
    name = split_dot(name_suffix)
    print(path, name_suffix, name)
