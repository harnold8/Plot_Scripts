clear
clc
close all

anz=1;
%to save the end values of the trajectory
values=zeros(anz,3);

%mapping 3D Texture onto sphere
f = figure();
original=imread('europa2.tif');
original = flipdim(original ,2);
[x,y,z]=ellipsoid(0,0,0,1,1,1,300);
surf(x,y,-z);
h=findobj('Type','surface');
set(h,'CData',original,'Facecolor','texturemap','edgecolor','none','HandleVisibility','off');
rotate(h,[0 0 1],-270);
axis equal;
hold on;

%background color    
set(gcf,'color','white');
set(gca,'color','white');
set(gca,'Visible','off');

%plot boundaries
min1=-3;
max1=3;
axis([min1 max1 min1 max1 -5 5]);



%cylinders
[X,Y,Z] = cylinder(1.,50)
%red
l=length(X);
Z=Z*5;
alpha=pi/4;
%calculating the inclination
for i=1:l
    X(2,i)=X(2,i)+tan(alpha)*Z(2,i);
end

%plotting the cylinders
%upper
h=surf(X,Y,Z);
set(h,'edgecolor','none','facecolor','black')
set(h,'FaceAlpha',0.5)
%lower
Z=Z*(-1);
h=surf(X,Y,Z);
set(h,'edgecolor','none','facecolor','black')
set(h,'FaceAlpha',0.5)

%plotting the arrows
anz=10
for i=1:anz
[X,Y,Z] = cylinder(1.,50);
stepsize=4/anz;
z_n=i*stepsize;
l=length(X);

for i=1:l
    X(2,i)=X(2,i)+tan(alpha)*z_n;
    Z(2,i)=z_n;
end
l2=round(l/2);
l4=floor(l/4);
plot3(X(2,1:l4),Y(1,1:l4),Z(2,1:l4),'-','color','blue','linewidth',2);
mArrow3([X(2,1+2) Y(2,1+2) z_n],[X(2,l) Y(2,l) z_n],'color','blue','stemWidth',0.025);
mArrow3([X(2,1+2) Y(2,1+2) -z_n],[X(2,l) Y(2,l) -z_n],'color','blue','stemWidth',0.025);

plot3(X(2,l4:l2),Y(1,l4:l2),Z(2,l4:l2),'-','color','red','linewidth',2);
mArrow3([X(2,l4) Y(2,l4) z_n],[X(2,l4)+0.2 Y(2,l4) z_n],'color','red','stemWidth',0.025);
mArrow3([X(2,l4) Y(2,l4) -z_n],[X(2,l4)+0.2 Y(2,l4) -z_n],'color','red','stemWidth',0.025);


plot3(X(2,l2:l4+l2),Y(1,l2:l4+l2),Z(2,l2:l4+l2),'-','color','blue','linewidth',2);
mArrow3([X(2,l4+l2) Y(2,l4+l2) z_n],[X(2,l4+l2)+0.2 Y(2,l4+l2) z_n],'color','blue','stemWidth',0.025);
mArrow3([X(2,l4+l2) Y(2,l4+l2) -z_n],[X(2,l4+l2)+0.2 Y(2,l4+l2) -z_n],'color','blue','stemWidth',0.025);

plot3(X(2,l4+l2:l),Y(1,l4+l2:l),Z(2,l4+l2:l),'-','color','red','linewidth',2);
mArrow3([X(2,l-2) Y(2,l-2) z_n],[X(2,l) Y(2,l) z_n],'color','red','stemWidth',0.025);
mArrow3([X(2,l-2) Y(2,l-2) -z_n],[X(2,l) Y(2,l) -z_n],'color','red','stemWidth',0.025);

plot3(X(2,1:l4),Y(1,1:l4),-Z(2,1:l4),'-','color','blue','linewidth',2);
plot3(X(2,l4:l2),Y(1,l4:l2),-Z(2,l4:l2),'-','color','red','linewidth',2);
plot3(X(2,l2:l4+l2),Y(1,l2:l4+l2),-Z(2,l2:l4+l2),'-','color','blue','linewidth',2);
plot3(X(2,l4+l2:l),Y(1,l4+l2:l),-Z(2,l4+l2:l),'-','color','red','linewidth',2);

if z_n<0.5
   mArrow3([-5 -Y(1,l4+5) stepsize],[X(2,l4+5) -Y(1,l4+5) stepsize],'color','black','stemWidth',0.015); 
   mArrow3([-5 -Y(1,l4+5) -stepsize],[X(2,l4+5) -Y(1,l4+5) -stepsize],'color','black','stemWidth',0.015);
else   
    if z_n<1
       mArrow3([-5 -Y(1,l4+9) stepsize*2],[X(2,l4+9) -Y(1,l4+9) stepsize*2],'color','black','stemWidth',0.015);
       mArrow3([-5 -Y(1,l4+9) -stepsize*2],[X(2,l4+9) -Y(1,l4+9) -stepsize*2],'color','black','stemWidth',0.015);
    else
        mArrow3([-5 0 z_n],[min(X(2,:)) 0 z_n],'color','black','stemWidth',0.015);
        mArrow3([-5 0 -z_n],[min(X(2,:)) 0 -z_n],'color','black','stemWidth',0.015);
    end
end

end


%viewingangle for the plot
phi=-39.;
theta=21.;


view([phi theta]);
set(gcf,'units','centimeters','PaperPosition',[0 0 15 8]);
fig = gcf;
fig.InvertHardcopy = 'off';
string="alfvenwing.png"
print(gcf,string,'-dpng','-r500');
