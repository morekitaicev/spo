#!/bin/bash
(echo "Filepath;Filename;Extension;Size;Permissions;Creation date;Modify date;MIME-type;Duration;Image size")>./Info.csv #Вводим в файл с таблицей выходных файлов названия столбцов
pars() #Пишем функцию для поиска свойств файлов
{
        (
        for i in "$1"/*
        do
        object=$i
        if [[ -d $object && -s $object ]]; then #Если объектом является директория, то рекурсивно применяем функцию для посика свойств файлов во вложенной директории
                pars "$object"
                continue
        fi
        filepath="$object" #Достаем путь к файлу, его имя и расширение
        filename="$(basename $object)"
        extension="${filename#*.}"
	filename="${filename%.*}"
        if [[ $filename == $extension ]]; then #Если нет расширения то оставляем неизвестное расширение
                extension="unknown"
        fi
        duration="$(mediainfo "$object" --Output="General;%Duration/String%")" #Достаем длительность аудио- или видеофайла, если она имеется
        if [[ $extension == "jpg" || $extension == "png" || $extension == "jpeg" ]]; then #Если файл является картинкой достаем её разрешение в пикселях
                imgsize=$(identify -format '%w x %h' $object)
        else 
                imgsize="-"
        fi
        size=$(stat -c%s "$object") #Достаем остальные свойства файла
        access=$(stat -c%A "$object")
        birth=$(stat -t -c%.10w "$object")
        mod=$(stat -t -c%.10y "$object")
        mime=$(file --mime-type -b "$object")
	echo "$filepath,$filename,$extension,$size,$access,$birth,$mod,$mime,$duration,$imgsize" | sed 's/,/;/g' #Закидываем все в файл попутно разделяя на столбцы
        done 
        )>>./Info.csv
}
pars /mnt/c/Users/morek/Downloads #Указываем директорию, к которой применяем данную программу
