clear;
pkg load io; %importamos la librería io
close all;
clc;
%importamos los datos de la pruba realizada
data = csv2cell("data_all.csv",",");#data.csv es el .csv de prueba
#data = csv2cell("data_all.csv",",");#data.csv es el .csv de prueba
%nos quedamos con los números y creo una matriz
num = cell2mat(data(2:end,2:10));
%nos quedamos con el instante en el que se tomaron los datos
date = data(2:end,11);
%convertimos en character array para poder hacer split en el tiempo
date = char(date);
for i = 1:length(date)
ans=strsplit(date(i,:)," ");
%nos quedamos con las horas minutos y segundos
hms(i)=ans(2);
endfor
hms=char(hms);
%encabezado de cada uno
fields = char(data(1,:));
%Representación
for i = 3:(length(fields)-2)
  if i == 6 || i == 7 %que no selecione la latitud y longitud
    continue
  else
    figure; %crea una gráfica
    hold on;%la mantiene
    plot(1:length(num(:,i)),num(:,i)); %pinta las líneas azules
    plot(1:length(num(:,i)),num(:,i),'*r'); %pinta los puntos rojos
    xlabel('número de muestra'); %nombra el eje x
    title(fields(i+1,:)); %pone título a la gráfica
    grid; %crea un mallado para visualizar mejor los datos
    axis([0 length(num(:,i))]); %define la escala del eje x
  endif
endfor