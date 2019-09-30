#!/bin/bash
(echo "Filepath,Filename,Extension,Size,Permissions,Creation date, Modify date,MIME-type,Duration,Image size")>./Info.xls #Создаем названия столбцов в файле выхода

pars() #Прописываем функцию для вывода данных в файл
{
        (
        for i in "$1"/* #Для каждого объекта в директории выполняем следующее
        do
        object=$i
        if [[ -d $object && -s $object ]]; then #Если данный объект является папкой(директорией) рекурсивно применяем функцию для обработки этой директории 
                pars "$object"
                continue #Сразу же прыгаем на следующую итерацию цикла, так как директория не имеет файловых свойств
        fi
        filepath="$object"                #Ищем путь к файлу
        filename="$(basename $object)"    #Ищем имя файла
        extension="${object#*.}"          #Ищем расширение файла
        if [[ $filename == $extension ]]; then #Если расширение не указано, то оставляем неизвестное расширение
                extension="unknown"
        fi
        if [[ $extension == "mp4" || $extension == "mkv" ]]; then  #Ищем длительность видеофайлов с помощью утилиты mediainfo
                duration=$(mediainfo "$i"|head -n7|tail -n1|cut -c44-) #Достаем необходимую информацию из огромного вывода с помощью редактирования текста
        elif [[ $extension == "avi" ]]; then
                duration=$(mediainfo "$i"|head -n6|tail -n1|cut -c44-)
        elif [[ $extension == "mp3" ]]; then
                duration=$(mediainfo "$i"|head -n5|tail -n1|cut -c44-)
        elif [[ $extension == "jpg" || $extension == "png" || $extension == "jpeg" ]]; then
                imgsize=$(identify -format '%w %h' $object)
        else
                duration="-"
                imgsize="-"
        fi
        size=$(stat -c%s "$object")       #Размер файла в байтах
        access=$(stat -c%A "$object")     #Права доступа
        birth=$(stat -t -c%.10w "$object") #Дата создания
        mod=$(stat -t -c%.10y "$object")   #Дата последнего изменения
        mime=$(file --mime-type -b "$object") #Mime тип файла
        echo $filepath,$filename,$extension,$size,$access,$birth,$mod,$mime,$duration,$imgsize #Выводим информацию в файл
        done 
        )>>./Info.xls
}
pars ~/SPO #Применяем функцию к данной директории