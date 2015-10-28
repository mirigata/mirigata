#!/usr/bin/env bash

set -e
set -u

TARGET=$(pwd)
FONT=/Library/Fonts/Luminari.ttf

mkdir -p ${TARGET}

convert -background orange -fill white -font ${FONT}  -size 32x32 -gravity South label:M ${TARGET}/favicon.png
convert -background orange -fill white -font ${FONT}  -size 32x32 -gravity South label:M ${TARGET}/favicon.ico

convert -background transparent -fill white -font ${FONT} -size x48 -gravity South label:M ${TARGET}/logo-mini.png
convert -background transparent -fill white -font ${FONT} -size 800x label:Mirigata ${TARGET}/logo-full.png
