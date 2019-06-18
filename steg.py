#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 15:24:21 2019

@author: max
"""
import math
from PIL import Image
chars = [
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
    'm',
    'n',
    'o',
    'p',
    'q',
    'r',
    's',
    't',
    'u',
    'v',
    'w',
    'x',
    'y',
    'z',
    'A',
    'B',
    'C',
    'D',
    'E',
    'F',
    'G',
    'H',
    'I',
    'J',
    'K',
    'L',
    'M',
    'N',
    'O',
    'P',
    'Q',
    'R',
    'S',
    'T',
    'U',
    'V',
    'W',
    'X',
    'Y',
    'Z',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '0',
    ' ',
    ',',
    '.',
    ':',
    ';',
    '`',
    '~',
    '!',
    '@',
    '#',
    '$',
    '%',
    '^',
    '&',
    '*',
    '(',
    ')',
    '<',
    '>',
    '/',
    '\\',
    '\'',
    '"',
    '?',
    '-',
    '_',
    '+',
    '=',
    '{',
    '}',
    '[',
    ']',
    '|',]


def open_image(path):
    im = Image.open(path)
    return im


def save_image(image, path):
    image.save(path, 'png')


def get_pixel(image, x, y):
    width, height = image.size
    if x > width or y > height:
        return None
    pixel = image.getpixel((x, y))
    return pixel


def change_pixel(image, x, y, r, g, b, a):
    pix = image.load()
    pix[x, y] = (r, g, b, a)
    return image


def charToBin(char):
    return bin(chars.index(char))[2:]


def encode(path, newpath, message: str):
    im = open_image(path).convert('RGBA')
    im.save(path)
    y = 0
    width, height = im.size
    if len(message) > width * height:
        print('Message too long for provided image')
    for i in range(len(message)):
        if i < width:
            x = i
        else:
            x = i % width
            y = math.floor(i / width)
        char = message[i]
        charBin = charToBin(char)
        while len(charBin) < 7:
            charBin = '0' + charBin
        rgba = get_pixel(im, x, y)
        r = list('0' + bin(rgba[0])[2:])
        g = list('0' + bin(rgba[1])[2:])
        b = list('0' + bin(rgba[2])[2:])
        r[-2] = charBin[1]
        r[-1] = charBin[2]
        g[-2] = charBin[3]
        g[-1] = charBin[4]
        b[-2] = charBin[5]
        b[-1] = charBin[6]
        a = 255 - int(charBin[0])
        r = ''.join(r)
        g = ''.join(g)
        b = ''.join(b)
        r = int(r, 2)
        g = int(g, 2)
        b = int(b, 2)
        value = (r, g, b, a)
        pix = im.load()
        pix[x, y] = value
    save_image(im, newpath)
    exit()


def decode(path: str, length: int):
    im = open_image(path).convert('RGBA')
    string = ''
    y = 0
    width, height = im.size
    for i in range(length):
        if i < width:
            x = i
        else:
            x = i % width
            y = math.floor(i / width)
        rgba = get_pixel(im, x, y)
        r = '0' + bin(rgba[0])[2:]
        g = '0' + bin(rgba[1])[2:]
        b = '0' + bin(rgba[2])[2:]
        a = bin(255-rgba[3])[2:]
        binny = a[-1]+r[-2] + r[-1] + g[-2] + g[-1] + b[-2] + b[-1]
        try:
            char = chars[int(binny, 2)]
            string += char
        except IndexError:
            continue
    print(string)
