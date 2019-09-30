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
        if [[ $extension == "mp4" || $extension == "mkv" ]]; then #Достаем длительность видеофайла исходя из его расширения(вывод утилиты mediainfo отличается для разных расширений)
                duration=$(mediainfo "$i"|head -n7|tail -n1|cut -c44-)
        elif [[ $extension == "avi" ]]; then
                duration=$(mediainfo "$i"|head -n6|tail -n1|cut -c44-)
        elif [[ $extension == "mp3" ]]; then
                duration=$(mediainfo "$i"|head -n5|tail -n1|cut -c44-)
        elif [[ $extension == "jpg" || $extension == "png" || $extension == "jpeg" ]]; then #Если файл является картинкой достаем её разрешение в пикселях
                imgsize=$(identify -format '%w x %h' $object)
        else
                duration="-" 
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
pars /mnt/c/Users/morek/Downloads
