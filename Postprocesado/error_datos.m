close all; clc;
%Ahora estudiamos el error, para ello introducimos el valor mínimo y máximo del
%rango que pretendemos estudiar [min max]
%script preconfigurado para analizar de inicio a fin
%Se puede cambiar manualmente
pkg load statistics;
final = length(num(:,3));
Temp = [188 final];
Ph = [1 final];
O2 = [146 final];
Cond = [1 final];
Orp = [155 301];
%Creamos una matriz con esos rangos (no tocar)
rango = zeros(11,2);
rango(3,:) = Temp;
rango(4,:) = Ph;
rango(5,:) = O2;
rango(8,:) = Cond;
rango(9,:) = Orp;

%matriz que almacenará los valores estadísticos de los datos anteriores
val = zeros(11,3); % Media | desviación estándar | asimetría

%Pintamos un histograma con la dristribución de los datos, de esta forma si se 
%selecciona un rango adecuado podemos visualizar el error y ver si su 
%distribución es normal
ncampos=10; %modifica la resolución del histograma
fprintf("         Media         S.T.D.       Asimetría\n");
for i = 3:(length(fields)-2)
  if i == 6 || i == 7 %que no seleccione la latitud y longitud
    continue
  else
    figure; %crea una gráfica
    hold on;%la mantiene
    hist(num(rango(i,1):rango(i,2),i),ncampos);
    ylabel('frecuencia'); %nombra el eje y
    title(fields(i+1,:)); %pone título a la gráfica
    grid; %crea un mallado para visualizar mejor los datos
    %Ahora calculamos la media, desviación estándar
    val(i,1) = mean(num(rango(i,1):rango(i,2),i)); %media
    val(i,2) = std(num(rango(i,1):rango(i,2),i));
    val(i,3) = skewness(num(rango(i,1):rango(i,2),i));
    fprintf("%s \n",fields(i+1,:));%Imprime por pantalla el título
    %Imprime por pantalla los resultados
    fprintf("       %f   |   %f   |  %f\n",val(i,1),val(i,2),val(i,3));
    
  endif
endfor
%Error asociado
fprintf("\nConfianza del 95.4%s \n","%");
for i = 3:(length(fields)-2)
  if i == 6 || i == 7 %que no seleccione la latitud y longitud
    continue
  else
    error = 2*val(i,2); %Error del 95.4% de confianza
    fprintf("\nError %s\n",fields(i+1,:));
    fprintf("%f   |   %f\n",-error,error);
    
  endif
endfor
