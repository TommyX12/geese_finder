m = 1.5

loc=zeros(size(x, 1)-1, 2);

latex = string('\n');

for i = 1:size(x, 1)-1                
    r = sqrt((x(i+1)-0.5)^2 + (y(i+1)-0.5)^2);
    y(i+1) = (y(i+1)-0.5)*(1-1.0*r^2)/0.5+0.5;
    x(i+1) = (x(i+1)-0.5)*(1-1.0*r^2)/0.5+0.5;
    loc(i, 1) = lat(i+1)-x(i+1)*sin(heading(i+1))+y(i+1)*cos(heading(i+1));
    loc(i, 2) = lon(i+1)+y(i+1)*sin(heading(i+1))+x(i+1)*cos(heading(i+1));
    latex += string(i)) + string('&')+ string(loc(i, 1)) + string('&') + string(loc(i, 2)) + string('\\')
end

    